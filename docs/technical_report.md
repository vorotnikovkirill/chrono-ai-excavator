# Chrono AI Excavator — Living Technical Report

## 1. Project objective

The project demonstrates an end-to-end public engineering workflow that produces a fast, clear, and visually strong Project Chrono result. **Implemented:** the Milestone 1 foundation, the accepted Milestone 2 static scene, the accepted Milestone 3 articulated mechanics, and the accepted Milestone 4 torque actuation and basic joint control. **Current limitation:** contacts, dynamic cubes, and excavation sequencing do not exist yet.

## 2. Demonstrator concept

The demonstrator concept is an original block-style toy excavator that will eventually scoop colored rigid cubes from a platform, rotate, and dump them into a container. The recognizable static composition now exists, but the scoop-and-dump behavior remains future work. It does not reproduce a specific commercial toy set or use protected branding.

## 3. ChatGPT → Codex → Project Chrono workflow

ChatGPT supports engineering discussion and decomposition; Codex implements and verifies bounded milestones; Project Chrono will execute multibody and contact simulation. Later outputs will include telemetry, public technical documentation, a presentation, and a final video. The current repository preserves the specification and records tool, time, iteration, and cost evidence.

## 4. Scope-control principle

Every addition must either satisfy the current milestone or materially improve the final video. Speculative abstractions and unnecessary physical depth are excluded. Human active effort, AI wall time, and computation time are tracked independently.

## 5. Planned mechanical architecture

The static visual excavator uses fixed, collision-free Project Chrono bodies with original box and cylinder geometry. Named components include two track assemblies and rollers, a lower chassis, a visual rotating platform, cabin and windows, rear body and counterweight, boom, stick, bucket, and dark pivot details. These bodies are presentation geometry only; they are not the future dynamic-body decomposition. Real track dynamics, CAD import, hydraulics, flexible bodies, and deformation remain excluded.

## 6. Joint and torque-control concept

Revolute spindle constraints represent swing, boom, stick, and bucket motion. Milestone 4 implements four torque motors and bounded PD control toward deterministic scripted targets, as detailed in Section 15. The demonstrator gains are intentionally uncalibrated, and an excavation control state machine remains future work.

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

- overlap-safe calendar duration: 1 hour 34 minutes;
- human active effort: 40.8 minutes;
- Codex/AI wall time: 21 minutes 57 seconds;
- simulation/computation wall time: 35 seconds;
- documented attributable software and infrastructure cost: none measurable;
- iterations: 27 initial, 12 corrections, 4 repeated runs, and 0 rework events;
- AI-result counts: 20 accepted, 6 accepted with corrections, 1 rejected, and 1 pending review;
- estimate quality: 25 measured, 22 timestamp-derived, and 2 approximate records.

Required final project metrics are:

- calendar duration;
- human active effort;
- AI-assisted development effort;
- simulation wall-clock time;
- software and infrastructure cost;
- initial, correction, repeat, and rework counts.

## 13. Current limitations

The articulated excavator uses preliminary toy-model masses and inertias, while Milestone 4 uses zero gravity to isolate controller behavior. Track belts remain visual, the environment and 30 cubes remain fixed, and pivot markers remain decorative. There are no joint limits, contacts, dynamic cubes, excavation state machine, telemetry, alternative cameras, rendered frames, PDF, presentation, or video. The living report will later become the source for the public technical PDF.

## 14. Milestone 3 mechanical architecture

Milestone 3 converts the accepted visual excavator into a minimal articulated topology while retaining the fixed platform, 30 fixed cubes, receiving container, lighting, and external camera. The accepted Milestone 2 static module remains the frozen visual reference; the new mechanical module groups its excavator primitives onto five primary bodies without redesigning their initial appearance.

The topology is `BASE → UPPER → BOOM → STICK → BUCKET`. `BASE` is fixed; the other four bodies are dynamic. Four `ChLinkLockRevolute` joints provide `J0_SLEW` (BASE–UPPER), `J1_BOOM` (UPPER–BOOM), `J2_STICK` (BOOM–STICK), and `J3_BUCKET` (STICK–BUCKET). The slew axis follows scene vertical Y, while the three arm hinge axes are mutually parallel along scene Z and pass through the accepted visual pivots.

Positive mass and diagonal inertia values are preliminary toy-model mechanical properties for architecture verification only. They are finite placeholders, not calibrated real-excavator properties. Architecture validation uses zero gravity and zero initial velocity so the unactuated mechanism retains its ready-to-scoop pose during a short constraint smoke test.

