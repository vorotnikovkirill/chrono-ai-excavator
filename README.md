# Chrono AI Excavator

Chrono AI Excavator is a public engineering demonstrator built around a clear workflow: ChatGPT discussion and system decomposition, Codex implementation and verification, and Project Chrono multibody/contact simulation. The intended final scene is an original block-style toy excavator that scoops colored rigid cubes from a platform, rotates, and dumps them into a container.

## Current status

**Milestone 1 — accepted, published, and complete.** The initial scaffold was committed and is now publicly available at [vorotnikovkirill/chrono-ai-excavator](https://github.com/vorotnikovkirill/chrono-ai-excavator). This milestone contains only the repository scaffold, environment checks, project ledger, tests, and documentation foundation.

No Milestone 2 functionality exists. Excavator geometry, joints, motors, contacts, control, telemetry, cameras, rendering, PDF, presentation, and video are not implemented.

The verified local environment is macOS 26.6 on arm64 with the `chrono` Conda environment, Python 3.12.13, and PyChrono. `ChSystemNSC`, `ChBody`, `ChLinkMotorRotationTorque`, Irrlicht, and postprocess are available. VSG and FFmpeg are unavailable and are not required for this milestone. PyChrono is supplied by Conda and is intentionally not declared as a PyPI dependency.

## Verify

From the repository root, activate the existing environment and run:

```bash
conda activate chrono
python scripts/check_environment.py
python scripts/summarize_project_tracking.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

No display window is opened. The current verified environment does not include pytest; the display-free tests use the Python standard-library `unittest` runner, and Milestone 1 does not authorize installing packages.

## Roadmap

Milestone 2 is the next planned step and will create the first visual static scene. Dynamics, joints, contacts, torque control, telemetry, and cameras remain future work. Planned views include a cinematic external camera, a bucket-mounted camera, and a cabin/operator-view camera. PDF and presentation generation remain deferred until a visually meaningful milestone.

See [the living technical report](docs/technical_report.md) and [the project ledger policy](project_tracking/README.md) for scope and evidence.

## License

Source code and original project materials are released under the [MIT License](LICENSE). Third-party assets may be added only when their redistribution rights are documented.
