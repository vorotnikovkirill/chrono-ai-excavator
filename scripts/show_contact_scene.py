#!/usr/bin/env python3
"""Open or validate the Milestone 5 contact scene."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pychrono as chrono  # noqa: E402

from chrono_ai_excavator.contact_scene import (  # noqa: E402
    PILE_DURATION,
    TIMESTEP,
    ContactValidationError,
    assert_valid_contact_scene,
    build_contact_scene,
    run_contact_validation_suite,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show the Milestone 5 fixed-excavator NSC contact scene."
    )
    parser.add_argument(
        "--headless-check",
        action="store_true",
        help="run the pile and contact probes without opening Irrlicht",
    )
    return parser.parse_args(argv)


def run_headless_check() -> int:
    try:
        result = run_contact_validation_suite()
    except (RuntimeError, ContactValidationError, ValueError) as exc:
        print(f"Contact scene headless check: FAIL ({exc})", file=sys.stderr)
        return 1
    pile = result.pile
    print("Contact scene headless check: PASS")
    print(
        f"Pile: cubes={pile.cube_count}; duration={pile.simulated_duration:.3f} s; "
        f"timestep={pile.timestep:.3f} s; peak_contacts={pile.peak_contact_count}; "
        f"final_contacts={pile.final_contact_count}"
    )
    print(
        f"Final speeds: linear={pile.maximum_final_linear_speed:.6f} m/s; "
        f"angular={pile.maximum_final_angular_speed:.6f} rad/s"
    )
    print(
        f"Platform penetration: {'PASS' if pile.platform_penetration_passed else 'FAIL'} "
        f"(tolerance={pile.penetration_tolerance:.3f} m)"
    )
    print(f"Cube/platform: {'PASS' if pile.cube_platform_passed else 'FAIL'}")
    print(f"Cube/cube: {'PASS' if result.cube_cube.passed else 'FAIL'}")
    print(f"Cube/container: {'PASS' if result.cube_container.passed else 'FAIL'}")
    print(f"Cube/bucket: {'PASS' if result.cube_bucket.passed else 'FAIL'}")
    print(f"Measured contact simulation-loop wall time: {result.simulation_wall_seconds:.6f} s")
    return 0


def run_interactive_viewer() -> int:
    try:
        import pychrono.irrlicht as chronoirr

        scene = build_contact_scene()
        assert_valid_contact_scene(scene)
        viewer = chronoirr.ChVisualSystemIrrlicht()
        viewer.AttachSystem(scene.system)
        viewer.SetWindowSize(1280, 800)
        viewer.SetWindowTitle("Chrono AI Excavator — Milestone 5 Contact Physics")
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
    except (ImportError, RuntimeError, ContactValidationError, ValueError) as exc:
        print(f"Interactive contact scene: FAIL ({exc})", file=sys.stderr)
        return 1

    print("The fixed excavator will remain still while 30 cubes fall and settle.")
    wall_start = time.perf_counter()
    while viewer.Run():
        desired_time = min(time.perf_counter() - wall_start, PILE_DURATION)
        while scene.system.GetChTime() + TIMESTEP <= desired_time:
            scene.system.DoStepDynamics(TIMESTEP)
        viewer.BeginScene()
        viewer.Render()
        viewer.EndScene()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run_headless_check() if args.headless_check else run_interactive_viewer()


if __name__ == "__main__":
    raise SystemExit(main())
