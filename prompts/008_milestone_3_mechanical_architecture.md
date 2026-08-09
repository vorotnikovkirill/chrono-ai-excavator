# Milestone 3 — Mechanical Architecture and Revolute Joints

## Objective

Implement the mechanical architecture of the Chrono AI Excavator.

Convert the accepted visual excavator concept into a minimal articulated Project Chrono multibody mechanism with exactly four functional revolute joints:

* `J0_SLEW` — fixed base to upper structure;
* `J1_BOOM` — upper structure to boom;
* `J2_STICK` — boom to stick;
* `J3_BUCKET` — stick to bucket.

This milestone establishes the mechanical topology only.

Do not add motors, controllers, contacts, autonomous motion, telemetry, camera variants, or video functionality.

The result must remain visually consistent with the accepted Milestone 2 scene.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

Do not introduce:

* side tasks;
* opportunistic refactoring;
* unrelated cleanup;
* additional features;
* future-milestone implementation;
* additional audits beyond the verification explicitly required here.

If an unexpected repository condition, API incompatibility, or design ambiguity appears that would require changing the agreed scope, STOP and report it.

Do not make an unapproved design decision outside this task.

The project priority remains:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/mechanical-architecture`

Expected starting HEAD:

`848d2806945748fb0332d50f1cdf74d7c4f8bbd9`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

The branch was created and published from the fully closed Milestone 2 `main`.

Do not switch branches.

Do not commit.

Do not push.

Do not modify remotes.

---

# Existing accepted visual baseline

Milestone 2 produced and human-approved the first static scene.

The accepted visual scene contains:

* procedural block-style excavator;
* platform;
* 30 colored cubes;
* receiving container;
* external Irrlicht camera;
* lighting and background.

The existing accepted implementation includes:

`src/chrono_ai_excavator/static_scene.py`

and:

`scripts/show_static_scene.py`

The static Milestone 2 scene is a frozen visual reference.

Do not alter its accepted appearance unless technically unavoidable for the new mechanical scene.

Do not refactor the existing static scene merely to improve architecture.

---

# Mechanical architecture

## 1. Mechanical bodies

Create a minimal articulated excavator using five primary mechanical bodies.

### `BASE`

Fixed body.

It represents:

* lower chassis;
* left track visual assembly;
* right track visual assembly.

The tracks remain visual only.

Do not implement track dynamics.

### `UPPER`

Dynamic body.

It represents the rotating upper excavator structure, including visual elements such as:

* rotating platform;
* cabin;
* roof/windows;
* rear body;
* counterweight.

These visual elements must move rigidly with `UPPER`.

### `BOOM`

Dynamic body.

Represents the complete boom assembly.

### `STICK`

Dynamic body.

Represents the complete stick/arm assembly.

### `BUCKET`

Dynamic body.

Represents the complete bucket assembly.

The accepted visual bucket may remain assembled from multiple primitive visual shapes, but all of those shapes must belong mechanically to one bucket body.

---

# 2. Mechanical scene environment

Retain the Milestone 2 environment:

* platform;
* 30 colored cubes;
* receiving container;
* accepted external scene composition.

For this milestone:

* platform remains fixed;
* cubes remain fixed;
* container remains fixed;
* collision is not required;
* contact is not implemented.

Do not make the cubes dynamic.

---

# 3. Revolute joints

Create exactly four functional Project Chrono revolute joints.

Use the installed PyChrono API rather than assuming API syntax from another Chrono release.

Inspect available classes when necessary.

## `J0_SLEW`

Connect:

`BASE → UPPER`

Axis:

vertical axis of the current scene coordinate system.

Purpose:

allow only upper-structure rotation relative to the fixed base.

---

## `J1_BOOM`

Connect:

`UPPER → BOOM`

Axis:

horizontal boom hinge axis through the visual boom pivot.

Purpose:

allow boom elevation rotation.

---

## `J2_STICK`

Connect:

`BOOM → STICK`

Axis:

parallel to the boom hinge axis.

Purpose:

allow stick rotation relative to the boom.

---

## `J3_BUCKET`

Connect:

`STICK → BUCKET`

Axis:

parallel to the boom and stick hinge axes.

Purpose:

allow bucket curl rotation.

---

# 4. Joint geometry

Joint locations must correspond to recognizable visual pivot locations in the accepted excavator geometry.

Requirements:

* joint frames must be finite;
* connected bodies must begin in the accepted ready-to-scoop pose;
* joint anchors must visually align with the mechanism;
* J1, J2, and J3 axes must be mutually parallel within numerical tolerance;
* J0 must be aligned with the scene vertical direction;
* no severe body interpenetration should be introduced by the mechanical conversion.

Do not add joint limits in this milestone.

Do not add springs, dampers, bushings, or compliance.

---

# 5. Mass and inertia

Dynamic bodies require positive mass and inertia values.

Use simple, clearly documented engineering placeholder values sufficient for a valid multibody model.

Requirements:

* positive mass;
* positive principal inertias;
* finite values;
* no attempt at real-excavator calibration.

If useful, derive simple placeholder values from the procedural dimensions.

Clearly document that these values are:

> preliminary toy-model mechanical properties for architecture verification only.

Do not perform mass-property calibration or optimization.

---

# 6. Gravity and movement

This milestone is about topology, not uncontrolled excavator motion.

The mechanical architecture must support display-free verification without the boom collapsing under gravity.

For the architecture-validation configuration:

* use zero gravity or otherwise explicitly disable gravity-driven motion;
* initialize all velocities to zero;
* do not add actuators merely to hold the pose.

A very short zero-gravity dynamics/constraint smoke test is allowed solely to verify that the joint topology remains finite and stable.

Do not demonstrate excavator motion yet.

---

# Required implementation

## 7. Mechanical scene module

Create:

`src/chrono_ai_excavator/mechanical_scene.py`

Keep the implementation focused.

Provide a small API capable of:

* building the articulated Chrono system;
* returning references to the five primary mechanical bodies;
* returning references to the four revolute joints;
* exposing joint names, pivot locations, and axis metadata;
* exposing lightweight mechanical metadata needed for testing;
* performing headless architecture validation.

Do not create a general multibody framework.

Do not create speculative abstraction layers for future control or contact systems.

Reuse existing visual definitions where practical, but do not refactor the accepted Milestone 2 static scene merely for code elegance.

---

## 8. Mechanical viewer

Create:

`scripts/show_mechanical_scene.py`

It must support:

```bash
python scripts/show_mechanical_scene.py
```

for interactive Irrlicht viewing.

The viewer should:

* show the articulated mechanical scene in the accepted ready-to-scoop pose;
* use the same general external composition as Milestone 2;
* preserve the recognizable accepted appearance;
* not advance the mechanism into uncontrolled motion;
* not animate joints;
* not add HUD or joint overlays.

Also support:

```bash
python scripts/show_mechanical_scene.py --headless-check
```

Headless mode must:

* build the complete mechanical scene;
* validate the mechanical topology;
* report concise mechanical information;
* open no display window;
* return nonzero on validation failure.

A useful summary should include at least:

* mechanical body count;
* dynamic body count;
* fixed base status;
* joint count;
* joint names.

---

# Validation requirements

## 9. Mechanical validation

Validate at least:

### Bodies

Exactly five primary mechanical excavator bodies exist:

* `BASE`
* `UPPER`
* `BOOM`
* `STICK`
* `BUCKET`

Verify:

* `BASE` is fixed;
* `UPPER`, `BOOM`, `STICK`, and `BUCKET` are dynamic;
* masses are positive;
* principal inertias are positive;
* positions and orientations are finite.

### Joints

Exactly four excavator revolute joints exist:

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

Verify connectivity:

* `J0_SLEW`: BASE ↔ UPPER
* `J1_BOOM`: UPPER ↔ BOOM
* `J2_STICK`: BOOM ↔ STICK
* `J3_BUCKET`: STICK ↔ BUCKET

Verify:

* joint pivot locations are finite;
* joint axes are finite and normalized;
* J0 is parallel to the scene vertical direction;
* J1/J2/J3 are mutually parallel.

### Environment

Verify:

* platform exists;
* 30 cubes remain present;
* receiving container remains present;
* cubes are not converted into dynamic contact bodies.

### Scope

Verify mechanically or structurally where practical that:

* no motor links were added;
* no controller objects were added;
* no contact implementation was added.

---

## 10. Constraint smoke test

Run a short display-free, zero-gravity mechanical smoke test.

Purpose:

verify only that the articulated mechanism can be advanced through a small number of solver steps without:

* exceptions;
* NaNs;
* infinities;
* obvious constraint explosion.

Initial velocities must be zero.

This smoke test is not a motion demonstration.

Do not tune solver settings beyond what is necessary for a minimal stable check.

Do not optimize performance.

---

# Tests

## 11. Automated tests

Create:

`tests/test_mechanical_scene.py`

Use standard-library `unittest`.

Keep all existing tests.

Cover at least:

* mechanical scene construction;
* exact five-body primary mechanical topology;
* fixed/dynamic body status;
* positive masses and inertias;
* exact four-joint count;
* exact joint names;
* correct joint connectivity;
* J0 vertical-axis alignment;
* J1/J2/J3 parallel-axis alignment;
* finite joint pivots;
* environment retention;
* 30 cubes retained;
* no motors in the architecture;
* zero-gravity constraint smoke test;
* deterministic mechanical metadata;
* headless validation success.

Tests must not open Irrlicht.

Do not install pytest.

---

# Project tracking

## 12. Record branch creation

Add the already measured branch-creation event to:

`project_tracking/events.csv`

if it is not already present.

Use:

* event_id: `M3-BRANCH-CREATION-001`
* milestone: `M3`
* started_at: `2026-08-09T09:47:44+03:00`
* ended_at: `2026-08-09T09:47:45+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Created and published the Milestone 3 mechanical-architecture feature branch from the fully closed Milestone 2 main branch.`
* human_active_minutes: `0.02`
* ai_wall_seconds: empty
* compute_wall_seconds: empty
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* cost_amount: empty
* cost_currency: empty
* evidence:
  `/tmp/chrono_ai_excavator_step_07a_create_m3_branch.txt and starting commit 848d2806945748fb0332d50f1cdf74d7c4f8bbd9`
* estimate_quality: `measured`
* notes:
  `Local and remote feature/mechanical-architecture branches were verified at the same starting commit.`

Preserve LF CSV line endings.

Do not invent Codex execution duration.

Do not infer task timing from file timestamps.

Any measured Codex timing must come from external evidence.

---

# Documentation

## 13. README

Update `README.md` minimally.

State:

* Milestone 2 remains complete;
* Milestone 3 is in progress;
* the current Milestone 3 implementation introduces the articulated mechanical architecture;
* five primary mechanical bodies are used;
* four functional revolute joints are used;
* headless mechanical verification is available.

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

Do not claim Milestone 3 is complete before human review.

---

## 14. Technical report

Update:

`docs/technical_report.md`

Add the Milestone 3 mechanical-architecture work.

Document:

* five-body mechanical topology;
* four revolute joints;
* joint connectivity;
* joint-axis intent;
* placeholder mass/inertia policy;
* zero-gravity architecture-validation approach;
* distinction between accepted visual geometry and new mechanical bodies;
* automated verification;
* current limitations.

State:

> Milestone 3 mechanical architecture is implemented and awaiting human review.

Do not document motors, control, or contact as implemented.

---

# 15. Preserve this task

Save this complete specification as:

`prompts/008_milestone_3_mechanical_architecture.md`

Do not alter prompts 001 through 007.

---

# Verification

Run only these planned checks inside the existing `chrono` Conda environment:

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

Do not run additional audits unless one of these checks fails and diagnosis is required.

Do not automatically repair an unexpected condition outside this task.

Do not open the interactive Irrlicht viewer as part of automated verification.

Human visual inspection of the mechanical scene will be a separate step after Codex reports success.

---

# Strict scope exclusions

Do not implement:

* motors;
* `ChLinkMotorRotation*` links;
* torque commands;
* position commands;
* PD control;
* PI control;
* state-machine control;
* scripted excavator motion;
* joint limits;
* springs;
* dampers;
* bushings;
* contact materials;
* collision response;
* cube dynamics;
* bucket-to-cube contact;
* cube-to-cube contact;
* terrain;
* real track mechanics;
* hydraulics;
* telemetry;
* HUD;
* active-joint highlighting;
* torque arrows;
* bucket camera;
* cabin camera;
* camera animation;
* screenshot automation;
* rendering pipeline;
* PDF;
* presentation;
* video;
* FFmpeg;
* CI;
* GitHub Actions;
* new dependencies;
* CAD;
* external meshes;
* optimization;
* unrelated refactoring;
* branch switching;
* commit;
* push.

---

# Completion report

Report only:

1. files created or modified;
2. mechanical-body architecture;
3. body fixed/dynamic status;
4. placeholder mass/inertia approach;
5. four joint names and connectivity;
6. joint-axis configuration;
7. mechanical viewer command;
8. mechanical headless-check result;
9. zero-gravity constraint smoke-test result;
10. unittest result;
11. compilation result;
12. tracking-summary result;
13. `git diff --check` result;
14. current branch and worktree status;
15. branch-creation ledger event status;
16. known mechanical limitations;
17. items requiring human visual review;
18. exact confirmation that the accepted Milestone 2 static scene was not visually redesigned;
19. exact confirmation that no motors, control, contacts, telemetry, camera variants, PDF, presentation, or video were implemented;
20. exact confirmation that no package installation, commit, push, branch switch, or remote modification was performed.

Do not commit or push.