Display-free validation checks body status and properties, joint names and connectivity, finite pivots and axes, retained environment geometry, absence of motor links and collision response, deterministic metadata, and short-step constraint stability. The accepted verification passed all 30 tests and the 0.005-second zero-gravity constraint smoke test. Final human visual review also passed and confirmed that the corrected J1/J2/J3 decorative pivot markers align with their transverse joint axes.

Two focused corrections were required. First, the installed PyChrono binding returns `ChBodyFrame` wrappers from `GetBody1()` and `GetBody2()` without `GetName()`. Connectivity validation now uses binding-tested direct equality against the exact stored `ChBody` references, preserving all parent/child checks and topology. Second, `ChVisualShapeCylinder` was confirmed to be intrinsically Z-aligned. Decorative Z-axis pivot cylinders now use identity rotation, while Y-axis cylinders rotate intrinsic Z to scene Y with `QuatFromAngleX(-π/2)`. Mechanical joint frames and pivot positions were unchanged.

The accepted implementation is commit `408b50f231a4b2e3edfdc52ef51b1e13240b5f3f` (`feat: add excavator mechanical architecture`), and Milestone 3 tracking was finalized in `887a97be2eb5b68374bafc10104eff392bf41478` (`docs: finalize milestone 3 tracking`). Feature closeout documentation was committed as `578d2b3290969cbd4e04dc98e08534b41e60aafc` (`docs: close milestone 3`) from `2026-08-09T11:34:37+03:00` through `2026-08-09T11:34:39+03:00`.

The accepted feature branch was then fast-forward merged into `main` and pushed from `2026-08-09T11:37:14+03:00` through `2026-08-09T11:37:16+03:00`. Local and remote `main` were synchronized at `578d2b3290969cbd4e04dc98e08534b41e60aafc`. These Git operations introduced no separately measurable additional software or infrastructure cost, and their network time is not classified as simulation or computation time.

**Milestone 3 is complete.**

The next planned stage remains future work and is named only at a high level: actuation and control foundation.

## 15. Milestone 4 torque actuation and basic joint control

Milestone 4 replaces the four revolute constraints in a separate controlled-scene build with exactly four `ChLinkMotorRotationTorque` links. Each torque motor embeds the corresponding spindle constraint, so no duplicate revolute constraint is stacked on the same axis. The accepted Milestone 3 mechanical scene remains an independent reference model.

Each joint uses bounded PD control, `τ = clamp(Kp(θref−θ) + Kd(ωref−ω), −τmax, +τmax)`, with gains in N·m/rad and N·m·s/rad and torque limits in N·m. These values are deterministic toy-model controller placeholders rather than calibrated excavator actuators. Target deltas are +12° slew, +8° boom, −8° stick, and +10° bucket, using the one-second cubic transition `s(u)=3u²−2u³` and its analytic velocity.

Motion `(Kp, Kd)` values are `(1500, 2500)` for slew, `(2000, 1200)` for boom, `(1500, 700)` for stick, and `(800, 200)` for bucket. Zero-reference hold values are `(1500, 2500)`, `(6500, 2800)`, `(6000, 2200)`, and `(1600, 500)`, respectively. Torque limits remain 800, 800, 600, and 300 N·m. The one-second transition is followed by a deterministic two-second settling interval.

Zero gravity isolates actuator and feedback behavior from gravity compensation, payload, and contact. Independent validation commands each joint while the other three hold zero reference; a combined smoke test commands all four. The checks require finite state, correct motion direction, final error within 1.5°, uncommanded motion within 0.5°, and strict torque saturation. The measured simulation-loop wall time is recorded separately from human and AI effort in the project ledger.

The accepted independent-joint and combined headless simulation loops took `0.266271 s` of measured wall time.

The corrected independent results are: slew 12.71° final with −0.71° error, 0.09° maximum hold deviation, and 454.59 N·m peak torque; boom 8.12° final with −0.12° error, 0.42° hold deviation, and 183.00 N·m peak; stick −7.89° final with −0.11° error, 0.44° hold deviation, and 82.01 N·m peak; and bucket 10.00° final with effectively zero error, 0.03° hold deviation, and 8.31 N·m peak. The combined four-joint smoke test also passes.

The final display-free verification passed the mechanical and controlled headless checks, the combined four-joint smoke test, all 38 unit tests, compilation, and whitespace validation. Human review accepted the controlled motion and explicitly accepted bucket motion below the platform as an expected consequence of the current no-contact scope.

