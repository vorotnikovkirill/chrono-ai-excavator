# Milestone 5 — Contact Physics and Dynamic Cubes

## Objective

Implement contact physics and dynamic cube behavior for the Chrono AI Excavator.

This milestone proves:

> gravity → dynamic rigid cubes → rigid contact → stable interaction with platform, other cubes, bucket, and receiving container

The excavator remains fixed in its accepted ready-to-scoop pose for this milestone.

Do not combine torque control and contacts yet.

Do not implement excavation sequencing.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

No side tasks, speculative refactoring, visual redesign, future-milestone functionality, or additional features are allowed.

If an unexpected API limitation or design issue requires changing this scope:

STOP and report it.

Do not broaden the task automatically.

Project priority:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/contact-dynamic-cubes`

Expected starting HEAD:

`978740650388263531d0606451a1ee0be5298a86`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

Do not:

* switch branches;
* commit;
* push;
* modify remotes.

---

# Frozen previous milestones

Milestone 4 is complete.

Do not modify or break:

* `static_scene.py`
* `mechanical_scene.py`
* `controlled_scene.py`
* accepted mechanical topology;
* accepted controller gains;
* torque limits;
* trajectories;
* lighting;
* cameras.

The new contact-enabled scene must be a separate milestone implementation.

---

# Contact architecture

## 1. Contact formulation

Use:

`ChSystemNSC`

Use the installed PyChrono binding and probe exact API names when necessary.

Do not switch to SMC.

Do not introduce another physics engine.

---

## 2. Gravity

Enable:

```text
(0, -9.81, 0) m/s²
```

Scene Y remains vertical.

---

## 3. Contact materials

Use simple deterministic placeholder NSC materials.

Create only the minimum required material definitions.

Use these baseline properties unless the installed binding requires a naming/API adaptation:

### Cubes

* friction: `0.45`
* restitution: `0.05`

### Platform and container

* friction: `0.55`
* restitution: `0.03`

### Bucket

* friction: `0.60`
* restitution: `0.02`

These values are demonstrator contact parameters.

They are not calibrated physical material data.

Do not add:

* cohesion;
* rolling resistance;
* spinning resistance;
* compliance;
* adhesion;

unless an API default requires explicitly setting a harmless zero value.

Do not tune materials unless one of the prescribed acceptance tests fails for a direct, documented contact reason.

If substantial tuning appears necessary:

STOP and report it.

---

# Dynamic cubes

## 4. Cube count

Use exactly:

`30`

cubes.

Retain the accepted visual cube dimensions and color palette.

All 30 cubes must become dynamic rigid bodies.

Requirements:

* `SetFixed(False)` or installed equivalent;
* positive mass;
* positive inertia;
* collision enabled;
* box collision shape matching visual cube dimensions;
* finite initial state.

---

## 5. Cube mass/inertia

Use one simple deterministic placeholder cube mass.

Prefer:

`0.25 kg`

for every cube unless the existing visual cube dimensions make this invalid for the installed API.

Compute principal cube inertia from the actual cube dimensions and mass using the standard rigid-box expression.

Do not calibrate density.

Do not optimize mass.

Document that these are toy-model contact parameters.

---

# Initial cube arrangement

## 6. Dynamic release configuration

The accepted Milestone 2 cubes were arranged for static visualization.

For dynamic contact simulation, use a deterministic, non-overlapping release arrangement located in the same general pile region near the bucket.

Requirements:

* 30 cubes;
* same colors;
* same cube size;
* compact arrangement;
* small positive separation between initial collision shapes;
* lowest cubes initially slightly above the platform;
* no severe initial penetration;
* no random seed dependency unless the seed is fixed and documented.

Do not redesign the whole scene.

The purpose is only to allow cubes to fall and form a dynamic pile.

---

# Fixed contact environment

## 7. Platform

The accepted platform remains fixed.

Add collision geometry matching its existing dimensions and pose.

Enable collision.

Do not alter its appearance, position, dimensions, lighting, or material appearance.

---

## 8. Container

The receiving container remains fixed.

Enable collision on:

* floor;
* four walls.

Use box collision shapes matching the current procedural geometry.

Do not change container dimensions or position.

---

## 9. Bucket

The excavator remains fixed in the accepted ready-to-scoop pose.

The bucket must have collision geometry sufficient for cube interaction.

Use simple box collision primitives corresponding to the existing procedural bucket pieces where practical.

Requirements:

* bucket remains fixed;
* collision enabled;
* no bucket motor;
* no bucket movement;
* no contact geometry for the entire excavator unless required.

For this milestone, enable excavator collision only where needed to demonstrate cube ↔ bucket interaction.

Prefer bucket-only excavator collision.

Do not enable unnecessary track/boom/cabin collision.

---

# No control in contact scene

## 10. Frozen excavator

This milestone isolates contacts.

Do not use:

* torque motors;
* PD control;
* mechanical joint motion;
* the Milestone 4 target trajectories.

The excavator is fixed for the contact scene.

`controlled_scene.py` remains unchanged.

---

# Required implementation

## 11. Contact scene module

Create:

`src/chrono_ai_excavator/contact_scene.py`

Provide a focused API for:

* building the contact-enabled scene;
* accessing all 30 dynamic cubes;
* accessing platform;
* accessing container collision bodies;
* accessing bucket collision bodies;
* exposing contact-material metadata;
* exposing cube mass/inertia metadata;
* running a deterministic dynamic-pile scenario;
* running small contact validation probes;
* validating finite states;
* returning concise result metadata.

Do not create a generic contact framework.

Do not perform broad refactoring of existing scene modules.

Reuse existing metadata/builders only where it can be done without changing accepted previous-milestone behavior.

---

# Main dynamic-pile scenario

## 12. Simulation

Run one deterministic gravity-settling simulation.

Suggested baseline:

* timestep: `0.002 s`
* simulated duration: `3.0 s`

These values may be minimally adjusted only if required for stable execution.

Do not optimize timestep.

Do not perform parameter sweeps.

Record any change.

---

## 13. Main scenario acceptance

The 30-cube pile scenario must satisfy:

1. exactly 30 dynamic cubes exist;
2. all cube positions and rotations remain finite;
3. all cube linear/angular velocities remain finite;
4. active contact count becomes greater than zero;
5. peak active contact count is greater than zero;
6. no cube passes materially through the platform;
7. no cube falls outside the platform because of numerical instability;
8. cubes visibly fall under gravity;
9. cubes form a physically plausible settled or near-settled pile;
10. no numerical explosion occurs.

For platform penetration use a small explicit numerical tolerance based on cube size.

Do not silently use a large tolerance.

Report the tolerance.

---

## 14. Settling criterion

At the end of the 3-second scenario, calculate:

* maximum cube linear speed;
* maximum cube angular speed;
* final contact count.

Use a practical demonstrator criterion:

* maximum linear speed ≤ `0.25 m/s`

Do not add a strict angular-speed acceptance limit unless required by an observed failure.

Report angular speed diagnostically.

If the pile is still clearly moving after 3 seconds but otherwise stable:

STOP and report the result.

Do not simply extend simulation indefinitely.

---

# Contact pair validation

## 15. Cube ↔ platform

Verify with the 30-cube main scenario that cube/platform contact occurs.

Use installed contact-count/reporting capabilities where practical.

At minimum, physical outcome must prove cubes are supported by the platform rather than passing through it.

---

## 16. Cube ↔ cube

Verify that cube/cube contact occurs during pile formation.

Do not merely infer it from cube count.

Use contact reporting if the installed binding provides a simple reliable way.

If pair identification through the Python contact callback is unexpectedly complex, a separate deterministic two-cube physical probe is acceptable.

Do not build a callback framework.

---

## 17. Cube ↔ container

Create one small display-free validation probe if necessary.

Use:

* the same contact material;
* the same cube collision shape;
* the actual container collision geometry.

Drop one temporary probe cube into the container.

Verify:

* finite motion;
* cube is stopped/supported by container floor;
* it does not pass through floor/walls;
* contact occurs.

The temporary probe cube is test-only and does not change the 30-cube main scene.

---

## 18. Cube ↔ bucket

Create one small display-free validation probe if necessary.

Use:

* the actual fixed bucket collision geometry;
* one temporary cube;
* gravity.

Position the probe deterministically above an exposed bucket collision surface.

Verify:

* finite motion;
* contact occurs;
* the cube does not pass straight through the bucket collision geometry.

This probe is validation-only.

Do not move the bucket.

Do not create scoop motion.

---

# Contact counting

## 19. Contact metadata

Use the simplest binding-compatible method available.

Prefer:

* `system.GetNumContacts()`

or:

* `system.GetContactContainer().GetNumContacts()`

if exposed in the installed binding.

Probe the installed API minimally.

Do not create a permanent custom contact-reporting framework unless exact pair identification cannot otherwise be validated.

---

# Interactive viewer

## 20. Viewer

Create:

`scripts/show_contact_scene.py`

Default behavior:

* build the contact scene;
* use the accepted external camera;
* use the accepted custom lighting;
* start with the deterministic 30-cube release arrangement;
* run gravity dynamics;
* visibly show cubes falling and settling;
* leave excavator fixed;
* leave bucket fixed;
* continue displaying the settled scene until the user closes the window.

Do not animate the excavator.

Do not add HUD.

Do not add force arrows.

---

## 21. Headless mode

Support:

```text
python scripts/show_contact_scene.py --headless-check
```

Headless mode must run:

1. 30-cube pile scenario;
2. cube/platform validation;
3. cube/cube validation;
4. cube/container probe;
5. cube/bucket probe.

No Irrlicht window.

Return nonzero if any required criterion fails.

Print concise results including:

* cube count;
* simulated duration;
* timestep;
* peak contact count;
* final contact count;
* maximum final cube linear speed;
* maximum final cube angular speed;
* platform penetration result;
* cube/platform result;
* cube/cube result;
* cube/container result;
* cube/bucket result;
* measured simulation-loop wall time.

---

# Tests

## 22. Automated tests

Create:

`tests/test_contact_scene.py`

Use `unittest`.

Retain all existing 38 tests.

Cover at least:

* `ChSystemNSC` contact scene;
* gravity vector;
* exactly 30 cubes;
* all cubes dynamic;
* positive cube mass;
* positive cube inertia;
* cube collision enabled;
* platform fixed and collidable;
* container fixed and collidable;
* bucket contact geometry present;
* contact-material parameters;
* deterministic release configuration;
* no initial severe penetration;
* pile simulation finite;
* contact count becomes positive;
* platform penetration criterion;
* final speed criterion;
* cube/platform probe PASS;
* cube/cube probe PASS;
* cube/container probe PASS;
* cube/bucket probe PASS;
* controlled scene remains unchanged;
* no motors in contact scene;
* deterministic metadata.

Tests must be display-free.

Do not weaken previous tests.

---

# Project tracking

## 23. Record final Milestone 4 closeout commit

Add if absent:

* event_id: `M4-FINAL-CLOSEOUT-COMMIT-PUSH-001`
* milestone: `M4`
* started_at: `2026-08-09T23:05:07+03:00`
* ended_at: `2026-08-09T23:05:09+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Committed and pushed the final Milestone 4 merge-closeout documentation on main.`
* human_active_minutes: `0.03`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `Git commit 978740650388263531d0606451a1ee0be5298a86`
* estimate_quality: `measured`
* notes:
  `Local and remote main were verified at the same commit. Network time is not simulation or computation time.`

---

## 24. Record Milestone 5 branch creation

Add if absent:

* event_id: `M5-BRANCH-CREATION-001`
* milestone: `M5`
* started_at: `2026-08-09T23:07:23+03:00`
* ended_at: `2026-08-09T23:07:25+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Created and published the Milestone 5 contact-dynamic-cubes feature branch from the fully closed Milestone 4 main branch.`
* human_active_minutes: `0.03`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `/tmp/chrono_ai_excavator_step_09a_create_m5_branch.txt and starting commit 978740650388263531d0606451a1ee0be5298a86`
* estimate_quality: `measured`
* notes:
  `Local and remote feature/contact-dynamic-cubes branches were verified at the same starting commit.`

Preserve LF endings.

---

# 25. Measure Codex development effort

At actual execution start record an ISO-8601 system-clock timestamp.

After successful prescribed verification record end timestamp.

If this task succeeds, add:

* event_id: `M5-CODEX-CONTACT-DYNAMICS-001`
* milestone: `M5`
* activity_category: `codex_development`
* actor: `codex`
* tool: actual Codex CLI/version and `gpt-5.6-sol`
* description:
  `Implemented Milestone 5 NSC contact physics and dynamic-cube validation.`
* ai_wall_seconds: measured wall seconds
* iteration_type: `initial`
* ai_result_status: `pending_review`
* estimate_quality: `measured`
* evidence:
  `prompts/018_milestone_5_contact_dynamic_cubes.md and Codex task transcript`

Do not fabricate timing.

If the task stops on failure, report measured time but do not record it as accepted.

---

# 26. Measure contact-simulation wall time

Measure actual wall time spent only inside:

* main 30-cube simulation loop;
* required contact probe simulation loops.

Expose this as a headless result.

After successful verification add:

* event_id: `M5-CONTACT-SIMULATION-001`
* milestone: `M5`
* activity_category: `simulation`
* actor: `project_chrono`
* tool: `Project Chrono / PyChrono`
* description:
  `Executed the Milestone 5 30-cube NSC settling scenario and required contact validation probes.`
* compute_wall_seconds: measured simulation-loop wall seconds
* iteration_type: `initial`
* ai_result_status: `accepted`
* estimate_quality: `measured`
* evidence:
  `scripts/show_contact_scene.py --headless-check`

Do not include imports, tests, documentation, or Git time.

---

# Documentation

## 27. README

Update minimally.

State:

* Milestone 4 remains complete;
* Milestone 5 is in progress;
* NSC contact scene implemented;
* 30 dynamic cubes implemented;
* gravity enabled;
* platform/cube/container/bucket contact implemented;
* headless contact validation available;
* human visual review pending.

Still future:

* moving controlled excavator with contacts;
* scoop/dump cycle;
* excavation state machine;
* telemetry/HUD;
* active-contact visualization;
* bucket camera;
* cabin camera;
* video.

Do not mark Milestone 5 complete.

---

## 28. Technical report

Document:

* Milestone 5 objective;
* NSC contact formulation;
* contact materials and values;
* dynamic cube mass/inertia;
* release configuration;
* platform collision;
* container collision;
* bucket collision;
* fixed-excavator isolation strategy;
* timestep/duration;
* 30-cube settling result;
* contact counts;
* penetration check;
* final speed result;
* four contact pair validations;
* simulation wall time;
* limitations.

State:

> **Milestone 5 contact physics and dynamic cubes are implemented and awaiting human review.**

Do not describe moving scoop behavior as implemented.

---

# 29. Preserve this task

Save this complete specification as:

`prompts/018_milestone_5_contact_dynamic_cubes.md`

Do not alter prompts 001 through 017.

---

# Verification environment

The Codex shell may not expose a bare `python` command.

Therefore, run all Python verification explicitly through the existing Conda environment.

Use exactly this style:

```text
conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python ...
```

Do not treat absence of bare shell `python` as a project failure.

---

# Verification sequence

Run in this order:

```text
conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python scripts/check_environment.py

conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python scripts/show_contact_scene.py --headless-check

conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python -m unittest discover -s tests -v

conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python -m compileall -q src scripts tests

conda run --no-capture-output -n chrono \
  env PYTHONPATH="$PWD/src" \
  python scripts/summarize_project_tracking.py

git diff --check
git status --short --branch
```

If any prescribed check fails:

STOP.

Report the exact failure.

Do not automatically expand scope into a repair.

A narrow installed-binding API adaptation may be diagnosed, but do not implement an unapproved architecture change.

Do not open Irrlicht during automated verification.

---

# Strict scope exclusions

Do not:

* modify Milestone 4 controller;
* combine control and contact;
* move excavator joints;
* add gravity compensation;
* add scoop motion;
* add dump motion;
* add excavation state machine;
* add contact-force HUD;
* add force arrows;
* add telemetry;
* add active-contact coloring;
* add bucket camera;
* add cabin camera;
* add camera animation;
* add PDF;
* add presentation;
* add video;
* add FFmpeg;
* add CI;
* add dependencies;
* add CAD;
* add meshes;
* optimize performance;
* perform broad refactoring;
* switch branches;
* commit;
* push.

---

# Completion report

Report only:

1. files created or modified;
2. contact-scene architecture;
3. NSC material parameters;
4. cube mass/inertia policy;
5. release arrangement;
6. timestep and simulated duration;
7. 30-cube pile result;
8. peak and final contact count;
9. final maximum linear/angular cube speeds;
10. platform penetration result/tolerance;
11. cube/platform result;
12. cube/cube result;
13. cube/container result;
14. cube/bucket result;
15. measured contact-simulation wall time;
16. headless-check result;
17. unittest count/result;
18. compilation result;
19. tracking-summary result;
20. `git diff --check` result;
21. branch, HEAD, upstream, and worktree status;
22. M4 final-closeout ledger event status;
23. M5 branch ledger event status;
24. measured Codex wall time;
25. items requiring human visual review;
26. confirmation that Milestone 4 control source was unchanged;
27. confirmation that control and contact were not combined;
28. confirmation that no excavation sequence, telemetry, cameras, PDF, presentation, or video were added;
29. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
