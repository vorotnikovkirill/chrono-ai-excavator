# Chrono AI Excavator — Living Technical Report

## 1. Project objective

The project demonstrates an end-to-end public engineering workflow that produces a fast, clear, and visually strong Project Chrono result. **Implemented:** the Milestone 1 foundation and the first fixed procedural scene for Milestone 2 visual review. **Current limitation:** no dynamic excavator simulation exists yet.

## 2. Demonstrator concept

The demonstrator concept is an original block-style toy excavator that will eventually scoop colored rigid cubes from a platform, rotate, and dump them into a container. The recognizable static composition now exists, but the scoop-and-dump behavior remains future work. It does not reproduce a specific commercial toy set or use protected branding.

## 3. ChatGPT → Codex → Project Chrono workflow

ChatGPT supports engineering discussion and decomposition; Codex implements and verifies bounded milestones; Project Chrono will execute multibody and contact simulation. Later outputs will include telemetry, public technical documentation, a presentation, and a final video. The current repository preserves the specification and records tool, time, iteration, and cost evidence.

## 4. Scope-control principle

Every addition must either satisfy the current milestone or materially improve the final video. Speculative abstractions and unnecessary physical depth are excluded. Human active effort, AI wall time, and computation time are tracked independently.

## 5. Planned mechanical architecture

The static visual excavator uses fixed, collision-free Project Chrono bodies with original box and cylinder geometry. Named components include two track assemblies and rollers, a lower chassis, a visual rotating platform, cabin and windows, rear body and counterweight, boom, stick, bucket, and dark pivot details. These bodies are presentation geometry only; they are not the future dynamic-body decomposition. Real track dynamics, CAD import, hydraulics, flexible bodies, and deformation remain excluded.

## 6. Planned joint and torque-control concept

Future revolute joints will represent swing, boom, stick, and bucket motion. A minimal controller is expected to command joint torque toward a scripted motion target, subject to what is visually useful and stable. No joints, motors, controllers, control state machine, or calibration exists yet.

## 7. Planned contact scene

The scene includes a thick fixed dark-gray platform, a deterministic loose pile of 30 bright fixed cubes near the bucket, and a contrasting open orange receiving container made from a floor and four walls. The composition communicates the intended task, but no collisions, contact materials, solver behavior, cube dynamics, or loading behavior exists.

## 8. Planned visualization and camera views

The Milestone 2 script provides one perspective external Irrlicht camera, a neutral blue-gray background, the procedural platform, and simple useful lighting. Normal Irrlicht interaction lets the project owner orbit and inspect the complete fixed scene. Alternative cameras, HUD, camera switching, animation, plots, frame output, and video do not exist.

## 9. Milestone 2 static visual scene

The purpose of this milestone is visual communication and human acceptance before any physical complexity is introduced. `static_scene.py` builds the complete display-independent Chrono system and exposes immutable object metadata, a named body registry, camera framing, validation, and a concise summary. `show_static_scene.py` uses that same build path for either headless validation or the interactive Irrlicht window.

The ready-to-scoop excavator faces the compact cube pile with its boom raised, stick descending, and bucket close to the pile. The receiving container is offset across the platform so a future upper-structure rotation could reach it. The palette deliberately separates warm construction components, dark running gear, blue-tinted windows, multicolored cubes, and the orange container.

The static-scene implementation is complete. The accepted composition contains the procedural excavator, platform, 30 colored cubes, receiving container, lighting, and external camera. Automated checks verify names, required components, cube count, dimensions, finite transforms, a reasonable composition bound, fixed bodies, and deterministic metadata without opening a display. They cannot assess silhouette, occlusion, perceived scale, color balance, or camera appeal.

The project owner performed the separate interactive human visual review and accepted the composition without requesting visual corrections. Human visual acceptance is distinct from automated verification. The temporary Step 06D log is unavailable, so the viewer exit status is `unavailable` and was not inferred; this does not invalidate the recorded human acceptance.

Display-free validation passed, including all 14 automated tests during the accepted verification. The static-scene implementation was committed as `d61e8369a843f4bce0c7f33842d5649ad87bf922` (`feat: add first static excavator scene`). Tracking guidance and finalization were committed as `26a7b073539d0dbb0f0450d96785260020025f6a` and `b3cc151325f442eda519726b31a029cd8201eaa5`.

The accepted feature branch was fast-forward merged into `main` and pushed from `2026-08-09T09:22:16+03:00` through `2026-08-09T09:22:19+03:00`, a measured three-second interval. Local and remote `main` were synchronized at `b3cc151325f442eda519726b31a029cd8201eaa5`. The merge introduced no separately measurable additional software or infrastructure cost, and merge/network time is not classified as simulation or computation time.

**Milestone 2 is complete.**

## 10. Milestone 0 preflight results

