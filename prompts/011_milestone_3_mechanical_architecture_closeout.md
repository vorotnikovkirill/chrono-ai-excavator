# Milestone 3 — Mechanical Architecture Closeout

## Objective

Close the accepted Milestone 3 mechanical-architecture implementation and prepare the feature branch for merge into `main`.

This task is strictly limited to:

* updating the README;
* updating the living technical report;
* documenting the Milestone 3 correction history;
* preserving this Codex task;
* running the established display-free verification.

Do not start the next milestone.

Do not change the accepted mechanical implementation.

Do not commit.

Do not push.

Do not merge branches.

If any unexpected condition is found that is outside this task, STOP and report it.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

No deviation is allowed without explicit project-owner approval.

Do not introduce:

* side tasks;
* cleanup;
* refactoring;
* extra features;
* additional architecture;
* future-milestone implementation;
* additional audits beyond those explicitly listed below.

The project priority remains:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/mechanical-architecture`

Expected HEAD:

`887a97be2eb5b68374bafc10104eff392bf41478`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

The branch is already synchronized with its remote.

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Accepted Milestone 3 implementation

Milestone 3 implemented the articulated mechanical architecture of the excavator.

## Primary mechanical bodies

Exactly five primary bodies:

* `BASE`
* `UPPER`
* `BOOM`
* `STICK`
* `BUCKET`

Status:

* `BASE` — fixed
* `UPPER` — dynamic
* `BOOM` — dynamic
* `STICK` — dynamic
* `BUCKET` — dynamic

Masses and inertias are preliminary toy-model values used only for mechanical-architecture verification.

They are not calibrated real-excavator properties.

---

# Revolute-joint architecture

Exactly four functional Project Chrono revolute joints:

* `J0_SLEW`: `BASE ↔ UPPER`
* `J1_BOOM`: `UPPER ↔ BOOM`
* `J2_STICK`: `BOOM ↔ STICK`
* `J3_BUCKET`: `STICK ↔ BUCKET`

Installed PyChrono convention confirmed during Milestone 3:

`ChLinkLockRevolute` rotates about the joint frame local Z axis.

Actual initial joint axes:

* `J0_SLEW`: approximately `(0, 1, 0)`
* `J1_BOOM`: `(0, 0, 1)`
* `J2_STICK`: `(0, 0, 1)`
* `J3_BUCKET`: `(0, 0, 1)`

Scene vertical is Y.

The boom/stick/bucket motion plane is approximately X-Y, so J1/J2/J3 correctly use transverse scene Z.

---

# Milestone 3 correction history

Document the two corrections accurately.

## Correction 1 — PyChrono connectivity validation

Initial mechanical verification stopped with:

`AttributeError: 'ChBodyFrame' object has no attribute 'GetName'`

Root cause:

`GetBody1()` and `GetBody2()` return `ChBodyFrame` wrappers in the installed PyChrono binding, and that wrapper does not expose `GetName()`.

Correction:

* direct equality comparison against the exact stored `ChBody` references was used;
* equality was verified to work reliably;
* Python object identity was not used;
* exact parent/child connectivity validation remained intact.

No topology was changed.

Preserved correction prompt:

`prompts/009_milestone_3_joint_connectivity_api_correction.md`

---

## Correction 2 — decorative pivot-marker orientation

Human visual review showed that the visible boom/stick/bucket pivot cylinders appeared vertical.

A diagnostic confirmed:

* actual Project Chrono revolute joints were correct;
* joint pivot coordinates were correct;
* only decorative cylinder markers were incorrectly oriented.

Root cause:

`ChVisualShapeCylinder` is intrinsically aligned with local Z, while the helper assumed an intrinsic Y axis.

Minimal correction:

* `cylinder_axis == "z"` uses identity rotation;
* `cylinder_axis == "y"` rotates intrinsic Z to scene Y using `QuatFromAngleX(-π/2)`.

Mechanical joint frames and pivot positions were not changed.

Preserved diagnostic/correction prompts:

* `prompts/009_milestone_3_joint_connectivity_api_correction.md`
* `prompts/010_milestone_3_pivot_marker_orientation_correction.md`

---

# Accepted verification result

The accepted Milestone 3 implementation passed:

* mechanical headless validation: **PASS**
* zero-gravity constraint smoke test: **PASS**
* smoke-test duration: `0.005 s`
* full unittest suite: **30/30 passed**
* Python compilation: **PASS**
* `git diff --check`: **PASS**

The mechanical scene retains:

* the accepted Milestone 2 environment;
* platform;
* 30 fixed colored cubes;
* receiving container;
* accepted visual composition.

No motors or contact implementation exist.

---

# Human visual acceptance

The final mechanical scene was manually reviewed by the project owner after the decorative-marker correction.

Result:

`accepted`

The project owner explicitly confirmed:

`ок. Выглядит правильно.`

Recorded project-ledger event:

`M3-MECHANICAL-VISUAL-REVIEW-001`

Human acceptance specifically confirmed that the corrected J1/J2/J3 decorative markers visually align with the transverse mechanical joint axes.

Do not create another duplicate visual-review event.

---

# Accepted Git history

Mechanical implementation commit:

`408b50f231a4b2e3edfdc52ef51b1e13240b5f3f`

Commit message:

`feat: add excavator mechanical architecture`

Milestone 3 tracking finalization:

`887a97be2eb5b68374bafc10104eff392bf41478`

Commit message:

`docs: finalize milestone 3 tracking`

Current feature branch HEAD:

`887a97be2eb5b68374bafc10104eff392bf41478`

---

# Required changes

## 1. Update README

Update `README.md` minimally.

State that Milestone 3 mechanical architecture is:

* implemented;
* display-free verified;
* human visually accepted;
* committed;
* pushed to `feature/mechanical-architecture`;
* awaiting merge into `main`.

Document the implemented architecture concisely:

* five primary mechanical bodies;
* four functional revolute joints;
* zero-gravity topology verification.

State clearly that the following remain future work:

* motors;
* torque control;
* state-machine control;
* contacts;
* dynamic cubes;
* telemetry;
* active-joint visualization;
* bucket-mounted camera;
* cabin/operator camera;
* video.

Do not add new roadmap items.

Do not mark Milestone 3 as merged or fully complete yet.

---

## 2. Update technical report

Update:

`docs/technical_report.md`

Document the accepted Milestone 3 result.

Include:

* five-body topology;
* four-joint topology and connectivity;
* confirmed joint-axis convention;
* placeholder mass/inertia policy;
* zero-gravity architecture-validation approach;
* 30/30 passing tests;
* zero-gravity smoke-test result;
* human visual acceptance;
* connectivity API correction;
* decorative pivot-marker correction;
* accepted implementation commit;
* tracking commit;
* current feature branch status;
* current limitations.

State explicitly:

> Milestone 3 mechanical implementation is accepted and ready for merge into main.

Do not state that Milestone 3 is merged or fully closed yet.

---

## 3. Project tracking

Do not create duplicate events.

Do not alter:

* `M3-BRANCH-CREATION-001`
* `M3-MECHANICAL-VISUAL-REVIEW-001`
* `M3-MECHANICAL-COMMIT-PUSH-001`

Do not invent Codex execution durations.

Do not infer missing timing from Git commits or file timestamps.

The tracking ledger should only be changed if required to correct a factual documentation inconsistency discovered within the explicit scope of this task.

Otherwise leave it unchanged.

---

## 4. Preserve this task

Save this complete task as:

`prompts/011_milestone_3_mechanical_architecture_closeout.md`

Do not alter prompts 001 through 010.

---

# Verification

Run only:

```bash
python scripts/check_environment.py
python scripts/show_static_scene.py --headless-check
python scripts/show_mechanical_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

