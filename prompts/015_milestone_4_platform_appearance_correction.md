# Milestone 4 — Controlled Viewer Lighting Parity Correction

## Objective

Correct exactly one confirmed visual regression in the Milestone 4 controlled viewer:

> The controlled scene appears too bright because `show_controlled_scene.py` uses `AddTypicalLights()`, while the accepted Milestone 2/3 viewers use a custom directional + point-light configuration.

The project owner explicitly authorized this narrow lighting correction.

Make the controlled viewer use the same accepted lighting configuration as the existing static/mechanical viewers.

Do not change anything else.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

This is one narrow correction only.

No unrelated cleanup, refactoring, feature work, visual redesign, or future-milestone implementation is allowed.

If the exact accepted lighting configuration cannot be reused without broader changes:

STOP and report the blocker.

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/joint-actuation-control`

The worktree contains the current uncommitted Milestone 4 implementation.

Preserve all existing work.

Do not reset.

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Confirmed diagnosis

The platform material is already correct.

Accepted platform color:

```text
PLATFORM_GRAY = (0.29, 0.32, 0.35)
```

The controlled scene already inherits this material through the shared mechanical-scene builder.

Therefore:

* platform material is not the defect;
* geometry is not the defect;
* camera is not the defect;
* controller is not the defect.

The confirmed difference is lighting.

Current controlled viewer:

`AddTypicalLights()`

Accepted Milestone 2/3 viewers:

custom directional and point lights.

---

# Required correction

## 1. Inspect accepted lighting

Inspect only the existing accepted viewer implementations:

* `scripts/show_static_scene.py`
* `scripts/show_mechanical_scene.py`

Identify the exact lighting configuration used by the accepted visual baseline.

Record:

* directional-light configuration;
* point-light configuration;
* any intensities/positions/colors directly relevant to that accepted lighting setup.

Do not change those files.

---

## 2. Apply lighting parity

Modify only:

`scripts/show_controlled_scene.py`

as required to replace `AddTypicalLights()` with the same accepted lighting setup already used by the accepted viewer(s).

Requirements:

* same lighting intent;
* same relevant light parameters;
* no change to camera position;
* no change to camera target;
* no change to background;
* no change to geometry;
* no change to platform material;
* no change to excavator colors;
* no change to cube/container appearance definitions.

Prefer direct reuse of the already accepted light calls.

Do not create a new lighting framework.

Do not refactor shared visualization architecture.

---

# Control configuration is frozen

Do not modify any Milestone 4 control value.

Motion gains remain:

* J0: `(1500, 2500)`
* J1: `(2000, 1200)`
* J2: `(1500, 700)`
* J3: `(800, 200)`

Hold gains remain:

* J0: `(1500, 2500)`
* J1: `(6500, 2800)`
* J2: `(6000, 2200)`
* J3: `(1600, 500)`

Torque limits remain:

* J0: `800 N·m`
* J1: `800 N·m`
* J2: `600 N·m`
* J3: `300 N·m`

Target deltas remain:

* J0: `+12°`
* J1: `+8°`
* J2: `−8°`
* J3: `+10°`

Trajectory duration remains:

`1.0 s`

Post-transition settling remains:

`2.0 s`

Do not alter any of these values.

---

# Contacts remain out of scope

Do not add contact or collision response.

The bucket may still pass visually below the platform.

This remains an accepted Milestone 4 limitation.

Do not modify trajectory or geometry to hide that behavior.

---

# Tracking

The earlier human visual review has not yet been added to the ledger.

Add exactly one event if absent:

* event_id: `M4-CONTROL-VISUAL-REVIEW-001`
* milestone: `M4`
* started_at: `2026-08-09T16:13:56+03:00`
* ended_at: `2026-08-09T16:15:20+03:00`
* activity_category: `human_review`
* actor: `project_owner`
* tool: `Project Chrono Irrlicht and ChatGPT`
* description:
  `Reviewed the Milestone 4 controlled scene. Joint motion was visually acceptable; the no-contact bucket motion was accepted as an expected limitation; a lighting-related platform appearance regression was identified for correction.`
* human_active_minutes: `1.40`
* ai_wall_seconds: empty
* compute_wall_seconds: empty
* iteration_type: `correction`
* ai_result_status: `accepted_with_corrections`
* cost_amount: empty
* cost_currency: empty
* evidence:
  `/tmp/chrono_ai_excavator_step_08b_control_visual_review.txt and project-owner assessment at 2026-08-09T16:15:20+03:00`
* estimate_quality: `derived_from_timestamps`
* notes:
  `Viewer exit status was 0. Control behavior was accepted. Contacts remain outside Milestone 4 scope. The requested correction is lighting parity with the accepted Milestone 2/3 viewer.`

Preserve LF line endings.

Do not modify unrelated ledger events.

---

# Preserve this correction task

Save this complete task as:

`prompts/015_milestone_4_platform_appearance_correction.md`

Since the previous STOP occurred before prompt 015 was created, this authorized lighting-parity correction becomes the canonical prompt 015.

Do not alter prompts 001 through 014.

---

# Verification

Run only:

```text
python scripts/show_controlled_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
git status --short --branch
```

The controlled headless check must continue to satisfy all previously accepted numerical control criteria.

If any control result regresses:

STOP.

Do not retune anything.

Do not open Irrlicht automatically.

Human visual confirmation of the corrected lighting will be a separate step.

---

# Strict scope exclusions

Do not:

* modify `controlled_scene.py`;
* change gains;
* change torque limits;
* change trajectories;
* change settling duration;
* change platform material;
* change platform geometry;
* change camera;
* change background;
* change excavator geometry;
* change cube/container geometry;
* add contacts;
* add dynamic cubes;
* add excavation logic;
* add telemetry;
* add HUD;
* add active-joint visualization;
* add bucket camera;
* add cabin camera;
* add PDF;
* add presentation;
* add video;
* add dependencies;
* refactor unrelated code;
* install packages;
* commit;
* push;
* switch branches.

---

# Completion report

Report only:

1. exact accepted lighting configuration identified;
2. exact lighting change made in `show_controlled_scene.py`;
3. files modified or created;
4. confirmation that platform material remained unchanged;
5. confirmation that camera and background remained unchanged;
6. confirmation that all control gains remained unchanged;
7. confirmation that torque limits, trajectories, and settling duration remained unchanged;
8. controlled headless-check result;
9. final four independent control results;
10. unittest count/result;
11. compilation result;
12. `git diff --check` result;
13. branch/worktree status;
14. `M4-CONTROL-VISUAL-REVIEW-001` ledger status;
15. confirmation that contacts were not added;
16. confirmation that bucket-below-ground behavior was not altered;
17. confirmation that no next-stage functionality was added;
18. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
