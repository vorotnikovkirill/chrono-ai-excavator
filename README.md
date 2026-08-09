# Chrono AI Excavator

Chrono AI Excavator is a public engineering demonstrator built around a clear workflow: ChatGPT discussion and system decomposition, Codex implementation and verification, and Project Chrono multibody/contact simulation. The intended final scene is an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container.

## Current status

**Milestone 2 — static visual composition accepted.** The first static Project Chrono scene is implemented, display-free verification passed, and project-owner visual review passed. It uses original procedural primitives to show a bright block-style excavator in a ready-to-scoop pose, a fixed construction platform, 30 colored cubes, and an open receiving container. These changes remain on `feature/first-visual-scene` pending repository review, commit, and push.

All scene bodies are fixed and collision-free. Dynamics, joints, contacts, control, telemetry, bucket and cabin cameras, rendered output, PDF, presentation, and video are not implemented.

The verified local environment is macOS 26.6 on arm64 with the `chrono` Conda environment, Python 3.12.13, and PyChrono. `ChSystemNSC`, `ChBody`, `ChLinkMotorRotationTorque`, Irrlicht, and postprocess are available. VSG and FFmpeg are unavailable and are not required for this milestone. PyChrono is supplied by Conda and is intentionally not declared as a PyPI dependency.

## Verify

From the repository root, activate the existing environment and run:

```bash
conda activate chrono
python scripts/check_environment.py
python scripts/show_static_scene.py --headless-check
python scripts/show_static_scene.py
python scripts/summarize_project_tracking.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

The `--headless-check` command and tests do not open a display. The viewer command opens the interactive Irrlicht window for required human visual inspection. The current verified environment does not include pytest; display-free tests use the Python standard-library `unittest` runner, and this milestone does not authorize installing packages.

## Roadmap

The next step is repository review followed by commit and push of the accepted static scene. Dynamics, joints, contacts, torque control, telemetry, bucket and cabin cameras, rendering, and video remain future work. PDF and presentation generation remain deferred.

See [the living technical report](docs/technical_report.md) and [the project ledger policy](project_tracking/README.md) for scope and evidence.

## License

Source code and original project materials are released under the [MIT License](LICENSE). Third-party assets may be added only when their redistribution rights are documented.
