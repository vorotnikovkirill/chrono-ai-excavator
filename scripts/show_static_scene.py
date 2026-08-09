#!/usr/bin/env python3
"""Open or validate the Milestone 2 static excavator scene."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pychrono as chrono  # noqa: E402

from chrono_ai_excavator.static_scene import (  # noqa: E402
    SceneValidationError,
    assert_valid_static_scene,
    build_static_scene,
    summarize_static_scene,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the deliberately small viewer interface."""

    parser = argparse.ArgumentParser(
        description="Show the Chrono AI Excavator Milestone 2 static scene."
    )
    parser.add_argument(
        "--headless-check",
        action="store_true",
        help="build and validate the complete scene without opening Irrlicht",
    )
    return parser.parse_args(argv)


def run_headless_check() -> int:
    """Build, validate, summarize, and exit without importing Irrlicht."""

    try:
        scene = build_static_scene()
        assert_valid_static_scene(scene)
    except (RuntimeError, SceneValidationError, ValueError) as exc:
        print(f"Static scene headless check: FAIL ({exc})", file=sys.stderr)
        return 1
    print("Static scene headless check: PASS")
    print("Objects: " + summarize_static_scene(scene))
    return 0


def run_interactive_viewer() -> int:
    """Open the fixed scene in the interactive Irrlicht viewer."""

    try:
        import pychrono.irrlicht as chronoirr

        scene = build_static_scene()
        assert_valid_static_scene(scene)
        viewer = chronoirr.ChVisualSystemIrrlicht()
        viewer.AttachSystem(scene.system)
        viewer.SetWindowSize(1280, 800)
        viewer.SetWindowTitle("Chrono AI Excavator — Milestone 2 Static Scene")
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
    except (ImportError, RuntimeError, SceneValidationError, ValueError) as exc:
        print(f"Interactive static scene: FAIL ({exc})", file=sys.stderr)
        return 1

    print("Chrono AI Excavator — Milestone 2 Static Scene")
    print("Scene: " + summarize_static_scene(scene))
    print("Use the normal Irrlicht mouse controls to inspect the scene; close the window to exit.")
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
