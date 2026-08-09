# Milestone 4 — Torque Actuation and Basic Joint Control

## Objective

Implement basic torque-based actuation and closed-loop joint control for the accepted Chrono AI Excavator mechanical architecture.

Control exactly these four joints:

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

Each joint must follow a small deterministic target-angle trajectory using bounded commanded torque.

This milestone proves:

> target joint trajectory → feedback controller → bounded actuator torque → Project Chrono mechanical motion

This milestone does not implement excavation behavior.

Do not add contacts, dynamic cubes, scoop/dump logic, telemetry/HUD, additional cameras, or video.

---

# Canonical project rule

Proceed strictly according to the agreed plan.

Do not introduce:

* side tasks;
* unrelated cleanup;
* speculative refactoring;
* future-milestone functionality;
* additional features;
* additional audits beyond those explicitly required here.

If an unexpected repository condition, PyChrono incompatibility, or design issue requires work outside this specification:

STOP.

Report the exact issue.

Do not broaden the task without explicit project-owner approval.

Project priority:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/joint-actuation-control`

Expected starting HEAD:

`a7387212e6797651003b12a351afa2e394918afd`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Accepted mechanical baseline

Milestone 3 is complete and frozen as the mechanical reference.

Primary bodies:

* `BASE`
* `UPPER`
* `BOOM`
* `STICK`
* `BUCKET`

Mechanical topology:

* `J0_SLEW`: `BASE ↔ UPPER`
* `J1_BOOM`: `UPPER ↔ BOOM`
* `J2_STICK`: `BOOM ↔ STICK`
* `J3_BUCKET`: `STICK ↔ BUCKET`

Accepted axes:

* `J0_SLEW` ≈ scene Y
* `J1_BOOM` = scene Z
* `J2_STICK` = scene Z
* `J3_BUCKET` = scene Z

Do not change:

* five-body topology;
* pivot locations;
* accepted joint-axis directions;
* visual geometry;
* masses/inertias except if an actual blocking invalid value is discovered, in which case STOP rather than silently changing it.

---

# Actuation architecture

## 1. Torque motors

Create the actuated model using:

`ChLinkMotorRotationTorque`

for the four controlled axes.

The installed PyChrono API must be probed when necessary rather than assuming signatures.

Rotational motors use the motor-frame local Z axis as their spindle axis.

A rotational motor normally embeds its own revolute spindle constraint.

Therefore, in the actuated model:

> Do not stack a `ChLinkMotorRotationTorque` on top of an existing `ChLinkLockRevolute` for the same joint.

That would duplicate mechanical constraints.

Instead, create exactly four torque-motor links that reproduce the accepted revolute topology and axes:

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

The accepted Milestone 3 `mechanical_scene.py` must remain a valid independent reference model with its existing revolute joints.

Do not convert or break the frozen mechanical-scene viewer/tests.

---

# 2. Controlled-scene implementation

Create:

`src/chrono_ai_excavator/controlled_scene.py`

The controlled scene should reuse the accepted geometry/mechanical definitions where practical.

A small non-breaking extraction or helper reuse from `mechanical_scene.py` is allowed only if genuinely required to avoid duplicating the entire scene.

Do not perform a broad refactor.

If reuse requires substantial architectural restructuring:

STOP and report it.

The controlled scene must contain:

* the same five primary mechanical bodies;
* the same environment;
* the same 30 fixed cubes;
* the same container;
* the same accepted initial pose;
* exactly four rotational torque motors;
* no separate duplicate revolute constraints on those same four axes.

---

# Controller

## 3. Basic PD torque control

Use a simple bounded PD controller for each joint.

Controller law:

```text
tau_raw =
    Kp * (theta_ref - theta)
  + Kd * (omega_ref - omega)

