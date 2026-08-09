# Milestone 4 — Joint Actuation and Control Closeout

## Objective

Close the accepted Milestone 4 joint-actuation and basic-control implementation and prepare `feature/joint-actuation-control` for merge into `main`.

This task is strictly limited to:

* recording the accepted Milestone 4 implementation commit/push;
* documenting the final accepted control result;
* documenting the correction history;
* updating README;
* updating the living technical report;
* preserving this Codex task;
* running the established display-free verification.

Do not start contacts or any next milestone.

Do not change the accepted control implementation.

Do not commit or push.

If anything unexpected is found outside this scope, STOP and report it.

---

# Canonical project rule

Proceed strictly according to the agreed plan.

No side tasks, cleanup, refactoring, visual improvements, additional features, or future-milestone work are allowed without explicit project-owner approval.

Project priority:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/joint-actuation-control`

Expected HEAD:

`9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

The accepted implementation is already committed and pushed to the feature branch.

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Accepted Milestone 4 result

Milestone 4 implements torque-based actuation and bounded PD control for exactly four joints:

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

The controlled scene uses four `ChLinkMotorRotationTorque` links without duplicate revolute constraints.

Milestone 3 reference mechanics remain unchanged.

Gravity remains disabled for this control-isolation milestone.

Contacts remain absent.

---

# Accepted controller configuration

## Motion gains `(Kp, Kd)`

* J0: `(1500, 2500)`
* J1: `(2000, 1200)`
* J2: `(1500, 700)`
* J3: `(800, 200)`

## Hold gains `(Kp, Kd)`

* J0: `(1500, 2500)`
* J1: `(6500, 2800)`
* J2: `(6000, 2200)`
* J3: `(1600, 500)`

## Torque limits

* J0: `800 N·m`
* J1: `800 N·m`
* J2: `600 N·m`
* J3: `300 N·m`

## Target deltas

* J0: `+12°`
* J1: `+8°`
* J2: `−8°`
* J3: `+10°`

Trajectory duration:

`1.0 s`

Post-transition settling:

`2.0 s`

These are demonstrator values, not calibrated excavator actuator properties.

---

# Accepted numerical verification

Final independent results:

## J0_SLEW

* target: `+12.00°`
* final: `+12.71°`
* error: `−0.71°`
* maximum non-commanded deviation: `0.09°`
* peak torque: `454.59 / 800 N·m`

## J1_BOOM

* target: `+8.00°`
* final: `+8.12°`
* error: `−0.12°`
* maximum non-commanded deviation: `0.42°`
* peak torque: `183.00 / 800 N·m`

## J2_STICK

* target: `−8.00°`
* final: `−7.89°`
* error: `−0.11°`
* maximum non-commanded deviation: `0.44°`
* peak torque: `82.01 / 600 N·m`

## J3_BUCKET

* target: `+10.00°`
* final: `+10.00°`
* error: approximately `0.00°`
* maximum non-commanded deviation: `0.03°`
* peak torque: `8.31 / 300 N·m`

Combined four-joint control smoke test:

`PASS`

Final verification:

* controlled headless check: `PASS`
* full unittest suite: `38/38 PASS`
* compilation: `PASS`
* `git diff --check`: `PASS`

---

# Human visual acceptance

Initial interactive review showed:

* joint motion visually acceptable;
* no-contact bucket motion accepted as an intentional limitation;
* controlled viewer lighting did not match the accepted darker baseline.

Recorded event:

`M4-CONTROL-VISUAL-REVIEW-001`

Result:

`accepted_with_corrections`

The lighting difference was diagnosed as:

* platform material already correct;
* controlled viewer used `AddTypicalLights()`;
* accepted Milestone 2/3 viewers used custom directional + point lighting.

The project owner explicitly authorized a lighting-only correction.

The controlled viewer was changed to use the exact accepted lighting configuration.

No:

* camera;
* background;
* platform material;
* geometry;
* control gains;
* torque limits;
* trajectories;
* settling;
* mechanics

were changed.

Final lighting review:

* viewer exit status: `0`
* project-owner verdict: `все хорошо`
* result: `accepted`

Recorded event:

`M4-LIGHTING-VISUAL-REVIEW-001`

---

# Accepted limitation

The bucket can move visually below the platform because Milestone 4 has no contacts.

This was explicitly reviewed and accepted as a current-scope limitation.

Do not treat this as a Milestone 4 defect.

Do not add contacts.

---

# Correction history

Document the two control/visual corrections accurately.

## Correction 1 — PD holding and settling

Initial bounded control did not satisfy all fixed criteria.

The project owner authorized one narrow correction pass limited to:

* PD retuning;
* distinct hold gains;
* deterministic settling extension.

Acceptance criteria, targets, trajectory duration, torque limits, mechanics, and scope remained unchanged.

Result:

all four joints passed.

Preserved prompt:

`prompts/014_milestone_4_pd_holding_correction.md`

## Correction 2 — controlled-viewer lighting parity

Human review found the platform appeared too bright.

Diagnosis:

* material was already correct;
* lighting configuration differed.

Correction:

replaced `AddTypicalLights()` with the exact accepted Milestone 2/3 directional and point lighting.

