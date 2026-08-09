#!/usr/bin/env python3
"""Open or validate the Milestone 4 torque-controlled excavator scene."""

from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pychrono as chrono  # noqa: E402

from chrono_ai_excavator.controlled_scene import (  # noqa: E402
    CONTROL_TIMESTEP,
    JOINT_NAMES,
    ControlValidationError,
    advance_controlled_step,
    assert_valid_controlled_scene,
    build_controlled_scene,
    run_control_validation,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show the Milestone 4 torque-controlled scene.")
    parser.add_argument("--headless-check", action="store_true", help="run all bounded control checks without Irrlicht")
    return parser.parse_args(argv)


def run_headless_check() -> int:
    try:
        result = run_control_validation()
    except (RuntimeError, ControlValidationError, ValueError) as exc:
        print(f"Controlled scene headless check: FAIL ({exc})", file=sys.stderr)
        return 1
    print("Controlled scene headless check: PASS")
    for item in result.independent:
        print(
            f"{item.joint_name}: target={math.degrees(item.target_angle):+.2f} deg; "
            f"final={math.degrees(item.final_angle):+.2f} deg; "
            f"error={math.degrees(item.final_error):+.2f} deg; "
            f"max_hold={math.degrees(item.max_hold_deviation):.2f} deg; "
            f"peak_torque={item.peak_abs_torque:.2f}/{item.tau_max:.2f} N*m"
        )
    print("Combined four-joint control smoke test: PASS")
    print(f"Measured control simulation-loop wall time: {result.simulation_wall_seconds:.6f} s")
    return 0


def run_interactive_viewer() -> int:
    try:
        import pychrono.irrlicht as chronoirr

        scene = build_controlled_scene()
        assert_valid_controlled_scene(scene)
        targets = {name: scene.controllers[name].target_delta for name in JOINT_NAMES}
        viewer = chronoirr.ChVisualSystemIrrlicht()
        viewer.AttachSystem(scene.system)
        viewer.SetWindowSize(1280, 800)
        viewer.SetWindowTitle("Chrono AI Excavator — Milestone 4 Torque Control")
        viewer.SetAntialias(True)
        viewer.SetBackgroundColor(chrono.ChColor(0.72, 0.76, 0.80))
        viewer.Initialize()
        viewer.AddCamera(chrono.ChVector3d(*scene.mechanical.camera_position), chrono.ChVector3d(*scene.mechanical.camera_target))
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
    except (ImportError, RuntimeError, ControlValidationError, ValueError) as exc:
        print(f"Interactive controlled scene: FAIL ({exc})", file=sys.stderr)
        return 1

    print("One bounded four-joint transition will run once and hold its final pose.")
    wall_start = time.perf_counter()
    while viewer.Run():
        desired_time = min(time.perf_counter() - wall_start, 3.0)
        while scene.system.GetChTime() + CONTROL_TIMESTEP <= desired_time:
            advance_controlled_step(scene, targets)
        viewer.BeginScene()
        viewer.Render()
        viewer.EndScene()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run_headless_check() if args.headless_check else run_interactive_viewer()


if __name__ == "__main__":
    raise SystemExit(main())