tau_cmd = clamp(tau_raw, -tau_max, +tau_max)
```

Where:

* `theta_ref` = target joint angle;
* `theta` = actual motor angle;
* `omega_ref` = target angular velocity;
* `omega` = actual motor angular velocity;
* `Kp` = proportional gain;
* `Kd` = derivative gain;
* `tau_max` = actuator torque limit.

No integral term.

No PID.

No feed-forward.

No gravity compensation.

---

# 4. Torque application

Use the simplest installed-binding-compatible way to update commanded motor torque each simulation step.

Prefer `ChFunctionSetpoint` if it is available and behaves correctly in the installed PyChrono binding.

The intended usage is:

* one externally updated torque value per motor;
* update once per simulation step;
* torque remains constant between updates.

If the installed binding requires another simple supported `ChFunction` mechanism, use it only after minimal API probing.

Do not implement a custom framework.

---

# 5. Motor state

Use the torque motor’s own rotation state where available:

* motor angle;
* motor angular velocity.

Do not estimate joint angle from body positions.

Do not reconstruct joint velocity by finite differences if the motor API provides it directly.

The controller must operate in radians and radians/second.

Human-readable output may additionally display degrees.

---

# Reference trajectories

## 6. Initial angle reference

The accepted ready-to-scoop pose is the zero-reference pose for this milestone.

Target trajectories should therefore be defined as small relative motor-angle changes from the initialized pose.

Do not redefine the accepted absolute geometry.

---

## 7. Smooth trajectory

Use a deterministic smooth cubic transition:

```text
s(u) = 3u² - 2u³
```

for:

`0 ≤ u ≤ 1`

with:

`u = t / T`

and analytic reference angular velocity.

Before the trajectory:

* target delta = 0

After the trajectory:

* hold the final target angle.

Use:

`T = 1.0 s`

for the basic transition.

---

## 8. Demonstration target deltas

Use these small relative target changes:

* `J0_SLEW`: `+12°`
* `J1_BOOM`: `+8°`
* `J2_STICK`: `-8°`
* `J3_BUCKET`: `+10°`

Convert to radians internally.

These are demonstration targets only.

They are not physical travel limits.

Do not add joint limits in this milestone.

---

# Controller parameters

## 9. Gain and torque policy

Use deterministic toy-model controller parameters.

Select one `Kp`, `Kd`, and `tau_max` set per joint based on the existing placeholder masses/inertias and the small target trajectories.

Requirements:

* values must be explicitly stored;
* units must be documented;
* torque must always be saturated by `tau_max`;
* values must be clearly marked as demonstrator/controller placeholders;
* no claim of real excavator calibration.

Minimal local tuning is allowed only to make the prescribed bounded zero-gravity tests work.

Do not perform optimization.

Do not run parameter sweeps.

Do not tune for realistic hydraulics.

If a reasonable small deterministic parameter set cannot satisfy the acceptance criteria without extensive tuning:

STOP and report it.

---

# Dynamics configuration

## 10. Gravity

Use zero gravity in Milestone 4.

Purpose:

isolate actuator and feedback-controller behavior from:

* gravity compensation;
* contact;
* payload;
* hydraulic modeling.

Do not enable gravity merely to make the demonstration more realistic.

Gravity-loaded control belongs to a later stage.

---

## 11. Contacts and environment

Retain:

* platform;
* 30 cubes;
* container.

But:

* cubes remain fixed;
* container remains fixed;
* no contact response;
* no bucket/cube interaction;
* no collision tuning.

---

# Required implementation

## 12. Controlled-scene API

`controlled_scene.py` should expose a focused API for:

* building the actuated scene;
* accessing the five primary bodies;
* accessing the four torque motors;
* accessing four controller configurations;
* computing smooth target angle and velocity;
* computing bounded PD torque;
* advancing one controlled step;
* running a bounded headless control scenario;
* returning deterministic result metadata.

Do not create a generic robotics/control framework.

---

## 13. Controller metadata

For each joint expose at least:

* joint name;
* connected body names;
* axis;
* `Kp`;
* `Kd`;
* `tau_max`;
* target delta;
* trajectory duration.

For headless results expose at least:

* initial angle;
* target angle;
* final angle;
* final angle error;
* peak absolute commanded torque;
* maximum allowed torque;
* finite-state status.

---

# Automated joint-control verification

## 14. Independent joint tests

Run each controlled joint independently.

For each test:

* start from the accepted initial pose;
* zero gravity;
* all initial velocities zero;
* command one joint to its prescribed target;
* other three controllers hold zero-reference targets;
* simulate long enough for the target transition and short settling period.

Use a deterministic fixed timestep.

Choose a simple timestep appropriate for the existing model.

Do not optimize it.

---

## 15. Required acceptance criteria

For each joint:

1. simulation remains finite;
2. commanded joint moves in the intended direction;
3. final joint angle is closer to target than initial joint angle;
4. final target error is no greater than:

   * `1.5°`
5. absolute commanded torque never exceeds:

   * `tau_max + numerical tolerance`
6. non-commanded joints remain within:

   * `0.5°`
     of their zero-reference targets;
7. no constraint explosion occurs;
8. no motor/revolute duplicate constraint exists.

If a prescribed joint cannot meet these requirements after a small local controller adjustment:

STOP and report it.

Do not weaken the acceptance criteria.

---

# 16. Combined control smoke test

After all four independent tests pass, run one short combined zero-gravity scenario where all four joints follow their prescribed smooth target trajectories simultaneously.

Verify:

* finite states;
* all four joints move toward their targets;
* torque limits respected;
* no solver failure.

This is not the excavation sequence.

It is only a combined control smoke test.

---

# Interactive viewer

## 17. Viewer script

Create:

`scripts/show_controlled_scene.py`

Default interactive behavior:

* open Irrlicht;
* retain the accepted external scene composition;
* run one smooth transition from the initial pose to the four-joint demonstration target pose;
* hold the final pose;
* allow normal camera interaction;
* do not loop an endless repetitive motion by default.

The visual result should clearly demonstrate that all four joints can be actuated.

Do not add:

* HUD;
* torque arrows;
* active-joint colors;
* graphs;
* bucket camera;
* cabin camera.

Those remain future work.

---

## 18. Viewer options

Support:

```text
python scripts/show_controlled_scene.py --headless-check
```

This must run:

* the four independent joint-control checks;
* the combined control smoke test;
* no Irrlicht window.

Also support, if simple to implement without expanding architecture:

```text
python scripts/show_controlled_scene.py --joint J1_BOOM
```

to visually exercise one selected joint.

If this option would require meaningful extra architecture, omit it.

The default four-joint visual transition is mandatory.

---

# Tests

## 19. Automated tests

Create:

`tests/test_controlled_scene.py`

Keep all existing tests.

Cover at least:

* five-body controlled topology;
* exactly four torque motors;
* exact motor names;
* correct body connectivity;
* correct motor axes;
* absence of duplicate revolute constraints in controlled scene;
* torque-controller configuration validity;
* positive `Kp`;
* non-negative `Kd`;
* positive `tau_max`;
* correct target deltas;
* smooth trajectory endpoint values;
* bounded torque saturation;
* motor angle/state remains finite;
* each independent joint moves toward target;
* each independent final error ≤ `1.5°`;
* non-commanded joints stay within `0.5°`;
* torque limits are never exceeded;
* combined four-joint control smoke test passes;
* 30 fixed cubes retained;
* no contacts introduced;
* deterministic metadata.

Tests must be display-free.

Do not weaken Milestone 3 tests.

---

# Tracking

## 20. Record missing final Milestone 3 closeout action

Add, if absent:

* event_id: `M3-FINAL-CLOSEOUT-COMMIT-PUSH-001`
* milestone: `M3`
* started_at: `2026-08-09T11:41:22+03:00`
* ended_at: `2026-08-09T11:41:24+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Committed and pushed the final Milestone 3 merge-closeout documentation on main.`
* human_active_minutes: `0.03`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `Git commit a7387212e6797651003b12a351afa2e394918afd`
* estimate_quality: `measured`
* notes:
  `Local and remote main were verified at the same commit. Network time is not simulation or computation time.`

Do not modify other M3 records.

---

## 21. Record Milestone 4 branch creation

Add, if absent:

* event_id: `M4-BRANCH-CREATION-001`
* milestone: `M4`
* started_at: `2026-08-09T11:45:46+03:00`
* ended_at: `2026-08-09T11:45:48+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Created and published the Milestone 4 joint-actuation-control feature branch from the fully closed Milestone 3 main branch.`
* human_active_minutes: `0.03`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `/tmp/chrono_ai_excavator_step_08a_create_m4_branch.txt and starting commit a7387212e6797651003b12a351afa2e394918afd`
* estimate_quality: `measured`
* notes:
  `Local and remote feature/joint-actuation-control branches were verified at the same starting commit.`

Preserve LF line endings.

---

# 22. Measure this Codex task

At the beginning of execution, before modifying project files:

* capture an actual ISO-8601 start timestamp using the system clock.

At the end, after successful prescribed verification:

* capture an actual ISO-8601 end timestamp;
* calculate task wall-clock seconds.

Record one event:

* event_id: `M4-CODEX-ACTUATION-001`
* milestone: `M4`
* activity_category: `codex_development`
* actor: `codex`
* tool: actual Codex CLI/version and `gpt-5.6-sol`
* description:
  `Implemented Milestone 4 torque actuation and basic bounded joint control.`
* human_active_minutes: empty
* ai_wall_seconds: measured task wall-clock seconds
* compute_wall_seconds: empty
* iteration_type: `initial`
* ai_result_status: `pending_review`
* estimate_quality: `measured`
* evidence:
  `prompts/013_milestone_4_joint_actuation_control.md and Codex task transcript`

Do not infer timing from Git or file timestamps.

---

# 23. Measure simulation wall time

For the prescribed headless control validation, measure actual wall-clock time spent inside the controlled simulation loops.

Do not include:

* imports;
* test discovery;
* documentation;
* Git operations.

Add or expose the measured simulation wall time in the headless result.

Record one computation event only after successful verification:

* event_id: `M4-CONTROL-SIMULATION-001`
* milestone: `M4`
* activity_category: `simulation`
* actor: `project_chrono`
* tool: `Project Chrono / PyChrono`
* description:
  `Executed the Milestone 4 independent-joint and combined zero-gravity control validation simulations.`
* human_active_minutes: empty
* ai_wall_seconds: empty
* compute_wall_seconds: actual measured simulation-loop wall seconds
* iteration_type: `initial`
* ai_result_status: `accepted`
* estimate_quality: `measured`
* evidence:
  `scripts/show_controlled_scene.py --headless-check`

Do not artificially inflate this duration.

---

# Documentation

## 24. README

Update `README.md` minimally.

State:

* Milestone 3 remains complete;
* Milestone 4 is in progress;
* four torque-actuated joints are implemented;
* bounded PD control is implemented;
* small deterministic target trajectories are implemented;
* headless joint-control verification is available;
* human interactive review remains pending.

Clearly state that these are still not implemented:

* contacts;
* dynamic cubes;
* scoop/dump cycle;
* excavation state machine;
* telemetry/HUD;
* active-joint visualization;
* bucket camera;
* cabin camera;
* final video.

Do not mark Milestone 4 complete.

---

## 25. Technical report

Update:

`docs/technical_report.md`

Document:

* Milestone 4 objective;
* torque-motor architecture;
* why the controlled scene must not duplicate revolute constraints;
* PD control law;
* saturation;
* target trajectory;
* zero-gravity isolation rationale;
* controller parameters and units;
* independent joint-control validation;
* combined control smoke test;
* measured simulation wall time;
* current limitations.

State:

> Milestone 4 actuation and basic joint control are implemented and awaiting human review.

Do not describe contacts or excavation behavior as implemented.

---

# 26. Preserve this task

Save this full specification as:

`prompts/013_milestone_4_joint_actuation_control.md`

Do not alter prompts 001 through 012.

---

# Verification

Run only these checks, in order:

```text
python scripts/check_environment.py
python scripts/show_mechanical_scene.py --headless-check
python scripts/show_controlled_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