Preserved prompt:

`prompts/015_milestone_4_platform_appearance_correction.md`

---

# Confirmed Git history

Accepted Milestone 4 implementation:

`9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`

Commit message:

`feat: add bounded joint actuation control`

Measured commit/push operation:

* started: `2026-08-09T22:42:44+03:00`
* ended: `2026-08-09T22:42:46+03:00`
* duration: `2 seconds`
* commit: `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`
* feature push: `PASS`

Evidence:

`/tmp/chrono_ai_excavator_step_08f_commit_push_m4.txt`

---

# Required changes

## 1. Record Milestone 4 commit/push

Update:

`project_tracking/events.csv`

Add exactly one event if absent:

* event_id: `M4-CONTROL-COMMIT-PUSH-001`
* milestone: `M4`
* started_at: `2026-08-09T22:42:44+03:00`
* ended_at: `2026-08-09T22:42:46+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Committed and pushed the accepted Milestone 4 bounded joint-actuation and control implementation.`
* human_active_minutes: `0.03`
* ai_wall_seconds: empty
* compute_wall_seconds: empty
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* cost_amount: empty
* cost_currency: empty
* evidence:
  `/tmp/chrono_ai_excavator_step_08f_commit_push_m4.txt and Git commit 9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`
* estimate_quality: `measured`
* notes:
  `Local and remote feature branches were verified at the same commit. Network time is not simulation or computation time.`

Preserve LF line endings.

Do not modify unrelated events.

---

## 2. Update README

Update `README.md` minimally.

Milestone 4 must be described as:

* implemented;
* numerically verified;
* human visually accepted;
* lighting correction accepted;
* committed;
* pushed to `feature/joint-actuation-control`;
* awaiting merge into `main`.

Document concisely:

* four torque-actuated joints;
* bounded PD motion control;
* distinct hold gains;
* fixed torque saturation;
* deterministic smooth target trajectories;
* zero-gravity control isolation;
* 38/38 passing tests.

State clearly that these remain future work:

* contacts;
* dynamic cubes;
* scoop/dump sequence;
* excavation state machine;
* telemetry/HUD;
* active-joint visualization;
* bucket camera;
* cabin camera;
* final video.

Do not mark Milestone 4 as merged or fully complete yet.

Do not add new roadmap items.

---

## 3. Update technical report

Update:

`docs/technical_report.md`

Document the accepted Milestone 4 result, including:

* torque-motor architecture;
* avoidance of duplicate revolute constraints;
* PD equation;
* saturation;
* motion gains;
* hold gains;
* torque limits;
* smooth 1.0-second target trajectory;
* 2.0-second settling interval;
* zero-gravity rationale;
* four independent numerical results;
* combined four-joint PASS;
* 38/38 tests;
* human control review;
* PD/holding correction;
* lighting-parity correction;
* final visual acceptance;
* accepted no-contact bucket-below-platform limitation;
* implementation commit `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`;
* current feature-branch state.

State explicitly:

> **Milestone 4 implementation is accepted and ready for merge into main.**

Do not state Milestone 4 is merged or fully closed yet.

---

## 4. Preserve this task

Save this complete task as:

`prompts/016_milestone_4_joint_actuation_control_closeout.md`

Do not alter prompts 001 through 015.

---

# Verification

Run only:

```text
python scripts/show_mechanical_scene.py --headless-check
python scripts/show_controlled_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

Verify only:

* branch is `feature/joint-actuation-control`;
* committed base remains `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`;
* origin unchanged;
* `controlled_scene.py` unchanged by this closeout task;
* `show_controlled_scene.py` unchanged by this closeout task;
* no package installation;
* no display window;
* no next-stage implementation.

If a listed check fails:

STOP and report it.

Do not automatically repair or broaden scope.

---

# Strict exclusions

Do not:

* modify controlled-scene source;
* modify controller gains;
* modify hold gains;
* modify torque limits;
* modify trajectories;
* modify settling duration;
* modify mechanics;
* modify lighting;
* modify camera;
* add contacts;
* add dynamic cubes;
* add excavation state machine;
* add scoop/dump sequence;
* add telemetry;
* add HUD;
* add active-joint visualization;
* add bucket camera;
* add cabin camera;
* add rendering;
* add PDF;
* add presentation;
* add video;
* add dependencies;
* refactor;
* switch branches;
* merge;
* commit;
* push.

---

# Completion report

Report only:

1. files modified or created;
2. `M4-CONTROL-COMMIT-PUSH-001` status;
3. README Milestone 4 status;
4. technical-report Milestone 4 status;
5. correction history documented;
6. preserved prompt path;
7. mechanical headless result;
8. controlled headless result;
9. four final independent control results;
10. combined control result;
11. unittest result;
12. compilation result;
13. tracking-summary result;
14. `git diff --check` result;
15. branch, HEAD, upstream, and worktree status;
16. confirmation that controlled-scene implementation files were unchanged;
17. confirmation that Milestone 4 is documented as accepted and ready for merge;
18. confirmation that contacts and next-stage work were not started;
19. confirmation that no package installation, commit, push, branch switch, remote modification, PDF, presentation, or video work occurred.

Do not commit or push.
