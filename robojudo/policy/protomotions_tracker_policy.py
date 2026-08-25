"""ProtoMotions tracker policy for RoboJuDo.

Runs a unified ONNX model exported by
``deployment/export_bm_tracker_onnx.py`` with cached 50 fps motion from
``deployment/motion_utils.MotionPlayer``.

Key inputs:

- ``historical.processed_actions`` — action history feedback (previous PD
  targets are fed back as an ONNX input)
- ``mimic.future_anchor_rot`` — anchor-body-only rotation references

Heading alignment
-----------------
Yaw-only offset computed on first step to align motion heading with robot heading.

Sensor requirements (real G1)
-----------------------------
- ``env_data.dof_pos`` / ``env_data.dof_vel`` -- joint encoders
- ``env_data.base_quat`` (xyzw) -- pelvis IMU
- ``env_data.base_ang_vel`` -- pelvis IMU gyro (body-local frame)
- ``env_data.torso_quat`` (xyzw) -- FK-computed (requires ``update_with_fk=True``)
"""

import logging
import re

import numpy as np
import onnxruntime as ort
import yaml

from robojudo.policy import Policy, policy_registry
from robojudo.policy.policy_cfgs import PolicyCfg
from robojudo.tools.tool_cfgs import DoFConfig
from robojudo.utils.motion_utils import (
    MotionPlayer,
    _extract_yaw_quat_np,
    apply_heading_offset_np,
    compute_yaw_offset_np,
)

logger = logging.getLogger(__name__)


def _slerp_np(a_xyzw: np.ndarray, b_xyzw: np.ndarray, t: float) -> np.ndarray:
    """Spherical linear interpolation between two xyzw quaternions."""
    b = b_xyzw if float(np.dot(a_xyzw, b_xyzw)) >= 0.0 else -b_xyzw
    d = abs(float(np.dot(a_xyzw, b)))
    if d > 0.9995:  # nearly parallel -- lerp and renormalise
        out = a_xyzw + t * (b - a_xyzw)
    else:
        theta = np.arccos(d)
        out = (np.sin((1.0 - t) * theta) * a_xyzw + np.sin(t * theta) * b) / np.sin(theta)
    return (out / np.linalg.norm(out)).astype(np.float32)