If a check fails:

STOP at that failure.

Report it.

Do not automatically expand the task into an unrelated repair.

A narrow binding/API correction directly required by the failed Milestone 4 implementation must still be reported before changing scope.

Do not open Irrlicht during automated verification.

---

# Strict scope exclusions

Do not implement:

* contacts;
* contact materials;
* collision response;
* dynamic cubes;
* bucket/cube interaction;
* cube/cube interaction;
* gravity compensation;
* realistic hydraulics;
* hydraulic cylinders;
* integral control;
* PID;
* feed-forward control;
* path planning;
* excavation state machine;
* scoop/dump sequence;
* joint limits;
* telemetry;
* HUD;
* active-joint colors;
* torque arrows;
* plots;
* bucket-mounted camera;
* cabin camera;
* camera animation;
* screenshot automation;
* PDF;
* presentation;
* video;
* FFmpeg;
* CI;
* new dependencies;
* CAD;
* external meshes;
* performance optimization;
* unrelated refactoring;
* branch switch;
* commit;
* push.

---

# Completion report

Report only:

1. files created or modified;
2. controlled-scene architecture;
3. how duplicate revolute constraints were avoided;
4. four torque-motor names and connectivity;
5. controller formula;
6. `Kp`, `Kd`, and `tau_max` for each joint;
7. target trajectory and target deltas;
8. independent result for each joint:

   * target;
   * final angle;
   * final error;
   * peak torque;
9. combined control smoke-test result;
10. measured simulation wall time;
11. mechanical baseline headless result;
12. controlled-scene headless result;
13. unittest count/result;
14. compilation result;
15. tracking-summary result;
16. `git diff --check` result;
17. branch, HEAD, and worktree status;
18. M3 final closeout ledger event status;
19. M4 branch event status;
20. measured M4 Codex task wall time;
21. items requiring human interactive review;
22. confirmation that Milestone 3 reference mechanics remain valid;
23. confirmation that no contacts, dynamic cubes, excavation state machine, telemetry/HUD, camera variants, PDF, presentation, or video were added;
24. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
