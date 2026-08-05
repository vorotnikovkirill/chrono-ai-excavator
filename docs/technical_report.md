# Chrono AI Excavator — Living Technical Report

## 1. Project objective

The project will demonstrate an end-to-end public engineering workflow that produces a fast, clear, and visually strong Project Chrono result. **Implemented:** the Milestone 1 repository and documentation foundation. **Current limitation:** no excavator simulation exists yet.

## 2. Demonstrator concept

The planned demonstrator is an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container. This is future work, not implemented functionality. It will not reproduce a specific commercial toy set or use protected branding.

## 3. ChatGPT → Codex → Project Chrono workflow

ChatGPT supports engineering discussion and decomposition; Codex implements and verifies bounded milestones; Project Chrono will execute multibody and contact simulation. Later outputs will include telemetry, public technical documentation, a presentation, and a final video. The current repository preserves the specification and records tool, time, iteration, and cost evidence.

## 4. Scope-control principle

Every addition must either satisfy the current milestone or materially improve the final video. Speculative abstractions and unnecessary physical depth are excluded. Human active effort, AI wall time, and computation time are tracked independently.

## 5. Planned mechanical architecture

**Planned assumption:** a compact rigid-body assembly will approximate a tracked base, rotating upper structure, boom, stick, and bucket using original procedural block geometry. Real track dynamics, CAD import, hydraulics, flexible bodies, and deformation are outside the present plan. No geometry or rigid-body assembly has been implemented.

## 6. Planned joint and torque-control concept

Future revolute joints will represent swing, boom, stick, and bucket motion. A minimal controller is expected to command joint torque toward a scripted motion target, subject to what is visually useful and stable. No joints, motors, controllers, control state machine, or calibration exists yet.

## 7. Planned contact scene

Future rigid colored cubes will rest on a platform and interact with the bucket before being deposited in a container. Contact material choices and solver settings remain future engineering decisions. No platform, cubes, container, contacts, or contact materials exist yet.

## 8. Planned visualization and camera views

The planned final visualization includes a cinematic external camera, a bucket-mounted camera, and a cabin/operator-view camera. It may show active joints, target and actual motion, commanded actuator torque, contact activity, and selected telemetry. No cameras, HUD, camera switching, plots, frames, or video exist yet.

## 9. Milestone 0 preflight results

**Verified findings:** macOS 26.6 arm64, Python 3.12.13 in the `chrono` Conda environment, PyChrono, `ChSystemNSC`, `ChBody`, `ChLinkMotorRotationTorque`, Irrlicht, and postprocess are available. VSG and FFmpeg are unavailable and unnecessary for Milestone 1. A minimal gravity smoke test passed during preflight. Three runs were needed: one initial run and two corrections. The source brief supplies the historical timestamps and evidence paths.

## 10. Milestone 1 scope and outputs

**Accepted and implemented:** repository policy, packaging metadata, package version, display-free environment verification, deterministic tests, standard-library project-ledger validation and summary, a living report, and preserved prompts. Milestone 1 is complete and ready for its initial public commit and publication; publication has not yet occurred.

One publication orchestration attempt failed before publication. Codex task execution never started because a global approval argument was placed after the `exec` subcommand, and unittest discovery omitted `PYTHONPATH=src`. Environment verification, the tracking summary, and compilation still passed. These were orchestration defects and did not invalidate the accepted scaffold. Pytest remains absent from the `chrono` environment, package installation remains prohibited, and the display-free tests run through standard-library `unittest`.

## 11. Project effort, tooling, and cost ledger

The CSV ledger records calendar duration without overlap double-counting and reports human active effort, AI-assisted development wall time, simulation/computation wall time, documented software and infrastructure cost, and iteration/rework counts. Historical project-owner active effort is an approximate 25 minutes with a plausible 20–30 minute range. Historical ChatGPT generation time and command-review effort are unknown and are not invented. Subscription costs and incremental ChatGPT/Codex project costs are not separately measurable from available evidence.

Required final project metrics are:

- calendar duration;
- human active effort;
- AI-assisted development effort;
- simulation wall-clock time;
- software and infrastructure cost;
- initial, correction, repeat, and rework counts.

## 12. Current limitations

No excavator simulation, geometry, joint, motor, controller, contact scene, telemetry, camera, render, PDF, presentation, or video exists. No Milestone 2 functionality has been implemented. PDF and presentation generation remain deferred until the first visually meaningful milestone. The living report will later become the source for the public technical PDF.

## 13. Next milestone

Milestone 2 will create the first visual static scene and matching verification while updating the README, report, ledger, tests, and preserved prompt. Exact architecture remains a future decision rather than an assumption embedded in this scaffold.
