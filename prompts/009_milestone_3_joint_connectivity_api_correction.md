# Milestone 3 — PyChrono Joint Connectivity Validation Correction

## Objective

Correct exactly one API-compatibility defect discovered during the prescribed Milestone 3 verification.

Do not redesign or extend the Milestone 3 implementation.

The failed check was:

```text
AttributeError: 'ChBodyFrame' object has no attribute 'GetName'
```

Location:

`validate_mechanical_scene()`

The failure occurred while validating revolute-joint body connectivity.

The installed PyChrono binding exposes the objects returned by:

```python
joint.GetBody1()
joint.GetBody2()
```

as `ChBodyFrame`, and `GetName()` is not available through that Python wrapper.

This is a validation-code compatibility defect.

It is not permission to change the mechanical topology.

---

# Canonical project rule

Proceed strictly according to the agreed Milestone 3 plan.

This correction is limited to the failed PyChrono API interaction.

Do not:

* add features;
* refactor unrelated code;
* improve the visual scene;
* change mechanical topology;
* change body count;
* change joint count;
* change joint locations or axes unless the current values are demonstrably required to fix the exact failed check;
* start motors, control, contacts, telemetry, cameras, PDF, presentation, or video work.

If another unrelated problem appears, STOP and report it.

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/mechanical-architecture`

Expected committed base:

`848d2806945748fb0332d50f1cdf74d7c4f8bbd9`

The current worktree already contains the uncommitted Milestone 3 implementation from the previous Codex task.

Preserve all current Milestone 3 work.

Do not reset or recreate it.

Do not switch branches.

Do not commit.

Do not push.

---

# Required correction

## 1. Fix connectivity validation only

Inspect the actual installed PyChrono Python API.

Do not assume that methods available on C++ `ChBody` are exposed on a Python object returned as `ChBodyFrame`.

Replace the invalid logic that performs:

```python
joint.GetBody1().GetName()
joint.GetBody2().GetName()
```

with a binding-compatible validation strategy.

The corrected validation must still genuinely verify the expected joint connectivity:

* `J0_SLEW`: `BASE` ↔ `UPPER`
* `J1_BOOM`: `UPPER` ↔ `BOOM`
* `J2_STICK`: `BOOM` ↔ `STICK`
* `J3_BUCKET`: `STICK` ↔ `BUCKET`

Use only mechanisms demonstrated to work in the installed binding.

Acceptable approaches include, in order of preference:

1. comparing the returned body-frame references with the exact stored body references if the installed binding supports reliable equality or identity for them;
2. using an exposed stable identifier/tag mechanism if it is demonstrably available on the returned wrapper;
3. maintaining explicit joint-connectivity metadata at joint construction and validating that metadata together with the actual link objects, if the binding prevents direct body-name introspection.

Do not choose an approach by assumption.

Probe the installed objects minimally if necessary and use the simplest working solution.

Do not use positions, masses, or other coincidental physical values as surrogate body identifiers.

---

## 2. Keep topology unchanged

The result must still contain exactly:

### Mechanical bodies

* `BASE`
* `UPPER`
* `BOOM`
* `STICK`
* `BUCKET`

### Revolute joints

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

Do not replace the joints with motors or another joint type.

Do not change the agreed parent-child connectivity.

---

## 3. Update tests only as required

Update:

`tests/test_mechanical_scene.py`

only where necessary to use the corrected binding-compatible connectivity validation.

The tests must still verify the exact four joint connections.

Do not weaken the test from connectivity verification to mere joint-count verification.

Do not remove any existing test requirement.

---

## 4. Documentation

Do not rewrite README or technical-report content merely because of this correction.

If the existing uncommitted Milestone 3 documentation remains accurate after the fix, leave it unchanged.

Only correct documentation if it currently contains a fact made false by this exact API correction.

---

## 5. Preserve this correction task

Save this complete specification as:

`prompts/009_milestone_3_joint_connectivity_api_correction.md`

Do not modify prompts 001 through 008.

---

# Verification sequence

Resume the original prescribed verification from the failed point.

Run first:

```bash
python scripts/show_mechanical_scene.py --headless-check
```

If it fails:

STOP and report the exact failure.

Do not continue.

If it passes, continue with exactly:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

The environment check and static-scene headless check already passed during the preceding attempt and do not need to be repeated in this correction task.

Do not add additional audits.

---

# Strict exclusions

Do not implement:

* motors;
* motor links;
* torque control;
* position control;
* controller logic;
* state machines;
* contact;
* collision response;
* cube dynamics;
* joint limits;
* springs;
* dampers;
* bushings;
* telemetry;
* HUD;
* active-joint highlighting;
* bucket camera;
* cabin camera;
* camera animation;
* PDF;
* presentation;
* video;
* FFmpeg;
* CI;
* dependencies;
* CAD;
* external meshes;
* optimization;
* unrelated refactoring.

---

# Completion report

Report only:

1. exact root cause confirmed;
2. exact connectivity-validation strategy used;
3. files modified or created by this correction;
4. confirmation that the five-body topology is unchanged;
5. confirmation that the four-joint topology and connectivity are unchanged;
6. mechanical headless-check result;
7. unittest result;
8. compilation result;
9. tracking-summary result;
10. `git diff --check` result;
11. current branch and worktree status;
12. confirmation that no test requirement was weakened;
13. confirmation that no next-stage functionality was added;
14. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
