#!/usr/bin/env python3
"""Open or validate the Milestone 3 mechanical excavator scene."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pychrono as chrono  # noqa: E402

from chrono_ai_excavator.mechanical_scene import (  # noqa: E402
    MechanicalValidationError,
    assert_valid_mechanical_scene,
    build_mechanical_scene,
    run_constraint_smoke_test,
    summarize_mechanical_scene,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the deliberately small viewer interface."""

    parser = argparse.ArgumentParser(
        description="Show the Chrono AI Excavator Milestone 3 mechanical scene."
    )
    parser.add_argument(
        "--headless-check",
        action="store_true",
        help="validate the articulated scene and constraints without opening Irrlicht",
    )
    return parser.parse_args(argv)


def run_headless_check() -> int:
    """Build, validate, smoke test, summarize, and exit without a display."""

    try:
        scene = build_mechanical_scene()
        assert_valid_mechanical_scene(scene)
        final_time = run_constraint_smoke_test(scene)
    except (RuntimeError, MechanicalValidationError, ValueError) as exc:
        print(f"Mechanical scene headless check: FAIL ({exc})", file=sys.stderr)
        return 1
    print("Mechanical scene headless check: PASS")
    print("Architecture: " + summarize_mechanical_scene(scene))
    print(f"Zero-gravity constraint smoke test: PASS ({final_time:.3f} s)")
    return 0


def run_interactive_viewer() -> int:
    """Open the articulated scene in its accepted ready-to-scoop pose."""

    try:
        import pychrono.irrlicht as chronoirr

        scene = build_mechanical_scene()
        assert_valid_mechanical_scene(scene)
        viewer = chronoirr.ChVisualSystemIrrlicht()
        viewer.AttachSystem(scene.system)
        viewer.SetWindowSize(1280, 800)
        viewer.SetWindowTitle("Chrono AI Excavator — Milestone 3 Mechanical Architecture")
        viewer.SetAntialias(True)
        viewer.SetBackgroundColor(chrono.ChColor(0.72, 0.76, 0.80))
        viewer.Initialize()
        viewer.AddCamera(
            chrono.ChVector3d(*scene.camera_position),
            chrono.ChVector3d(*scene.camera_target),
        )
        viewer.AddLightDirectional(
            55.0,
            35.0,
            chrono.ChColor(0.55, 0.55, 0.58),
            chrono.ChColor(0.22, 0.22, 0.22),
            chrono.ChColor(1.0, 0.97, 0.90),
        )
        viewer.AddLight(
            chrono.ChVector3d(-5.0, 8.0, 6.0),
            18.0,
            chrono.ChColor(0.45, 0.50, 0.58),
        )
    except (ImportError, RuntimeError, MechanicalValidationError, ValueError) as exc:
        print(f"Interactive mechanical scene: FAIL ({exc})", file=sys.stderr)
        return 1

    print("Chrono AI Excavator — Milestone 3 Mechanical Architecture")
    print("Architecture: " + summarize_mechanical_scene(scene))
    print("The zero-gravity mechanism is shown without animation; close the window to exit.")
    while viewer.Run():
        viewer.BeginScene()
        viewer.Render()
        viewer.EndScene()
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run headless validation or the interactive viewer."""

    args = parse_args(argv)
    if args.headless_check:
        return run_headless_check()
    return run_interactive_viewer()


if __name__ == "__main__":
    raise SystemExit(main())
