# Chrono AI Excavator

Chrono AI Excavator is a public engineering demonstrator built around a clear workflow: ChatGPT discussion and system decomposition, Codex implementation and verification, and Project Chrono multibody/contact simulation. The intended final scene is an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container.

## Current status

**Milestone 2 — complete.** The first static Project Chrono scene was implemented, display-free verified, human visually accepted, committed, pushed, fast-forward merged into `main`, and published in the public repository. It uses original procedural primitives to show a bright block-style excavator in a ready-to-scoop pose, a fixed construction platform, 30 colored cubes, and an open receiving container.

**Milestone 3 — accepted and ready for merge.** The articulated architecture is implemented, display-free verified, human visually accepted, committed, and pushed to `feature/mechanical-architecture`. It uses five primary mechanical bodies (`BASE`, `UPPER`, `BOOM`, `STICK`, and `BUCKET`), four functional revolute joints, and zero-gravity topology verification. It has not yet been merged into `main`.

Motors, torque control, state-machine control, contacts, dynamic cubes, telemetry, active-joint visualization, bucket-mounted and cabin/operator cameras, and video remain future work.

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
python scripts/summarize_project_tracking.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

The `--headless-check` command and tests do not open a display. The viewer command opens the interactive Irrlicht window for required human visual inspection. The current verified environment does not include pytest; display-free tests use the Python standard-library `unittest` runner, and this milestone does not authorize installing packages.

## Roadmap

Milestone 2 remains complete. Milestone 3 mechanical architecture is accepted and awaiting merge into `main`. Motors, control, contacts, telemetry, camera variants, rendering, and video remain future work. PDF and presentation generation remain deferred.

See [the living technical report](docs/technical_report.md) and [the project ledger policy](project_tracking/README.md) for scope and evidence.

## License

Source code and original project materials are released under the [MIT License](LICENSE). Third-party assets may be added only when their redistribution rights are documented.