Two focused corrections were completed without changing acceptance criteria, targets, torque limits, mechanics, or scope. The first introduced retuned motion gains, distinct hold gains, and a deterministic two-second settling interval after the initial bounded controller failed fixed holding criteria. The second restored controlled-viewer lighting parity after human review found the platform appeared too bright: the existing platform material was already correct, so `AddTypicalLights()` was replaced with the exact accepted Milestone 2/3 directional and point lights. Camera, background, geometry, materials, and control behavior were unchanged. The final lighting review exited successfully and the project owner accepted the result.

The accepted implementation is commit `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b` (`feat: add bounded joint actuation control`). Feature closeout documentation was committed as `1fd4218e948797f53c27398efe735ad6704d1e50` (`docs: close milestone 4`) from `2026-08-09T22:54:49+03:00` through `2026-08-09T22:54:51+03:00`, a measured two-second interval.

The accepted feature branch was then fast-forward merged into `main` and pushed from `2026-08-09T22:56:55+03:00` through `2026-08-09T22:56:58+03:00`, a measured three-second interval. Local and remote `main` were synchronized at `1fd4218e948797f53c27398efe735ad6704d1e50`. Human effort, AI-assisted effort, simulation/computation time, and cost remain separately reported; merge and network time are not classified as simulation or computation time.

Contacts, dynamic cubes, bucket/cube interaction, scoop/dump sequencing, excavation state-machine logic, telemetry/HUD, active-joint visualization, camera variants, and final video remain unimplemented.

**Milestone 4 is complete.**

## 16. Milestone 5 contact physics and dynamic cubes

Milestone 5 isolates contact behavior in a new scene while keeping the accepted excavator fixed in its ready-to-scoop pose. It uses `ChSystemNSC`, scene gravity `(0, −9.81, 0) m/s²`, and the installed Bullet collision backend. Explicit backend selection is required because this PyChrono binding leaves a new system without a collision system until one is selected. Milestone 4 control and contact are not combined.

Three minimal placeholder NSC materials are used: cubes have friction `0.45` and restitution `0.05`; the platform and container have friction `0.55` and restitution `0.03`; and the bucket has friction `0.60` and restitution `0.02`. These are deterministic demonstrator values, not calibrated material data. No cohesion, rolling resistance, spinning resistance, compliance, or adhesion was added.

All 30 cubes retain the accepted `0.46 × 0.46 × 0.46 m` visual dimensions and color cycle. Each cube is a dynamic, collidable rigid body with mass `0.25 kg` and box principal inertia `(0.0088167, 0.0088167, 0.0088167) kg·m²`, computed from the standard solid-box expression. The release arrangement is a deterministic `5 × 3 × 2` grid in the accepted pile region, with `0.04 m` clear separation between adjacent collision boxes. The lower layer starts `0.05 m` above the platform surface.

The accepted platform and all five receiving-container pieces remain fixed and use collision boxes matching their visual dimensions and poses. Only the four existing procedural bucket pieces receive excavator collision geometry; tracks, boom, cabin, and other unnecessary excavator parts remain collision-free. The bucket and the entire excavator remain fixed, with no motors, controller, or excavation motion.

The main pile scenario uses a `0.002 s` timestep for `3.0 s`. All 30 cubes fall under gravity, remain finite and within the platform, develop active contacts, and settle to a near-static pile. The deterministic accepted diagnostic produced a peak active contact count of `752`, final contact count of `742`, maximum final linear speed `0.000503 m/s`, and maximum final angular speed `0.001972 rad/s`. The lowest cube surface remains above the platform penetration threshold; the explicit allowed penetration tolerance is `0.020 m`, and the required final linear-speed limit is `0.25 m/s`.

Contact-pair validation passes for cube/platform support in the main scenario, a two-dynamic-cube zero-gravity collision probe, a cube dropped into the actual receiving-container geometry, and a cube dropped onto the actual fixed bucket geometry. Probe bodies are validation-only and do not alter the 30-cube scene. The accepted display-free run measured `4.323503 s` only inside the pile and probe dynamics loops; imports, tests, documentation, and Git operations are excluded.

Current limitations are deliberate: the excavator does not move, contact is not combined with torque control, cubes are toy-model rigid boxes, no scoop/dump sequence exists, and no telemetry, HUD, active-contact visualization, alternative cameras, or video was added.

**Milestone 5 contact physics and dynamic cubes are implemented and awaiting human review.**
