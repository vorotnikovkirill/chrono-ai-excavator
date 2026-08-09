# Chrono AI Excavator

Chrono AI Excavator is a public engineering demonstrator built around a clear workflow: ChatGPT discussion and system decomposition, Codex implementation and verification, and Project Chrono multibody/contact simulation. The intended final scene is an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container.

## Current status

**Milestone 2 — complete.** The first static Project Chrono scene was implemented, display-free verified, human visually accepted, committed, pushed, fast-forward merged into `main`, and published in the public repository. It uses original procedural primitives to show a bright block-style excavator in a ready-to-scoop pose, a fixed construction platform, 30 colored cubes, and an open receiving container.

**Milestone 3 — complete.** The articulated architecture was implemented, display-free verified, human visually accepted, committed, pushed, fast-forward merged into `main`, and published in the public repository. It uses five primary mechanical bodies (`BASE`, `UPPER`, `BOOM`, `STICK`, and `BUCKET`), four functional revolute joints, and zero-gravity topology verification.

**Milestone 4 — accepted and ready for merge.** Four torque-actuated joints, bounded PD motion control with distinct hold gains, fixed torque saturation, and deterministic smooth target trajectories were implemented and verified in zero gravity. All 38 tests pass, control motion and the corrected accepted-baseline lighting were visually accepted, and commit `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b` was pushed to `feature/joint-actuation-control`. The milestone is awaiting merge into `main`.

Contacts, dynamic cubes, the scoop/dump sequence, excavation state machine, telemetry/HUD, active-joint visualization, bucket and cabin cameras, and final video remain future work.

The verified local environment is macOS 26.6 on arm64 with the `chrono` Conda environment, Python 3.12.13, and PyChrono. `ChSystemNSC`, `ChBody`, `ChLinkMotorRotationTorque`, Irrlicht, and postprocess are available. VSG and FFmpeg are unavailable and are not required for this milestone. PyChrono is supplied by Conda and is intentionally not declared as a PyPI dependency.

## Verify

From the repository root, activate the existing environment and run:

```bash
conda activate chrono
python scripts/check_environment.py
python scripts/show_static_scene.py --headless-check
python scripts/show_static_scene.py
python scripts/show_mechanical_scene.py --headless-check
python scripts/show_mechanical_scene.py
python scripts/show_controlled_scene.py --headless-check
python scripts/show_controlled_scene.py
python scripts/summarize_project_tracking.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

The `--headless-check` command and tests do not open a display. The viewer command opens the interactive Irrlicht window for required human visual inspection. The current verified environment does not include pytest; display-free tests use the Python standard-library `unittest` runner, and this milestone does not authorize installing packages.

## Roadmap

Milestones 2 and 3 are complete. Milestone 4 actuation and basic control are accepted on `feature/joint-actuation-control` and awaiting merge into `main`. Contacts, dynamic cubes, scoop/dump behavior, an excavation state machine, telemetry/HUD, active-joint visualization, bucket and cabin cameras, rendering, and final video remain future work. PDF and presentation generation remain deferred.

See [the living technical report](docs/technical_report.md) and [the project ledger policy](project_tracking/README.md) for scope and evidence.

## License

Source code and original project materials are released under the [MIT License](LICENSE). Third-party assets may be added only when their redistribution rights are documented.
