# Milestone 1 — Public Repository Scaffold and Project Tracking Foundation

## Project

Create the initial public repository scaffold for:

**Chrono AI Excavator**

The project will demonstrate an end-to-end engineering workflow:

**ChatGPT engineering discussion and system decomposition
→ Codex implementation and verification
→ Project Chrono multibody and contact simulation
→ telemetry, technical documentation, presentation, and final video**

The final demonstrator will feature an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container.

The final visualization is planned to include:

* a main cinematic external camera;
* a bucket-mounted camera;
* a cabin/operator-view camera;
* visualization of active joints;
* joint target and actual motion;
* commanded actuator torque;
* contact activity and selected simulation telemetry.

These are roadmap requirements only. Do not implement them in this milestone.

---

## Primary objective

Create a clean, minimal, testable, public-repository foundation.

The project priority is:

> **Fast, clear, and visually strong. No unnecessary depth.**

Do not begin implementing the excavator or simulation architecture during this milestone.

Avoid speculative abstractions. Create only files that have an immediate and clearly documented purpose.

---

## Language policy

All repository content must be written in English, including:

* source code;
* comments and docstrings;
* filenames where practical;
* README and technical documentation;
* prompts;
* tests;
* command-line output;
* chart and figure labels;
* future presentation content;
* future video overlays;
* future Git commit and pull-request text.

The project owner may communicate with ChatGPT in Russian, but nothing written into the public repository should be in Russian.

---

## Public-project and licensing policy

The repository is intended to become public on GitHub.

Use only:

* original source code;
* original procedural geometry;
* assets created specifically for this project;
* third-party assets with clearly documented redistribution rights.

The future excavator must be an original block-style toy excavator.

Do not:

* copy a specific LEGO set;
* use LEGO logos or trademarks as project branding;
* include proprietary CAD geometry;
* add assets with unclear licenses;
* include employer, customer, or confidential information.

Do not create a GitHub remote, GitHub repository, release, issue, pull request, commit, or push during this milestone.

---

## Verified environment

The local environment has already been checked.

* Operating system: macOS 26.6, arm64
* Conda environment: `chrono`
* Python in the environment: 3.12.13
* Required module: `pychrono`
* `ChSystemNSC`: available
* `ChBody`: available
* `ChLinkMotorRotationTorque`: available
* `pychrono.irrlicht`: available
* `pychrono.postprocess`: available
* `pychrono.vsg`: unavailable and not required
* FFmpeg: unavailable and intentionally deferred

Do not install, upgrade, or remove any package.

Do not list `pychrono` as a normal PyPI dependency because it is supplied by the existing Conda environment.

---

# Required repository contents

## 1. `README.md`

Create a concise and accurate README containing:

* project title;
* public-project objective;
* planned ChatGPT → Codex → Project Chrono workflow;
* final demonstrator concept;
* current milestone and status;
* verified environment;
* minimal installation and verification instructions;
* explicit statement that Milestone 1 contains only the repository scaffold, environment checks, project ledger, and documentation foundation;
* short roadmap;
* planned external, bucket, and cabin camera views;
* license information.

Do not claim that excavator geometry, joints, contacts, control, telemetry, cameras, or video already work.

---

## 2. `LICENSE`

Use the MIT License.

* Copyright year: 2026
* Copyright holder: Kirill Vorotnikov

---

## 3. `.gitignore`

Cover at least:

* Python bytecode and caches;
* pytest and coverage caches;
* virtual and Conda environments;
* macOS metadata;
* editor-generated files;
* build artifacts;
* generated run directories;
* raw simulation outputs;
* rendered frame sequences;
* generated videos;
* generated PDF build files.

Do not ignore:

* source documentation;
* project prompts;
* tracking CSV files;
* intentionally selected figures or media committed later.

---

## 4. `pyproject.toml`

Create minimal project metadata.

Requirements:

* package name: `chrono-ai-excavator`;
* Python requirement compatible with Python 3.12;
* `src` package layout;
* package version: `0.1.0`;
* pytest configuration;
* no unnecessary runtime dependencies;
* no speculative optional dependency groups;
* do not declare `pychrono` as a PyPI dependency.

---

## 5. `AGENTS.md`

Create repository instructions for future Codex work.

Include these mandatory rules:

1. Keep all repository content in English.
2. Remain strictly within the current milestone.
3. Optimize for a fast, clear, and visually strong demonstrator.
4. Before adding complexity, determine whether it materially improves the final video or is required for the current milestone.
5. Avoid premature implementation of:

   * CAD import;
   * real track dynamics;
   * hydraulic-system simulation;
   * flexible bodies;
   * structural deformation;
   * optimization;
   * autonomous path planning;
   * advanced physical calibration;
   * unnecessary frameworks.
6. Every significant milestone must update:

   * README;
   * living technical report;
   * project time/tool/cost ledger;
   * relevant tests;
   * preserved Codex prompt.
