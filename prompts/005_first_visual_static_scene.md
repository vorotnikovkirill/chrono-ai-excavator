# Milestone 2 — First Visual Static Scene

## Objective

Create the first visually meaningful Project Chrono scene for the Chrono AI Excavator project.

The result must be a bright, recognizable, interactive static scene showing:

* an original block-style toy excavator;
* a construction platform;
* a pile of colored cubes;
* a receiving container;
* a clean external camera composition.

The scene must open in an interactive Irrlicht window so the project owner can visually inspect the model.

This milestone is intentionally visual and static.

Do not implement excavator dynamics, joints, motors, contacts, control, telemetry, alternative cameras, or video generation.

---

## Repository state

Work only in:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`feature/first-visual-scene`

Expected starting commit:

`77ddb26bd263ae477ff5ce8bdcaeb3d9f1de23a6`

The branch already exists locally and remotely.

Do not switch branches.

Do not commit or push.

---

## Project priorities

The main project rule is:

> **Fast, clear, and visually strong. No unnecessary depth.**

Before adding any feature, determine whether it is required to display and verify the first static scene.

Prefer simple procedural primitives over external assets or speculative architecture.

---

## Language and public-project rules

All repository content must remain in English:

* source code;
* comments and docstrings;
* command-line messages;
* tests;
* documentation;
* future display labels.

The repository is public.

Use only original procedural geometry.

Do not:

* copy a specific LEGO model or construction set;
* use LEGO branding;
* import proprietary CAD;
* download third-party geometry;
* add textures or assets with unclear redistribution rights;
* include confidential or employer-related material.

---

## Verified environment

* macOS arm64
* Conda environment: `chrono`
* Python: 3.12.13
* `pychrono`: available
* `pychrono.irrlicht`: available
* `pychrono.postprocess`: available
* `pychrono.vsg`: unavailable and not required
* FFmpeg: unavailable and not required
* pytest: not installed
* standard-library `unittest`: available

Do not install, remove, or upgrade packages.

Inspect the installed PyChrono API when necessary rather than assuming an API from another version.

---

# Required visual composition

## 1. Overall scene

Use a right-handed Project Chrono scene with the vertical axis consistent with the installed examples.

Create a clean toy-like construction scene containing:

* one large fixed platform;
* one original block-style excavator;
* approximately 24–36 colored cubes arranged as a compact pile;
* one open receiving container;
* a neutral background and useful lighting;
* a perspective external camera framing the complete scene.

The first camera view should immediately show:

* the full excavator;
* the cube pile;
* the container;
* enough platform around them to understand the intended scoop-and-dump task.

The scene should not appear empty or excessively zoomed out.

---

## 2. Excavator appearance

The excavator must be recognizable from the first frame.

Use only procedural primitive geometry, such as boxes and cylinders.

Include visually distinct components:

* left and right track assemblies;
* lower chassis;
* rotating-platform visual section;
* cabin;
* counterweight or rear body;
* boom;
* stick;
* bucket;
* visible pivot-location details where useful.

The excavator should use a bright construction-toy palette:

* yellow or warm orange main structure;
* dark tracks and chassis;
* dark or blue-tinted cabin windows;
* restrained metallic or dark pivot details.

The excavator should be shown in a static **ready-to-scoop pose**:

* boom extending toward the cube pile;
* stick angled downward;
* bucket near the front of the pile;
* no severe visual intersections between components.

This is visual geometry only.

Do not create functional joints, constraints, or motors.

---

## 3. Platform

Create a large fixed platform with:

* sufficient thickness to be clearly visible;
* a neutral dark-gray or concrete-like color;
* dimensions large enough for the complete composition;
* no external texture dependency.

Optional simple edge markings are allowed only if they are implemented with procedural primitives and materially improve the scene.

Do not add terrain simulation.

---

## 4. Colored cubes

Create approximately 24–36 cubes.

Requirements:

* several bright colors;
* consistent toy-like dimensions;
* arranged as a compact, visually interesting pile;
* positioned near the bucket;
* no dynamics or falling behavior;
* no contact simulation.

The cubes may be fixed for this static milestone.

Avoid placing them in a perfect grid. Use a deterministic arrangement that resembles a loose pile while remaining visually stable.

---

## 5. Receiving container

Create a simple open-top container using procedural box primitives.

It must include:

* a floor;
* four visible walls;
* a contrasting bright color;
* sufficient size to visibly receive cubes in a future milestone;
* placement reachable by a future turret rotation.

Do not implement collision or physical loading behavior in this milestone.

---

# Required implementation

## 6. Static-scene module

Create a focused module such as:

`src/chrono_ai_excavator/static_scene.py`

It should provide a small public API that can:

* build the static Project Chrono system;
* create and register the named visual objects;
* expose lightweight scene metadata needed for testing;
* validate important static-scene properties without opening a display.

Avoid a general scene framework or speculative architecture.

Use clear names for major components.

A simple dataclass or similarly lightweight structure is acceptable when it has an immediate practical purpose.

---

## 7. Interactive viewer script

Create:

`scripts/show_static_scene.py`

Default behavior:

* build the scene;
* initialize Irrlicht;
* open an interactive display window;
* set a useful initial external camera;
* add lighting and a neutral background;
* display the complete static scene;
* allow normal Irrlicht camera interaction;
* print concise English launch information.

The window title should clearly identify the project and milestone.

The script must also support a display-free mode such as:

```bash
python scripts/show_static_scene.py --headless-check
```

In headless-check mode it must:

* build the complete scene;
* run static validation;
* print a concise object summary;
* exit without opening an Irrlicht window;
* return nonzero if validation fails.

Do not automatically start a long simulation loop in headless mode.

---

## 8. Static validation

Validate at least:

* required major excavator components exist;
* both track assemblies exist;
* boom, stick, and bucket exist;
* platform exists;
* container exists;
* cube count is inside the specified range;
* object names are unique;
* important dimensions are positive;
* all objects use finite positions;
* the main composition remains within a reasonable bounding region;
* the scene can be built without a display.

Do not treat visual taste as an automated test. Human visual review remains mandatory.

---

## 9. Tests

Create or update display-free tests using `unittest`.

Cover at least:

* static scene construction;
* unique named components;
* required excavator visual components;
* cube-count range;
* deterministic scene metadata;
* positive dimensions;
* finite coordinates;
* headless validation success.

Tests must:

* run without opening Irrlicht;
* be quick;
* avoid optional external packages;
* remain compatible with the existing `src` layout.

Do not remove or weaken existing scaffold tests.

---

## 10. Documentation

Update `README.md` concisely:

* Milestone 2 is in progress;
* the first static scene has been implemented for visual review;
* provide the headless-check command;
* provide the interactive-view command;
* state clearly that dynamics, joints, contacts, control, telemetry, bucket camera, cabin camera, rendering, and video remain future work.

Update `docs/technical_report.md`:

* document the purpose of the static visual milestone;
* describe the procedural scene composition;
* distinguish visual bodies from future dynamic bodies;
* state that human visual acceptance is still pending;
* document limitations;
* identify the next step as visual review and refinement rather than dynamics.

Do not generate a PDF or presentation yet.

The initial presentation begins only after the project owner accepts the visual scene.

---

## 11. Preserve this task

Preserve this complete task as:

`prompts/005_first_visual_static_scene.md`

Do not alter prompts 001 through 004.

---

## 12. Project tracking

Do not invent task start or end timestamps.

Do not estimate Codex wall time inside the repository.

The external orchestration log will provide actual timing evidence after execution.

You may update documentation to state that Milestone 2 has started, but do not add fabricated measured ledger entries.

---

# Verification

Run inside the existing `chrono` Conda environment:

```bash
python scripts/check_environment.py
python scripts/show_static_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

Also verify:

* the current branch remains `feature/first-visual-scene`;
* `origin` is unchanged;
* no commit or push was performed;
* no large file was introduced;
* no Cyrillic repository text was introduced;
* no external asset was added;
* no display window was opened during automated verification;
* no out-of-scope dynamic functionality was implemented.

Do not run the interactive viewer as part of automated verification.

The project owner will run the interactive viewer manually after reviewing the Codex report.

---

# Explicit scope exclusions

Do not implement:

* functional revolute joints;
* constraints;
* motors;
* torque control;
* position control;
* state-machine control;
* gravity-driven excavator motion;
* cube dynamics;
* contact materials;
* cube-to-cube contact;
* bucket-to-cube contact;
* terrain;
* real track dynamics;
* hydraulic cylinders;
* telemetry;
* HUD;
* joint highlighting;
* main-camera animation;
* bucket-mounted camera;
* cabin/operator camera;
* screenshot automation;
* rendered frame output;
* PDF;
* presentation;
* video;
* FFmpeg;
* CI;
* GitHub Actions;
* new dependencies;
* CAD import;
* external meshes;
* speculative frameworks.

---

# Completion report

At the end, report:

1. every file created or modified;
2. static-scene architecture;
3. excavator components created;
4. platform, cube, and container composition;
5. interactive-view command;
6. headless-check command and result;
7. unittest command and result;
8. compilation result;
9. tracking-summary result;
10. Git diff and branch status;
11. visual assumptions that require human review;
12. known visual limitations;
13. exact confirmation that no package installation, commit, push, remote modification, dynamic physics, joints, control, camera variants, rendering output, PDF, presentation, or video was added.