@policy_registry.register
class ProtoMotionsTrackerPolicy(Policy):
    """Policy that drives a ProtoMotions tracker via unified ONNX model.

    The ONNX model bakes in: obs computation -> actor MLP -> action processing.
    Inputs are raw context tensors; outputs are absolute PD position targets.
    """

    cfg_policy: PolicyCfg

    def __init__(self, cfg_policy: PolicyCfg, device: str = "cpu"):
        # Load YAML metadata BEFORE calling super().__init__ so we can
        # build the DOF config from it.
        onnx_path = cfg_policy.policy_file
        yaml_path = onnx_path.replace(".onnx", ".yaml")

        with open(yaml_path) as f:
            self._meta = yaml.safe_load(f)

        robot_meta = self._meta["robot"]
        control_meta = self._meta["control"]
        motion_meta = self._meta["motion"]
        runtime = self._meta["_runtime"]

        joint_names = robot_meta["joint_names"]
        num_dofs = robot_meta["num_dofs"]
        stiffness = control_meta["stiffness"]
        damping = control_meta["damping"]
        effort_limits = control_meta.get("effort_limits")

        # Build DOF config from YAML metadata.
        dof_cfg = DoFConfig(
            joint_names=joint_names,
            default_pos=[0.0] * num_dofs,
            stiffness=stiffness,
            damping=damping,
            torque_limits=effort_limits,
        )
        cfg_policy_updated = cfg_policy.model_copy()
        cfg_policy_updated.obs_dof = dof_cfg
        cfg_policy_updated.action_dof = dof_cfg

        super().__init__(cfg_policy=cfg_policy_updated, device="cpu")

        # ONNX session
        logger.info(f"[TrackerPolicy] Loading ONNX: {onnx_path}")
        self._session = ort.InferenceSession(
            onnx_path, providers=["CPUExecutionProvider"]
        )
        self._onnx_in_names = [inp.name for inp in self._session.get_inputs()]
        self._onnx_out_names = [out.name for out in self._session.get_outputs()]
        self._onnx_name_to_key = runtime["onnx_name_to_in_key"]

        # Motion player (cached mode -- no protomotions import)
        motion_path = getattr(cfg_policy, "motion_path", None)
        if motion_path is None:
            raise ValueError("ProtoMotionsTrackerPolicyCfg must set motion_path")
        motion_index = getattr(cfg_policy, "motion_index", 0)
        timing = self._meta["timing"]
        self._player = MotionPlayer(
            motion_path, motion_index=motion_index, control_dt=timing["control_dt"]
        )

        # ONNX input config
        self._anchor_idx = robot_meta["anchor_body_index"]
        self._root_idx = robot_meta["root_body_index"]
        self._future_step_indices = motion_meta["future_step_indices"]

        # Determine how to read the anchor body rotation from env_data.
        # Use body name to look up in fk_info; pelvis uses base_quat directly.
        self._anchor_body_name = robot_meta.get("anchor_body_name")
        logger.info(
            f"[TrackerPolicy] anchor body: "
            f"{self._anchor_body_name or 'pelvis'} (idx={self._anchor_idx})"
        )

        # Action post-processing config
        self._pd_target_max_accel = control_meta.get("pd_target_max_accel")
        self._action_ema_alpha = control_meta.get("action_ema_alpha", 1.0)

        logger.info(
            f"[TrackerPolicy] {num_dofs} DOFs, "
            f"{self._player.total_frames} motion frames, "
            f"anchor_idx={self._anchor_idx}, root_idx={self._root_idx}"
        )

        # Resolve default standing pose from protomotions robot config.
        self._default_dof_pos = self._resolve_default_dof_pos(joint_names)

        # Reference-mode blend length (see set_default_pose_mode).
        blend_s = float(getattr(cfg_policy, "mode_blend_seconds", 0.5))
        self._blend_steps = max(int(round(blend_s / timing["control_dt"])), 0)
        logger.info(
            f"[TrackerPolicy] mode blend: {blend_s:.2f}s "
            f"({self._blend_steps} control steps)"
        )

        self._heading_offset = None
        self.reset()

    # G1 default standing pose (from protomotions.robot_configs.g1)
    _G1_DEFAULT_JOINT_POS = {
        ".*_hip_pitch_joint": -0.312,
        ".*_knee_joint": 0.669,
        ".*_ankle_pitch_joint": -0.363,
        ".*_elbow_joint": 0.6,
        "left_shoulder_roll_joint": 0.2,
        "left_shoulder_pitch_joint": 0.2,
        "right_shoulder_roll_joint": -0.2,
        "right_shoulder_pitch_joint": 0.2,
    }

    def _resolve_default_dof_pos(self, joint_names: list[str]) -> np.ndarray:
        """Resolve default DOF positions via regex-pattern matching."""
        DEFAULT_JOINT_POS = self._G1_DEFAULT_JOINT_POS

        default_pos = np.zeros(len(joint_names), dtype=np.float32)
        for pattern, value in DEFAULT_JOINT_POS.items():
            for i, name in enumerate(joint_names):
                if re.fullmatch(pattern, name):
                    default_pos[i] = value
        logger.info(f"[TrackerPolicy] resolved default DOF pos: {default_pos}")
        return default_pos

    def set_default_pose_mode(self, enabled: bool):
        """Switch between tracking real motion and holding default pose.

        When enabled, the policy sees synthetic references for the default
        standing pose instead of the real motion.  Used during prepare/rampdown.
        The switch itself is ramped: ``_blend_mix`` moves from its current
        value to the new one over ``_blend_steps`` control steps, so the policy's
        reference inputs stay continuous.  The pipeline flips this flag in one
        step (``[MOTION_DONE]`` / ``[MOTION_FADE_OUT]`` / ``[MOTION_RESET]``),
        and its own 5 s blend-out path is unreachable for policies that have
        this method -- without the ramp the references jump in a single frame.
        """
        if enabled == self._default_pose_mode and self._blend_step >= self._blend_steps:
            return  # already settled in this mode
        self._default_pose_mode = enabled
        if enabled:
            self._motion_done = False
        # Resume from wherever the current ramp got to, so a reversal mid-blend
        # does not snap the references.
        self._blend_from = self._blend_mix
        self._blend_to = 1.0 if enabled else 0.0
        self._blend_step = 0
        logger.info(
            f"[TrackerPolicy] default_pose_mode={'ON' if enabled else 'OFF'} "
            f"(ramping refs {self._blend_from:.2f} -> {self._blend_to:.0f} "
            f"over {self._blend_steps} steps)"
        )

    @property
    def _blending(self) -> bool:
        return self._blend_step < self._blend_steps

    def _advance_blend(self) -> float:
        """Step the mode ramp and return the current mix (0=motion, 1=default)."""
        if self._blend_steps <= 0:
            self._blend_mix = self._blend_to
            return self._blend_mix
        if self._blend_step < self._blend_steps:
            self._blend_step += 1
        u = self._blend_step / self._blend_steps
        u = u * u * (3.0 - 2.0 * u)  # smoothstep: zero slope at both ends
        self._blend_mix = self._blend_from + (self._blend_to - self._blend_from) * u
        return self._blend_mix

    def reset(self):
        self._frame = 0
        self._prev_pd = None
        self._prev_prev_pd = None
        self._ema_prev = None
        self._stashed_pd_targets = np.zeros(self.num_actions, dtype=np.float32)
        self._prev_actions = np.zeros(self.num_actions, dtype=np.float32)
        self._motion_done = False
        self._paused = False
        self._default_pose_mode = False
        # Reference-mode ramp state (0 = pure motion, 1 = pure default pose).
        # Preserve an in-progress ramp: on [MOTION_RESET] the pipeline calls
        # set_default_pose_mode(False) immediately before this, and snapping
        # here would undo the ramp it just started.
        if not hasattr(self, "_blend_mix"):
            self._blend_mix = 0.0
            self._blend_from = 0.0
            self._blend_to = 0.0
            self._blend_step = self._blend_steps
        else:
            self._blend_from = self._blend_mix
            self._blend_to = 0.0
            self._blend_step = self._blend_steps if self._blend_mix <= 0.0 else 0

    def reset_alignment(self):
        self._heading_offset = None

    def post_step_callback(self, commands=None):
        # Hold at the current frame while ramping *into* the motion, so the
        # ramp does not consume the opening of the clip.
        ramping_in = self._blending and self._blend_to == 0.0
        if not self._paused and not self._default_pose_mode and not ramping_in:
            self._frame += 1
            if self._frame >= self._player.total_frames:
                self._frame = self._player.total_frames - 1
                self._motion_done = True
        for cmd in commands or []:
            if cmd in ("[MOTION_RESET]", "[MOTION_FADE_IN]"):
                self.reset()

    def get_observation(self, env_data, ctrl_data):
        # -- Heading alignment (first step after reset) --
        if self._heading_offset is None:
            motion_anchor_rot = self._player.get_state_at_frame(0)["body_rot"][self._anchor_idx]
            robot_anchor_rot = self._get_anchor_quat(env_data)
            self._heading_offset = compute_yaw_offset_np(robot_anchor_rot, motion_anchor_rot)

        # -- State from env_data (already xyzw) --
        anchor_rot = self._get_anchor_quat(env_data)
        dof_pos = np.asarray(env_data.dof_pos, dtype=np.float32)
        dof_vel = np.asarray(env_data.dof_vel, dtype=np.float32)
        # env_data.base_ang_vel comes from MuJoCo qvel[3:6] which is ALREADY
        # in the pelvis local frame (not world frame).  On the real G1, the
        # IMU gyroscope also reads in body-local frame.  So we use it directly
        # as root_local_ang_vel -- NO quat_rotate_inverse needed.
        root_local_ang_vel = np.asarray(env_data.base_ang_vel, dtype=np.float32)

        # -- References: motion, default pose, or a ramp between the two --
        # mix = 0 -> pure motion, 1 -> pure default standing pose.
        mix = self._advance_blend()
        num_steps = len(self._future_step_indices)

        if mix < 1.0:
            # Future motion references with heading alignment.
            # Clamp each future step so it never exceeds the last valid frame.
            # This repeats the last frame's references at end-of-motion instead
            # of going out of bounds.
            last_frame = self._player.total_frames - 1
            clamped_steps = [min(self._frame + step, last_frame) - self._frame for step in self._future_step_indices]
            future_refs = self._player.get_future_references(self._frame, clamped_steps)
            future_body_rot = apply_heading_offset_np(self._heading_offset, future_refs["body_rot"])
            # Anchor-body-only rotation: [num_steps, 4]
            motion_rot = future_body_rot[:, self._anchor_idx, :]
            motion_dof_pos = future_refs["dof_pos"]
            motion_dof_vel = future_refs["dof_vel"]

        if mix > 0.0:
            # Synthetic references: hold the default standing pose.
            # Target DOFs = default standing pose, velocities = zero,
            # anchor rotation = yaw-only from robot's current anchor (hold
            # heading but neutral pitch/roll for stable upright standing).
            anchor_yaw_only = _extract_yaw_quat_np(anchor_rot)
            stand_rot = np.tile(anchor_yaw_only, (num_steps, 1))
            stand_dof_pos = np.tile(self._default_dof_pos, (num_steps, 1))
            stand_dof_vel = np.zeros_like(stand_dof_pos)

        if mix <= 0.0:
            future_anchor_rot = motion_rot
            future_dof_pos = motion_dof_pos
            future_dof_vel = motion_dof_vel
        elif mix >= 1.0:
            future_anchor_rot = stand_rot
            future_dof_pos = stand_dof_pos
            future_dof_vel = stand_dof_vel
        else:
            future_anchor_rot = np.stack(
                [_slerp_np(motion_rot[i], stand_rot[i], mix) for i in range(num_steps)]
            )
            future_dof_pos = (1.0 - mix) * motion_dof_pos + mix * stand_dof_pos
            future_dof_vel = (1.0 - mix) * motion_dof_vel + mix * stand_dof_vel

        # -- Build ONNX inputs --
        key_to_array = {
            "current.dof_pos": dof_pos[None],
            "current.dof_vel": dof_vel[None],
            "current.anchor_rot": anchor_rot[None],
            "current.root_local_ang_vel": root_local_ang_vel[None],
            "mimic.future_anchor_rot": future_anchor_rot[None],
            "mimic.future_dof_pos": future_dof_pos[None],
            "mimic.future_dof_vel": future_dof_vel[None],
            "historical.processed_actions": self._prev_actions[None, None],
        }
        onnx_inputs = {}
        for onnx_name in self._onnx_in_names:
            sem_key = self._onnx_name_to_key.get(onnx_name)
            if sem_key and sem_key in key_to_array:
                onnx_inputs[onnx_name] = key_to_array[sem_key].astype(np.float32)

        # -- ONNX inference --
        ort_out = self._session.run(self._onnx_out_names, onnx_inputs)
        pd_targets = ort_out[1].squeeze().copy()

        # -- PD target acceleration clamp --
        if (
            self._pd_target_max_accel is not None
            and self._prev_pd is not None
            and self._prev_prev_pd is not None
        ):
            delta = pd_targets - self._prev_pd
            prev_delta = self._prev_pd - self._prev_prev_pd
            accel = delta - prev_delta
            clamped_accel = np.clip(
                accel, -self._pd_target_max_accel, self._pd_target_max_accel
            )
            pd_targets = self._prev_pd + prev_delta + clamped_accel
        self._prev_prev_pd = self._prev_pd
        self._prev_pd = pd_targets.copy()

        # -- EMA action filter --
        alpha = self._action_ema_alpha
        if alpha < 1.0:
            if self._ema_prev is None:
                self._ema_prev = pd_targets.copy()
            pd_targets = alpha * pd_targets + (1.0 - alpha) * self._ema_prev
            self._ema_prev = pd_targets.copy()

        self._stashed_pd_targets = pd_targets
        self._prev_actions = pd_targets.copy()
        extras = {
            "CALLBACK": (
                ["[MOTION_DONE]"]
                if self._motion_done and not self._default_pose_mode
                else []
            ),
        }
        dummy_obs = np.zeros(1, dtype=np.float32)
        return dummy_obs, extras

    def _get_anchor_quat(self, env_data) -> np.ndarray:
        """Read the anchor body's quaternion from env_data.

        Uses the body name from YAML metadata to look up in fk_info.
        Falls back to base_quat for pelvis (root body).
        """
        name = self._anchor_body_name
        if name is not None and name not in (None, "pelvis"):
            # Named body -- look up in FK info
            fk = env_data.fk_info
            if fk is not None and name in fk:
                return np.asarray(fk[name]["quat"], dtype=np.float32)
            # Fallback: if the env exposes it as torso_quat and name matches
            if name == "torso_link" and env_data.torso_quat is not None:
                return np.asarray(env_data.torso_quat, dtype=np.float32)
        # Pelvis / root body -- always available as base_quat
        return np.asarray(env_data.base_quat, dtype=np.float32)

    def get_action(self, obs):
        return self._stashed_pd_targets

    def get_init_dof_pos(self):
        return self._player.get_state_at_frame(0)["dof_pos"].copy()