**Verified findings:** macOS 26.6 arm64, Python 3.12.13 in the `chrono` Conda environment, PyChrono, `ChSystemNSC`, `ChBody`, `ChLinkMotorRotationTorque`, Irrlicht, and postprocess are available. VSG and FFmpeg are unavailable and unnecessary for Milestone 1. A minimal gravity smoke test passed during preflight. Three runs were needed: one initial run and two corrections. The source brief supplies the historical timestamps and evidence paths.

## 11. Milestone 1 scope and outputs

**Accepted, published, and implemented:** repository policy, packaging metadata, package version, display-free environment verification, deterministic tests, standard-library project-ledger validation and summary, a living report, and preserved prompts. Milestone 1 is fully closed. The initial local commit was created and the accepted scaffold was published as the public repository [`vorotnikovkirill/chrono-ai-excavator`](https://github.com/vorotnikovkirill/chrono-ai-excavator).

The published commit is `b94197bd10a0f227bad7aa915a48b8e7aac6a323`. Publication ran from `2026-08-05T21:22:33+03:00` through `2026-08-05T21:22:38+03:00`, a measured five-second interval. Local and remote `main` were verified at the same commit. Publication introduced no separately measurable software or infrastructure cost, and network publication time is not classified as simulation or computation time.

One publication orchestration attempt failed before publication. Codex task execution never started because a global approval argument was placed after the `exec` subcommand, and unittest discovery omitted `PYTHONPATH=src`. Environment verification, the tracking summary, and compilation still passed. These were orchestration defects and did not invalidate the accepted scaffold. Pytest remains absent from the `chrono` environment, package installation remains prohibited, and the display-free tests run through standard-library `unittest`.

## 12. Project effort, tooling, and cost ledger

The CSV ledger records calendar duration without overlap double-counting and reports human active effort, AI-assisted development wall time, simulation/computation wall time, documented software and infrastructure cost, and iteration/rework counts. Historical project-owner active effort is an approximate 25 minutes with a plausible 20–30 minute range. Historical ChatGPT generation time and command-review effort are unknown and are not invented. Subscription costs and incremental ChatGPT/Codex project costs are not separately measurable from available evidence.

Closeout totals are generated by `scripts/summarize_project_tracking.py` and are recorded after final verification below. Human, AI, and computation time remain separate; measured, timestamp-derived, and approximate values are not conflated.

Latest tracking totals:

- overlap-safe calendar duration: 1 hour 18 minutes 0 seconds;
- human active effort: 36.7 minutes;
- Codex/AI wall time: 10 minutes 11 seconds;
- simulation/computation wall time: 30 seconds;
- documented attributable software and infrastructure cost: none measurable;
- iterations: 13 initial, 8 corrections, 4 repeated runs, and 0 rework events;
- AI-result counts: 15 accepted, 5 accepted with corrections, 1 rejected, and 0 pending review;
- estimate quality: 10 measured, 19 timestamp-derived, and 2 approximate records.

Required final project metrics are:

- calendar duration;
- human active effort;
- AI-assisted development effort;
- simulation wall-clock time;
- software and infrastructure cost;
- initial, correction, repeat, and rework counts.

## 13. Current limitations

The accepted scene remains intentionally static and visually approximate. Track belts are block silhouettes, the bucket is assembled from simple boxes, and pivot details are decorative. There are no dynamic bodies, joints, motors, controllers, contacts, telemetry, alternative cameras, rendered frames, PDF, presentation, or video. The living report will later become the source for the public technical PDF.

## 14. Next milestone

### Milestone 3 — Mechanical Architecture

Milestone 3 converts the accepted visual excavator into a minimal articulated topology while retaining the fixed platform, 30 fixed cubes, receiving container, lighting, and external camera. The accepted Milestone 2 static module remains the frozen visual reference; the new mechanical module groups its excavator primitives onto five primary bodies without redesigning their initial appearance.

The topology is `BASE → UPPER → BOOM → STICK → BUCKET`. `BASE` is fixed; the other four bodies are dynamic. Four `ChLinkLockRevolute` joints provide `J0_SLEW` (BASE–UPPER), `J1_BOOM` (UPPER–BOOM), `J2_STICK` (BOOM–STICK), and `J3_BUCKET` (STICK–BUCKET). The slew axis follows scene vertical Y, while the three arm hinge axes are mutually parallel along scene Z and pass through the accepted visual pivots.

Positive mass and diagonal inertia values are preliminary toy-model mechanical properties for architecture verification only. They are finite placeholders, not calibrated real-excavator properties. Architecture validation uses zero gravity and zero initial velocity so the unactuated mechanism retains its ready-to-scoop pose during a short constraint smoke test.

Display-free validation checks body status and properties, joint names and connectivity, finite pivots and axes, retained environment geometry, absence of motor links and collision response, deterministic metadata, and short-step constraint stability. Motors, controllers, limits, contacts, cube dynamics, telemetry, and camera variants remain intentionally unimplemented.

**Milestone 3 mechanical architecture is implemented and awaiting human review.**