7. A presentation should be updated only at visually meaningful milestones.
8. Do not commit or push unless explicitly requested.
9. Do not add assets without clear redistribution rights.
10. Do not combine human effort, AI execution time, and computation time into one misleading total.

---

## 6. Python package

Create only:

```text
src/chrono_ai_excavator/__init__.py
```

Expose:

```python
__version__ = "0.1.0"
```

Do not create empty future modules for geometry, contacts, control, rendering, telemetry, or cameras.

---

## 7. Environment verification script

Create:

```text
scripts/check_environment.py
```

It must:

* report Python version and executable;
* import `pychrono`;
* report the PyChrono module path;
* check required Chrono classes;
* detect Irrlicht and postprocess availability;
* report VSG as unavailable without treating that as a failure;
* create a minimal `ChSystemNSC`;
* explicitly set gravity;
* add one free rigid body;
* advance dynamics for a short deterministic interval;
* verify that the body moves downward;
* print a concise English PASS/FAIL summary;
* return a nonzero exit status if a required check fails.

The script must run from the repository root inside the existing `chrono` Conda environment.

---

## 8. Automated tests

Create a small, deterministic, fast test suite covering:

* package import;
* package version;
* required Project Chrono classes;
* gravity smoke test;
* visualization capability detection;
* VSG absence not causing test failure;
* project-tracking schema validation;
* project-tracking summary calculations using a small temporary fixture.

Tests must not require a display window.

Do not add CI in this milestone.

---

# Continuous project effort, tooling, and cost ledger

Starting with this milestone, maintain a separate reproducible project ledger alongside technical development.

Create:

```text
project_tracking/
├── README.md
├── events.csv
└── software_inventory.csv
```

Also create a minimal standard-library-only summary utility:

```text
scripts/summarize_project_tracking.py
```

Do not introduce a database, web dashboard, external project-management system, or third-party data-analysis dependency.

---

## 9. `project_tracking/README.md`

Document the tracking policy and schema.

The ledger must distinguish:

* ChatGPT discussion and engineering decisions;
* project-owner active effort:

  * task definition;
  * command execution;
  * review;
  * verification;
* Codex execution wall-clock time;
* computation and simulation wall-clock time;
* debugging and corrective iterations;
* repeated runs and rework;
* documentation effort;
* software, versions, licenses, and costs;
* ChatGPT, Codex, API, cloud, storage, or infrastructure expenses;
* whether an AI result was accepted, corrected, or rejected.

Use ISO 8601 timestamps with timezone offsets.

Use these controlled values where applicable.

### Activity category

* `chatgpt_discussion`
* `human_task_definition`
* `human_execution`
* `human_review`
* `codex_development`
* `verification`
* `computation`
* `simulation`
* `debugging`
* `rework`
* `documentation`
* `project_management`

### Actor

* `project_owner`
* `chatgpt`
* `codex`
* `project_chrono`
* `system`
* `mixed`

### AI result status

* `accepted`
* `accepted_with_corrections`
* `rejected`
* `pending_review`
* `not_applicable`

### Estimate quality

* `measured`
* `derived_from_timestamps`
* `approximate_estimate`

### Iteration type

* `initial`
* `correction`
* `repeat`
* `rework`
* `not_applicable`

Explain that overlapping human, AI, and computation periods must remain separate and must not be added together as though they were sequential labor.

---

## 10. `project_tracking/events.csv`

Use this header:

```text
event_id,milestone,started_at,ended_at,activity_category,actor,tool,description,human_active_minutes,ai_wall_seconds,compute_wall_seconds,iteration_type,ai_result_status,cost_amount,cost_currency,evidence,estimate_quality,notes
```

Create retrospective entries for work completed before the tracking policy was introduced.

Historical facts available:

### Project discussion

* Start: `2026-08-03T23:03:06+03:00`
* Tracking-policy introduction: `2026-08-03T23:58:59+03:00`
* Calendar span: 55 minutes 53 seconds
* Human active effort: approximate estimate of 25 minutes
* Note that the plausible range is approximately 20–30 minutes
* Estimate quality: `approximate_estimate`

### Preflight run 1

* Start: `2026-08-03T23:26:02+03:00`
* End: `2026-08-03T23:26:04+03:00`
* Result: core commands found, FFmpeg missing, initial PyChrono output not captured
* Iteration: `initial`
* AI result status: `accepted_with_corrections`
* Compute wall time: 2 seconds
* Evidence: `/tmp/chrono_ai_excavator_step_00.txt`
* Estimate quality: `derived_from_timestamps`

### Preflight run 2

* Start: `2026-08-03T23:27:01+03:00`
* End: `2026-08-03T23:27:05+03:00`
* Result: PyChrono and core classes verified; visualization check contained a Python quoting error; gravity smoke test passed
* Iteration: `correction`
* AI result status: `accepted_with_corrections`
* Compute wall time: 4 seconds
* Evidence: `/tmp/chrono_ai_excavator_step_00a.txt`
* Estimate quality: `derived_from_timestamps`

### Preflight run 3

