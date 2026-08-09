# Milestone 4 — PD Holding and Settling Correction

## Objective

Perform one narrow corrective pass on the existing uncommitted Milestone 4 torque-control implementation.

The previous implementation correctly produced:

* bounded torque;
* correct motion direction;
* successful `J3_BUCKET` control;

but did not satisfy all fixed acceptance criteria for `J0_SLEW`, `J1_BOOM`, and `J2_STICK`.

This correction is explicitly authorized by the project owner.

Allowed corrective actions are limited to:

1. retuning PD gains;
2. using appropriately stronger/differentiated holding gains for non-commanded joints;
3. increasing the deterministic settling interval if required.

Do not change any acceptance criterion.

Do not change target angles.

Do not increase the defined torque limits.

Do not change mechanical architecture.

Do not add new functionality.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

This is one narrow correction pass only.

If the fixed criteria still cannot be met after a reasonable deterministic retuning within the allowed changes:

STOP and report the remaining failure.

Do not:

* weaken acceptance criteria;
* raise torque limits;
* redesign the controller;
* introduce integral action;
* modify mechanics;
* introduce contacts;
* expand the milestone.

Project priority:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/joint-actuation-control`

Expected committed base:

`a7387212e6797651003b12a351afa2e394918afd`

The worktree already contains the uncommitted Milestone 4 implementation from the previous Codex task.

Preserve that implementation.

Do not reset or recreate it.

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Previous control result

Latest independent-joint results:

## `J0_SLEW`

Target:

`+12°`

Final:

`+14.082°`

Final error:

`−2.082°`

Failure:

final error exceeds `1.5°`.

---

## `J1_BOOM`

Target:

`+8°`

Final:

`+8.994°`

Final error:

`−0.994°`

Own-joint error passes.

Maximum non-commanded joint deviation:

`1.475°`

Failure:

non-commanded deviation exceeds `0.5°`.

---

## `J2_STICK`

Target:

`−8°`

Final:

`−8.285°`

Final error:

`+0.285°`

Own-joint error passes.

Maximum non-commanded joint deviation:

`0.977°`

Failure:

non-commanded deviation exceeds `0.5°`.

---

## `J3_BUCKET`

Target:

`+10°`

Final:

`+10.001°`

Final error:

`−0.001°`

Maximum non-commanded deviation:

`0.091°`

Result:

PASS.

---

# Confirmed behavior

All observed peak commanded torques remained within the existing torque limits.

All commanded joints moved in the correct direction.

Therefore this correction must focus only on:

* damping/settling of `J0_SLEW`;
* holding performance of coupled non-commanded joints during `J1_BOOM` and `J2_STICK` tests.

---

# Fixed acceptance criteria

Do not modify these requirements.

For every independent joint-control test:

1. all states remain finite;
2. commanded joint moves in the intended direction;
3. final angle is closer to target than initial angle;
4. final target error ≤ `1.5°`;
5. absolute commanded torque ≤ existing `tau_max` plus numerical tolerance;
6. every non-commanded joint remains within `0.5°` of its zero-reference target;
7. no constraint explosion;
8. no duplicate motor/revolute constraints.

All four joints must pass.

---

# Fixed target trajectories

Do not change:

* `J0_SLEW`: `+12°`
* `J1_BOOM`: `+8°`
* `J2_STICK`: `−8°`
* `J3_BUCKET`: `+10°`

Trajectory transition duration remains:

`T = 1.0 s`

using the existing smooth cubic transition.

Do not change the trajectory shape.

---

# Fixed torque limits

Do not increase any existing `tau_max`.

The correction must work within the torque limits already implemented in:

`src/chrono_ai_excavator/controlled_scene.py`

If a torque limit itself is invalid, inconsistent, or not actually applied as intended:

STOP and report that as a separate defect.

Do not silently change it.

---

# Allowed correction 1 — PD gain retuning

You may retune:

* `Kp`
* `Kd`

for the existing four joint controllers.

Use deterministic values.

The goal is not realism.

The goal is stable bounded control of the current toy-model mechanism.

Prefer increasing damping before substantially increasing proportional gain when correcting overshoot.

Avoid excessive gains that cause:

* oscillation;
* torque saturation for most of the trajectory;
* numerical stiffness;
* coupling instability.

Do not run an optimization algorithm.

Do not run broad parameter sweeps.

A small number of deliberate local tuning iterations is allowed.

---

# Allowed correction 2 — holding gains

During an independent joint test:

* one joint follows its prescribed moving reference;
* the other three joints hold their zero-reference angles.

You may use different PD gains for:

* a joint that is actively following a moving reference;
* the same joint when it is acting as a zero-reference holding controller.

This is permitted only to improve non-commanded joint holding.

Keep the design simple.

Acceptable implementation:

* one normal/motion gain set per joint;
* one hold gain set per joint;

or an equivalently minimal deterministic implementation.

Do not create a general control-mode framework.

Do not add a state machine.

Do not alter torque limits between motion and holding modes.

---

# Allowed correction 3 — settling interval

The target transition duration remains:

`1.0 s`.

You may increase only the post-transition settling interval used for acceptance evaluation.

Keep it deterministic and reasonably short.

Suggested upper bound:

`2.0 s` of additional settling after the 1.0-second trajectory.

Do not extend simulation merely to hide persistent oscillations.

A valid solution should visibly converge.

Record the final selected settling duration.

---

# Required diagnostics during tuning

For every tuning attempt, inspect at least:

* final commanded-joint error;
* peak commanded-joint torque;
* maximum non-commanded joint deviation;
* whether any motor spends prolonged time at `tau_max`.

Do not add permanent verbose logging unless needed for the final concise headless result.

Temporary diagnostic code outside the repository is allowed.

Do not leave temporary tuning scripts in the repository.

---

# Required implementation changes

Modify only what is necessary in:

`src/chrono_ai_excavator/controlled_scene.py`

and:

`tests/test_controlled_scene.py`

if tests must reflect the permitted hold-gain/settling configuration.

Modify:

`scripts/show_controlled_scene.py`

only if necessary for the same corrected controller configuration.

Do not modify:

`mechanical_scene.py`

unless a direct blocker proves the accepted Milestone 3 mechanics are incorrect.

If that occurs:

STOP.

Do not change Milestone 3 mechanics automatically.

---

# Documentation

Update the existing uncommitted Milestone 4 documentation only as required to reflect:

* final selected PD gains;
* hold gains if introduced;
* selected settling duration;
* final independent-test results.

Do not broaden README or technical-report scope.

Milestone 4 remains:

`in progress / awaiting human review`

even if automated acceptance passes.

---

# Preserve this correction task

Save this complete task as:

`prompts/014_milestone_4_pd_holding_correction.md`

Do not alter prompts 001 through 013.

---

# Tracking

Do not fabricate timing for the previous failed Codex attempt.

For this correction attempt, capture actual system-clock timestamps:

* correction start;
* correction end after successful verification or stop.

If the correction succeeds, add:

* event_id: `M4-CODEX-CONTROL-CORRECTION-001`
* milestone: `M4`
* activity_category: `codex_development`
* actor: `codex`
* tool: actual Codex CLI/version and `gpt-5.6-sol`
* description:
  `Retuned bounded PD motion/holding control and settling behavior to satisfy Milestone 4 joint-control acceptance criteria.`
* human_active_minutes: empty
* ai_wall_seconds: measured correction wall seconds
* compute_wall_seconds: empty
* iteration_type: `correction`
* ai_result_status: `pending_review`
* estimate_quality: `measured`
* evidence:
  `prompts/014_milestone_4_pd_holding_correction.md and Codex task transcript`

If the correction fails:

do not record it as accepted.

Report measured timing in the completion report.

Do not invent prior attempt timing.

---

# Verification sequence

First run only:

```text
python scripts/show_controlled_scene.py --headless-check
```

If it fails any fixed criterion:

STOP.

Report the exact final values.

Do not run later verification.

If it passes, continue with exactly:

```text
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

