> ## Fork notice
>
> This is a fork of [HansZ8/RoboJuDo](https://github.com/HansZ8/RoboJuDo).
> **This branch (`main`) is the upstream mirror** — it carries no project code,
> only upstream plus this notice and the [G1 deployment
> runbook](#-g1-deployment-runbook-fork) below. Keep it that way so upstream can
> be merged in without conflicts.
>
> Project work lives on the feature branches:
>
> | Branch | What it adds |
> |---|---|
> | [`feature/protomotions-tracker`](../../tree/feature/protomotions-tracker) | ProtoMotions tracker deployment: reference-mode blending in the tracker policy, the `unitree_cpp` build patch. |
> | [`integration/all`](../../tree/integration/all) | All feature branches merged. **This is the branch to check out for day-to-day work.** |
>
> Land new work on the feature branch it belongs to and merge up — don't commit
> straight to `integration/all`.
>
> ```bash
> git remote add upstream https://github.com/HansZ8/RoboJuDo.git
> git fetch upstream && git checkout main && git merge upstream/release
> ```
>
> Upstream's default branch is `release`, not `main`.
>
> ### License
>
> `SPDX-License-Identifier: CC-BY-4.0`
>
> Upstream RoboJuDo is licensed under [Creative Commons Attribution 4.0
> International](https://creativecommons.org/licenses/by/4.0/), and this fork inherits those terms:
> redistribution and adaptation are permitted, including commercially, provided you give credit and
> indicate what you changed.
>
> Upstream's [`LICENSE`](LICENSE) file stated these terms in summary form. This fork replaces it with
> the full CC BY 4.0 legal text so the license is unambiguous and machine-detectable; the license
> itself is unchanged, and HansZ8's copyright line is preserved. This is the one file on `main` that
> intentionally diverges from upstream, so expect to keep the fork's version when merging upstream.

<div align="center">
<h1>RoboJuDo 🤖</h1>

*A plug-and-play deploy framework for robots. Just deploy, just do.*

<h3>
🔗 RoboJuDo is part of the FRoM-W1 project, check it out at 👉 
<a href="https://github.com/OpenMOSS/FRoM-W1">
  OpenMOSS / FRoM-W1
</a>
</h3>

<p>
  <!-- Version -->
  <a href="https://github.com/HansZ8/RoboJuDo/releases">
    <img src="https://img.shields.io/github/v/release/HansZ8/RoboJuDo?color=blue&label=version" alt="release"/>
  </a>
  <!-- Platforms -->
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Ubuntu-green" alt="platform"/>
  <!-- Multi-Robot -->
  <img src="https://img.shields.io/badge/robot-UnitreeG1%20%7C%20UnitreeH1%20%7C%20FFTAIgr1-orange" alt="multi-robot"/>
  <!-- Pre Commit -->
  <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white]" alt="pre-commit"/>
  <!-- License -->
  <a href="https://creativecommons.org/licenses/by-nc/4.0/">
    <img src="https://img.shields.io/badge/License-CC--BY--NC--4.0-lightgrey.svg" alt="license"/>
  </a>
</p>
<img src="docs/images/header-demo.gif" width="80%" alt="demo"/>
<br>
<br>
</div>


Tired of projects that release only models but no deployment code? RoboJuDo provides a unified framework that makes policy deployment straightforward and practical.

Our framework highlights:
- **Out-of-the-box**: After setting up RoboJudo, multiple policies can be deployed on both simulation and real robots in minutes: [Quick Start](#quick-start).

- **Decoupled & Modular Design**: With a Python-first design, RoboJuDo makes fast prototyping easy. Environment, Controller, and Policy are modular and freely composable, while minimal code changes allow seamless adaptation across robots and setups: See how we achieve this: [Add a new module](#add-a-new-module).

- **Multi-policy switching**: Seamlessly switch between different policies during a task. Try this: [Multi-Policy Switching](#multi-policy-switch).

- **Light-Weight**: Our framework is lightweight, after 5 minutes of setup, it runs smoothly onboard. By [UnitreeCpp](https://github.com/HansZ8/unitree_cpp), RoboJuDo runs on Unitree G1 without the need for an Ethernet cable.


# 📓Content
 - [📄Introduction](#introduction)
 - [🛠️Easy Setup](#%EF%B8%8Feasy-setup)
 - [📖Quick Start](#quick-start)
 - [🤸 G1 Deployment Runbook (fork)](#-g1-deployment-runbook-fork)
 - [🧩 Develop and Contribute](#develop-and-contribute)


# 🗺️Roadmap

> **2026.03 Update**: We added built-in support for deploying the [ProtoMotions](https://github.com/NVlabs/ProtoMotions) G1 tracker in RoboJuDo. Thanks to [NVLabs](https://github.com/NVlabs) for the great work on ProtoMotions, and thanks to [Chen Tessler](https://github.com/tesslerc) and [Yifeng Jiang](https://github.com/jyf588) for contributing this integration.


<table>
<tr>
<td width="80%">

- [x] [2025.04] Initialized project
- [x] [2025.05] Add support for Unitree G1
- [x] [2025.05] Add support for Unitree H1, FFTAI Gr1T1
- [x] [2025.06] Integrated Unitree C++ SDK
- [x] [2025.08] Add support for beyondmimic
- [x] [2025.09] RoboJuDo Opensource 🎉
- [x] [2025.10] Add support for **ASAP**
  - [x] Implement `deepmimic` and `locomotion`, check [AsapPolicy](./docs/policy.md/#policy--asappolicy)!
  - [x] Preserve original keyboard and joystick mappings
  - [x] Support for **KungfuBot**
- [x] Add policy-switch pipeline with interpolation, check [LocoMimic Example](#loco-mimic-policy-switch-with-interpolation)!
- [x] [2025.11] Add support for **KungfuBot2** , check [KungfuBotGeneralPolicy](./docs/policy.md/#policy--kungfubotgeneralpolicy)!
- [x] [2025.11] Add support for **TWIST** , check [TwistPolicy](./docs/policy.md/#policy--twistpolicy)!
- [x] [2026.03] Add support for **ProtoMotions** ✨, check [ProtoMotions Tracker](#protomotions-tracker) and [ProtoMotionsTrackerPolicy](./docs/policy.md/#policy--protomotionstrackerpolicy)!
- [ ] Release code for **HugWBC**
- [ ] Release code for **GMT**
- [ ] Upcoming policies...

 

</td>
<td width="20%">

<div align="center">
<img src="docs\images\job.gif" alt="working" width="100%" >
</div>

</td>
</table>

# 📄Introduction

This repository provides a deployment framework for humanoid robots, supporting the use of different policies across different environments (real robots and simulation).  
We decouple the **controller**, **environment**, and **policy**, making it easy for users to add their own policies or environments.  
Experiment configurations can be organized through config files.

The main modules of **RoboJuDo** consist of:

- 🎮 **Controller**: A collection of control signals. It receives external inputs (e.g., joystick, keyboard, motion sequences) and forwards them as `ctrl_data` to the pipeline.  
- 🤖 **Environment**: The execution environment (e.g., Mujoco, real robot). It processes actions provided by the policy and sends real-time sensor data as `env_data` to the pipeline.  
- 🌐 **Policy**: A trained control policy (from various wbc & locomotion works). It generates actions based on information from both the environment and the controller.

Currently, **RoboJuDo** supports the following policy–environment combinations:


<div align="center">
<!-- 
|  | Human2Humanoid | AMO | GMT | HugWBC | BeyondMimic| ... |
|:-------:|:--------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| g1 mujoco | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ... |
| g1 real | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ... |
| h1 mujoco | ✔️ | ❎ | ❎ | ✔️ | ✔️ | ... |
| h1 real | ✔️ | ❎ | ❎ | ✔️ | ❎ |... |
| gr1t1 mujoco | ✔️ | ❎ | ❎ | ❎ | ❎ | ... |
| gr1t1 real | ❎ | ❎ | ❎ | ❎ | ❎ | ... | -->

| Policy | Unitree G1 | Unitree H1 | FFTAI gr1t1 | Ref | Doc | Feature & Note |
|:-------:|:--------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| Unitree Official | 🖥️ 🤖 | 🖥️ 🤖 | - | [unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym) | [UnitreePolicy](./docs/policy.md/#policy--unitreepolicy)|  |
| Unitree Wo Gait | 🖥️ 🤖 | - | - | [unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab) | [UnitreeWoGaitPolicy](./docs/policy.md/#unitreewogaitpolicy)| no gait |
| Human2Humanoid | 🖥️ 🤖 | 🖥️ 🤖 | 🖥️ | [H2H](https://github.com/LeCAR-Lab/human2humanoid) | [H2HStudentPolicy](./docs/policy.md/#policy--h2hstudentpolicy) | Need PHC submodule |
| Smooth | 🖥️ 🤖 | 🖥️ 🤖 | 🖥️ 🤖⚠️ | [Smooth](https://github.com/zixuan417/smooth-humanoid-locomotion) |  |
| AMO | 🖥️ 🤖 | - | - | [AMO](https://github.com/OpenTeleVision/AMO) | [AmoPolicy](./docs/policy.md/#policy--amopolicy) |  |
| GMT | 🖥️ 🤖 | - | - | [GMT](https://github.com/zixuan417/humanoid-general-motion-tracking) |  |  |
| HugWBC | 🖥️ 🤖 | 🖥️ 🤖 | - | [HugWBC](https://github.com/apexrl/HugWBC) | [HugWbcPolicy](./docs/policy.md/#policy--hugwbcpolicy) |  |
| **BeyondMimic** | 🖥️ 🤖 | - | - | [whole_body_tracking](https://github.com/HybridRobotics/whole_body_tracking) | [BeyondmimicPolicy](./docs/policy.md/#policy--beyondmimicpolicy) | With&Wo SE supported |
| **ASAP** | 🖥️ 🤖 | - | - | [ASAP](https://github.com/LeCAR-Lab/ASAP) | [AsapPolicy](./docs/policy.md/#policy--asappolicy) | deepmimic & locomotion supported |
| KungfuBot<br>**KungfuBot2** | 🖥️ 🤖 | - | - | [PBHC](https://github.com/TeleHuman/PBHC) | [AsapPolicy](./docs/policy.md/#policy--asappolicy)<br>[KungfuBotGeneralPolicy](./docs/policy.md/#policy--kungfubotgeneralpolicy) | Need PHC submodule |
| **TWIST** | 🖥️ 🤖 | - | - | [TWIST](https://github.com/YanjieZe/TWIST) | [TwistPolicy](./docs/policy.md/#policy--twistpolicy) |  |
| **ProtoMotions** | 🖥️ 🤖 | - | - | [ProtoMotions](https://github.com/NVlabs/ProtoMotions) | [ProtoMotionsTrackerPolicy](./docs/policy.md/#policy--protomotionstrackerpolicy) | [nvlab doc](https://nvlabs.github.io/ProtoMotions/tutorials/workflows/g1_deployment.html) |
| ... | ... | ... | ... | ... | ... | ... |
</div>

🖥️ means policy is ready for simulation, while 🤖 means policy has been tested on real robot.


<!-- Refer [Deploy Policy](#amo-policy-for-g1) for usage. -->


# 🛠️Easy Setup

RoboJuDo supports **multiple platforms**, officially tested on **Ubuntu**, **macOS**and **Windows**. 

Robot onboard PCs are also supported.


## 1️⃣ Basic Installation

**Step 1: Clone the repository and create a Python environment**

```bash
git clone https://github.com/HansZ8/RoboJuDo.git
cd RoboJuDo/
# Example using conda
conda create -n robojudo python=3.11 -y
conda activate robojudo
```
**Step 2: Install RoboJuDo**

```bash
# Optional, install cpu version for speed up
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e .
```

## 2️⃣ Install Optional Modules

RoboJuDo is a **plug-and-play framework**. After a minimal default installation, you can selectively configure and install only the modules you need.

---

**Step 0: \[Optional\] Install Robot SDK**

> *You can skip this for sim2sim and development.*

If you plan to control a real robot, install the corresponding SDK.

For example, see [unitree_setup.md](docs/unitree_setup.md) for Unitree robots.

---

**Step 1: Configure modules**

Edit [submodule_cfg.yaml](./submodule_cfg.yaml) to select modules, by setting `install` as `true`.

> As default, `mujoco_viewer` is selected for sim2sim.

**Step 2: Install modules**

```bash
# Install all required modules
python submodule_install.py

# Or specify modules to install with args
# python submodule_install.py unitree_cpp
```

# 📖Quick Start

`RoboJuDo` is a modular framework where tasks can be flexibly defined by composing configuration files.  
In the following, we use the deployment on G1 as an example.

<!-- 😎For module combinations, we provide ready-to-use config files that can be directly applied.  -->
1. [Run Sim2Sim](#run-robojudo-on-simulation)
2. [Run Sim2Real](#run-robojudo-on-real-robot-🤖)
3. [Deploy More Policies✨](#deploy-more-policies)

## Run RoboJuDo on Simulation

Begin your journey with unitree g1 sim2sim.

> A Xbox controller is needed for control.

```bash
# run the default g1 sim2sim cfg
python scripts/run_pipeline.py
```

You can control the motivation using any Xbox controller:

- `left axes` move forward/backward/lfet/right
- `right axes` turn left/right

<!-- Or a keyboard:

- `wsad` move forward/backward/left/right
- `qe` turn left/right -->

<!-- For cooler policy, run:

```bash
python scripts/run_pipeline.py -c g1_beyondmimic
```
You can control the simulation environment using the Keyboard:

- `shift + <` start the motion play
- `shift + >` pause the motion play
- `shift + |` reset the motion progress
- `~` button: reset robot. -->

## Run RoboJuDo on Real Robot 🤖

### Alert & Disclaimer ⚠️⚠️⚠️
> Before deployment, you'd better first purchase accident insurance to cover any potential incidents that may occur during real-world operation. Policies could cause ⚠️**violent motions**⚠️ when losing balance. Always verify that the emergency stop button (e.g., **A** for default config) works properly.

> Unless you have strong sim-to-real expertise and rigorous safety measures, **DO NOT run these models on real robots**. They are provided for research only, and we disclaim any responsibility for harm, loss, or malfunction.

### Robot Setup

Follow our [setup guide](./docs/unitree_setup.md) to set up the robot sdk on your computer or robot.

### Start RoboJuDo

Open [`g1_cfg.py`](robojudo/config/g1/g1_cfg.py) and modify the `g1_real` config.

Edit the `env_type` and `net_if` according to your robot sdk setup.

```python
class g1_real(g1):
    env: G1RealEnvCfg = G1RealEnvCfg(
        env_type="UnitreeEnv",  # For unitree_sdk2py
        # env_type="UnitreeCppEnv",  # For unitree_cpp, check README for more details
        unitree=G1UnitreeCfg(
            net_if="eth0",  # note: change to your network interface
        ),
    )
```

Refer to [official guide](https://github.com/unitreerobotics/unitree_rl_gym/blob/main/deploy/deploy_real/README.md#startup-process) to prepare and start the robot.

Then start the pipeline on the real robot:

```bash
python scripts/run_pipeline.py -c g1_real
```

Your robot should move into default pos. 
**During the preparation, put your robot on the ground.**

You can control the real robot using the Unitree controller:
- `A` button: Emergency stop. The robot immediately switches to damping mode. Be careful.
- `left axes` move forward/backward/let/right
- `right axes` turn left/right

## Deploy More Policies

💡Now you’re familiar with RoboJuDo’s config design, it’s time to experience the **amazing variety of policies**!

### BeyondMimic & ASAP

Try the out of box experience of **BeyondMimic** and **ASAP**:

```bash
python scripts/run_pipeline.py -c g1_beyondmimic
python scripts/run_pipeline.py -c g1_asap
```

check documentation [BeyondmimicPolicy](./docs/policy.md/#policy--beyondmimicpolicy) and [AsapPolicy](./docs/policy.md/#policy--asappolicy) for more details.

### Multi-Policy Switch
`g1_switch` config in [g1_cfg.py](robojudo/config/g1/g1_cfg.py) is equipped with Multi-Policy Pipeline.

```bash
python scripts/run_pipeline.py -c g1_switch
```

Xbox Controller:

- `left axes` move forward/backward/left/right
<!-- - `right axes(for/back)` stand higher/squat -->
- `right axes(left/right)` turn left/right

Switch between Unitree Policy and AMO Policy:
- `RB + Dpad[Down]` switch to Unitree Policy
- `RB + Dpad[Up]` switch to AMO Policy

### Loco-Mimic Policy Switch with Interpolation

For deploying **Motion Mimic Policies** with **Locomotion** as backup, we built [LocoMimicPipeline](robojudo/pipeline/rl_loco_mimic_pipeline.py) for multi-policy switching with interpolation, 

Check `g1_locomimic` config in [g1_cfg.py](robojudo/config/g1/g1_cfg.py), and more fancy locomimic configs in [g1_loco_mimic_cfg.py](robojudo/config/g1/g1_loco_mimic_cfg.py).

```bash
python scripts/run_pipeline.py -c g1_locomimic_beyondmimic
python scripts/run_pipeline.py -c g1_locomimic_asap
```

We have the same Keyboard control as ASAP:
- `[` to switch to MotionMimic
- `]` to switch to LocoMotion
- `;` toggle next mimic policy
- `'` toggle prev mimic policy

<div align="center">
<img src="docs/images/locomimic_asap.gif" width="20%" alt="locomimic_asap"/>
</div>

### More Policies

We also provide config files for other policies, check [config_g1](robojudo/config/g1) and [config_h1](robojudo/config/h1) for more details.

#### ASAP
In RoboJuDo, we have fully replicated ASAP’s Sim2Real workflow, including all motions. 
Please refer to `g1_locomimic_asap_full` in [g1_loco_mimic_cfg.py](robojudo/config/g1/g1_loco_mimic_cfg.py). This highlights the modular advantages of our framework.

#### ProtoMotions Tracker
Please first follow the official workflow from [NVLabs / ProtoMotions](https://nvlabs.github.io/ProtoMotions/tutorials/workflows/g1_deployment.html) and clone the `ProtoMotions` repo as a sibling directory named `protomotions`.

Then you can run the built-in RoboJuDo config directly:

```bash
python scripts/run_tracker_pipeline.py -c g1_protomotions_tracker \
  --motion-path assets/motions/g1/g1_bones_seed_mini.pt \
  --motion-index 0
```

For more details, check [ProtoMotionsTrackerPolicy](./docs/policy.md/#policy--protomotionstrackerpolicy).


# 🤸 G1 Deployment Runbook (fork)

*Fork-only section — the operational procedure for deploying a ProtoMotions
tracker policy onto a real Unitree G1, written up from repeated hardware
sessions. Upstream does not carry this.*

Notation used below:

| Placeholder | Meaning |
|---|---|
| `$ROBOJUDO` | your clone of this repository |
| `$PROTOMOTIONS` | your ProtoMotions checkout, where policies are trained |
| `$NET_IF` | the host network interface facing the robot (`ip -br addr` to find it) |
| `<clip>` | motion name; `<clip>-bm-deploy` is its deploy-tracker experiment |

```bash
cd $ROBOJUDO
conda activate robojudo
```

## Prerequisites per motion

Both artifacts are produced on the ProtoMotions side:

1. `$PROTOMOTIONS/results/<clip>-bm-deploy/compiled_models/unified_pipeline.onnx`
   — an exported **deploy-tracker fine-tune**. Plain `mlp.py` policies use a
   privileged full-state actor and can **not** be deployed.
2. `<clip>.50fps.pt` — a 50 Hz motion cache, written by ProtoMotions'
   `deployment/test_tracker_mujoco.py --cache-motion`.

## Host setup (once per machine)

```bash
python -c "from robojudo.environment import UnitreeCppEnv"   # SDK OK if this is silent
ip -br addr                       # find $NET_IF; give it an address on 192.168.123.0/24
ping -c 2 192.168.123.161         # the G1 onboard PC should answer
```

- Set `net_if` in the `g1_protomotions_tracker_real` config
  (`robojudo/config/g1/g1_cfg.py`) to `$NET_IF`. It ships as `eth0`.
- **Firewall:** DDS multicast must be allowed on the robot-facing interface —
  `sudo ufw allow in on $NET_IF`. Re-apply if ufw is ever reset. The symptom
  when it is missing is distinctive: ping succeeds but RoboJuDo reports
  `Low state data is not available`.
- Bundled reference assets, useful as known-good baselines: the pretrained
  NVIDIA tracker at `assets/models/g1/protomotions_tracker/unified_pipeline.onnx`
  (the default when `--onnx-path` is omitted) and the 58-motion library
  `assets/motions/g1/g1_bones_seed_mini.pt` — index **16** is idle, **19** a
  short walk, **0** a jump-360. Never use index 0 as a first test.

## Robot startup ritual (every session)

1. Hang the robot in the gantry, feet off the ground. Power on and **wait ~1
   minute for a full boot**, until it reaches **zero-torque mode** — the joints
   go loose, wiggle a limb to confirm.
2. On the Unitree remote press **L2 + R2** for debug mode. The joints switch to
   damping and the built-in controller is suspended.
3. Only then start the pipeline.

Two log-reading notes: the self-check window is only about 3 seconds, so a
failed start is always worth one plain retry; and
`Motion control service shutdown successfully` is printed even with no robot
connected, so it means nothing on its own.

## Deploying a motion (escalation ladder)

Each rung tests exactly one new thing. Rungs 1 and 2 use the known-good
pretrained policy and only need repeating after a hardware or setup change, not
for every motion.

```bash
# 0. Sim rehearsal of your motion — no robot, MuJoCo viewer.
python scripts/run_tracker_pipeline.py -c g1_protomotions_tracker \
    --onnx-path $PROTOMOTIONS/results/<clip>-bm-deploy/compiled_models/unified_pipeline.onnx \
    --motion-path <path>/<clip>.50fps.pt

# 1. Real robot, known-good policy, idle — validates the whole hardware chain.
python scripts/run_tracker_pipeline.py -c g1_protomotions_tracker_real \
    --motion-path assets/motions/g1/g1_bones_seed_mini.pt --motion-index 16

# 2. Real robot, known-good policy, walk.
python scripts/run_tracker_pipeline.py -c g1_protomotions_tracker_real \
    --motion-path assets/motions/g1/g1_bones_seed_mini.pt --motion-index 19

# 3. Real robot, your policy and your motion.
python scripts/run_tracker_pipeline.py -c g1_protomotions_tracker_real \
    --onnx-path $PROTOMOTIONS/results/<clip>-bm-deploy/compiled_models/unified_pipeline.onnx \
    --motion-path <path>/<clip>.50fps.pt
```

## Operator flow during a run

Ramp-up (3 s) and the policy blend (5 s) run automatically once the script
starts. The robot then holds its default pose and waits for a trigger.

**On the real robot, use the Unitree remote only, and press each button
alone.** The keyboard bindings are simulation-only — the `press R` line in the
log is for sim. Holding L1 or R1 changes the trigger lookup key and swallows
the command; the vibration on L1+R1 is Unitree firmware and can be ignored.

| Button | Action |
|---|---|
| **Y** | start / reset motion |
| **X** | blend in |
| **B** | blend out |
| **A** | emergency shutdown — plain `A`, takes effect instantly |

In simulation the equivalents are `r` reset, `i` respawn, `<` fade-in,
`>` fade-out, `o` shutdown.

Gantry flow: start the script while the robot hangs → let ramp and blend finish
→ lower the gantry until the feet take the load → **Y** to start the motion →
**B** when it is done → raise the gantry.

- Three ways out, in order of reach: **A** on the remote, Ctrl-C in the
  terminal, the gantry itself.
- Know the risky moments before you run. Trace the final checkpoint with
  ProtoMotions' `scripts/mujoco_rollout_trace.py` and note where tracking error
  and balance margin are tightest — keep the gantry line honest there.
- Clear floor space larger than the motion's footprint. Motions drift.

## Troubleshooting

**`Low state data is not available`** — the self check failed.

1. Redo the startup ritual and rerun the script; the self-check window is ~3 s.
2. The classic cause is the firewall: ping works but DDS is silent. Apply
   `sudo ufw allow in on $NET_IF`. To confirm the robot's DDS heartbeat without
   root, join multicast `239.255.0.1:7400` from a plain UDP socket and listen.
3. `sudo tcpdump -i $NET_IF -c 5 udp port 7400` — packets arriving from `.161`
   point at a receive-side problem on the PC; no packets at all points at the
   robot, meaning it is still booting or not in debug mode.

**Remote buttons ignored** — you are most likely holding L1 or R1; press the
button by itself. If plain buttons are also dead, check that lowstate is
flowing at all: the button states ride inside `lowstate.wireless_remote`.


# 🧩Develop and Contribute

## Add a new module

Refer to the documentation on [Policy](docs/policy.md), [Controller](docs/controller.md), [Env](docs/environment.md), create and deploy your own policy in minutes.

(By the way, deploying AMO takes only 30 minutes, and GMT about 1 hour in our framework.)

Or simply create an issue — we will include updates in future releases!

## Contribute to our project

We warmly welcome contributions from the community. Let’s build a strong and open ecosystem for RoboJuDo together!

# 🔗Citation

If you find our work useful, please cite our GitHub repository:

```bibtex
@misc{li2026fromw1generalhumanoidwholebody,
      title={FRoM-W1: Towards General Humanoid Whole-Body Control with Language Instructions}, 
      author={Peng Li and Zihan Zhuang and Yangfan Gao and Yi Dong and Sixian Li and Changhao Jiang and Shihan Dou and Zhiheng Xi and Enyu Zhou and Jixuan Huang and Hui Li and Jingjing Gong and Xingjun Ma and Tao Gui and Zuxuan Wu and Qi Zhang and Xuanjing Huang and Yu-Gang Jiang and Xipeng Qiu},
      year={2026},
      eprint={2601.12799},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2601.12799}, 
}

@misc{RoboJuDo,
  author = {Zihan Zhuang, Yi Dong, Peng Li},
  title = {A plug-and-play deploy framework for robots. Just deploy, just do.},
  url = {https://github.com/HansZ8/RoboJuDo},
  year = {2025}
}
```
or star our repo😁

# 🔗 Related Repo

- [Unitree SDK2 Python](https://github.com/unitreerobotics/unitree_sdk2_python): used for implementing `UnitreeEnv`.
- [PHC](https://github.com/ZhengyiLuo/PHC): used for implementing the `MotionCtrl` module for OmniH2O.
- [UnitreeCpp](https://github.com/HansZ8/unitree_cpp): our pybind of `unitree_sdk2` used in `UnitreeCppEnv`.
- [ZED Proxy](https://github.com/HansZ8/ZED-Proxy/): ZED Camera Odometry Service.
- [ProtoMotions](https://github.com/NVlabs/ProtoMotions): GPU-accelerated simulation and learning framework by NVLabs.