* Start: `2026-08-03T23:27:49+03:00`
* End: `2026-08-03T23:27:52+03:00`
* Result: Irrlicht and postprocess verified, VSG confirmed unavailable, gravity test passed
* Iteration: `correction`
* AI result status: `accepted`
* Compute wall time: 3 seconds
* Evidence: `/tmp/chrono_ai_excavator_step_00b.txt`
* Estimate quality: `derived_from_timestamps`

Do not invent exact historical ChatGPT generation time or historical command-review effort that cannot be recovered.

Beginning at:

```text
2026-08-03T23:58:59+03:00
```

new records must use actual timestamps and reproducible evidence whenever technically possible.

---

## 11. `project_tracking/software_inventory.csv`

Use this header:

```text
software_name,version,role,license,cost_amount,cost_currency,cost_basis,verification_source,notes
```

Populate only verified or clearly qualified information.

Include:

* macOS 26.6;
* Python 3.12.13 from Conda environment `chrono`;
* Project Chrono/PyChrono, with version marked `not exposed` if unavailable;
* PyChrono Irrlicht module;
* PyChrono postprocess module;
* Git 2.50.1;
* GitHub CLI 2.96.0;
* Codex CLI version only if it can be measured during this task;
* ChatGPT and Codex costs as `not separately measurable` unless an actual amount is available;
* FFmpeg as `not installed`.

For license and cost fields:

* do not guess;
* use `unknown` or `not separately measurable` where evidence is unavailable;
* distinguish total subscription cost from incremental project cost;
* do not claim that a subscription product is free merely because no additional project charge was observed.

---

## 12. Tracking summary script

Create:

```text
scripts/summarize_project_tracking.py
```

Use only the Python standard library.

It must read the CSV files and report:

1. calendar duration;
2. human active effort;
3. Codex/AI-assisted development wall-clock time;
4. simulation and computation wall-clock time;
5. documented software and infrastructure cost;
6. number of initial iterations;
7. number of corrections;
8. number of repeated runs;
9. number of rework events;
10. counts of accepted, corrected, rejected, and pending AI results.

Requirements:

* do not double-count calendar duration;
* do not merge human, AI, and compute time;
* handle empty numeric fields safely;
* clearly distinguish measured values from approximate historical estimates;
* return a nonzero exit status for an invalid schema.

---

# Technical documentation

## 13. `docs/technical_report.md`

Create a lightweight English living technical report with:

1. Project objective
2. Demonstrator concept
3. ChatGPT → Codex → Project Chrono workflow
4. Scope-control principle
5. Planned mechanical architecture
6. Planned joint and torque-control concept
7. Planned contact scene
8. Planned visualization and camera views
9. Milestone 0 preflight results
10. Milestone 1 scope and outputs
11. Project effort, tooling, and cost ledger
12. Current limitations
13. Next milestone

The report must explicitly distinguish:

* implemented functionality;
* planned functionality;
* verified findings;
* assumptions;
* future work.

State that:

* no excavator simulation exists yet;
* no joints or controllers exist yet;
* no cameras exist yet;
* no PDF or presentation is generated in Milestone 1;
* polished PDF and presentation work begins at the first visually meaningful milestone;
* the living report will later become the source for the public technical PDF.

Include the required final project metrics:

* calendar duration;
* human active effort;
* AI-assisted development effort;
* simulation wall-clock time;
* software and infrastructure cost;
* iteration and rework counts.

---

## 14. Preserve this prompt

Keep this exact task specification at:

```text
prompts/001_repository_scaffold.md
```

Do not overwrite or substantially shorten it.

---

# Verification

Run all verification commands inside the existing `chrono` Conda environment.

At minimum, run:

```bash
python scripts/check_environment.py
python scripts/summarize_project_tracking.py
python -m pytest -q
```

Also inspect:

* repository file list;
* Git status;
* generated caches;
* accidentally added large files;
* non-English repository text where reasonably detectable.

Do not install anything.

Do not open an Irrlicht display window.

---

# Explicit scope exclusions

Do not:

* create excavator geometry;
* create platform, cubes, or container geometry;
* implement rigid-body assembly;
* implement joints or motors;
* implement torque controllers;
* implement contact materials;
* implement a state machine;
* implement telemetry collection;
* implement HUD graphics;
* implement camera switching;
* implement bucket or cabin cameras;
* create plots;
* create rendered images;
* create a PDF;
* create a presentation;
* install FFmpeg;
* create CI;
* create GitHub resources;
* commit;
* push;
* add speculative future modules.

The future camera requirements must be documented in the roadmap and report, but not implemented.

---

# Completion report

At the end, report:

1. all files created or modified;
2. verification commands executed;
3. test results;
4. environment smoke-test result;
5. tracking-summary result;
6. retrospective ledger entries created;
7. assumptions and unknown values;
8. scope exclusions respected;
9. current Git status;
10. exact confirmation that no commit, push, GitHub remote, or package installation was performed.

Do not commit or push.