Verify only:

* branch is `feature/mechanical-architecture`;
* committed base remains `887a97be2eb5b68374bafc10104eff392bf41478`;
* origin is unchanged;
* accepted mechanical-scene source code was not changed;
* no package was installed;
* no display window was opened;
* no next-stage functionality was added.

If any prescribed verification fails:

STOP and report the exact failure.

Do not automatically fix it unless the required fix is explicitly inside this task.

---

# Strict scope exclusions

Do not:

* modify `mechanical_scene.py`;
* modify the accepted mechanical topology;
* modify joint axes;
* modify pivot positions;
* modify visual proportions;
* modify colors;
* modify camera composition;
* modify cube arrangement;
* add motors;
* add motor links;
* add torque control;
* add position control;
* add state machines;
* add joint limits;
* add springs;
* add dampers;
* add contacts;
* add collision response;
* make cubes dynamic;
* add telemetry;
* add HUD;
* add active-joint highlighting;
* add bucket camera;
* add cabin camera;
* add camera animation;
* add screenshots;
* add rendering;
* add PDF;
* add presentation;
* add video;
* add FFmpeg;
* add CI;
* add dependencies;
* add CAD;
* add meshes;
* refactor unrelated code;
* switch branches;
* merge;
* commit;
* push.

---

# Completion report

Report only:

1. files modified or created;
2. README Milestone 3 status;
3. technical-report Milestone 3 status;
4. correction history documented;
5. preserved prompt path;
6. environment-check result;
7. static-scene headless result;
8. mechanical-scene headless result;
9. zero-gravity smoke-test result;
10. unittest result;
11. compilation result;
12. tracking-summary result;
13. `git diff --check` result;
14. branch, HEAD, and worktree status;
15. confirmation that accepted mechanical source code was unchanged;
16. confirmation that Milestone 3 is documented as accepted and ready for merge;
17. confirmation that Milestone 3 was not merged;
18. confirmation that no next-stage functionality was started;
19. confirmation that no package installation, commit, push, branch switch, remote modification, PDF, presentation, or video work occurred.

Do not commit or push.