Do not repeat environment or mechanical-baseline checks unless the controlled-scene correction unexpectedly indicates a baseline failure.

Do not open Irrlicht automatically.

Human visual review remains a separate next step.

---

# Success report requirements

If successful, report for each joint:

## J0_SLEW

* target angle;
* final angle;
* final error;
* maximum non-commanded deviation;
* peak absolute torque.

## J1_BOOM

same fields.

## J2_STICK

same fields.

## J3_BUCKET

same fields.

Also report:

* final motion `Kp`, `Kd` for all four joints;
* final hold `Kp`, `Kd` if distinct hold gains were introduced;
* unchanged `tau_max` for all four joints;
* final post-trajectory settling duration;
* combined four-joint control result;
* measured control-simulation wall time;
* full unittest result.

---

# Strict exclusions

Do not:

* change target deltas;
* change 1.0-second trajectory duration;
* increase torque limits;
* weaken `1.5°` target-error criterion;
* weaken `0.5°` holding criterion;
* add integral action;
* add PID;
* add feed-forward;
* add gravity;
* add gravity compensation;
* modify mechanical bodies;
* modify joint pivots;
* modify joint axes;
* add contacts;
* add dynamic cubes;
* add excavation sequence;
* add state machine;
* add telemetry;
* add HUD;
* add active-joint visualization;
* add cameras;
* add PDF;
* add presentation;
* add video;
* add dependencies;
* commit;
* push;
* switch branches.

---

# Completion report

Report only:

1. files modified or created;
2. exact allowed correction used:

   * PD retuning;
   * hold gains;
   * settling duration;
3. final motion gains for each joint;
4. final hold gains for each joint if applicable;
5. confirmation that all `tau_max` values are unchanged;
6. final settling duration;
7. final independent result for J0;
8. final independent result for J1;
9. final independent result for J2;
10. final independent result for J3;
11. combined four-joint result;
12. controlled headless-check result;
13. unittest count/result;
14. compilation result;
15. tracking-summary result;
16. `git diff --check` result;
17. branch/worktree status;
18. measured correction Codex wall time;
19. measured simulation wall time;
20. confirmation that acceptance criteria were not weakened;
21. confirmation that Milestone 3 mechanics were unchanged;
22. confirmation that no contacts, dynamic cubes, excavation logic, telemetry, cameras, PDF, presentation, or video were added;
23. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
