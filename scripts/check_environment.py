#!/usr/bin/env python3
"""Verify the minimal Project Chrono environment without opening a display."""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass


REQUIRED_CLASSES = ("ChSystemNSC", "ChBody", "ChLinkMotorRotationTorque")


@dataclass(frozen=True)
class CapabilityReport:
    irrlicht: bool
    postprocess: bool
    vsg: bool


def detect_visualization_capabilities() -> CapabilityReport:
    """Detect optional visualization modules without creating a window."""

    def available(module_name: str) -> bool:
        try:
            importlib.import_module(module_name)
        except ImportError:
            return False
        return True

    return CapabilityReport(
        irrlicht=available("pychrono.irrlicht"),
        postprocess=available("pychrono.postprocess"),
        vsg=available("pychrono.vsg"),
    )


def run_gravity_smoke_test(chrono: object) -> tuple[float, float]:
    """Advance one free body and return its initial and final vertical position."""

    system = chrono.ChSystemNSC()
    system.SetGravitationalAcceleration(chrono.ChVector3d(0.0, -9.81, 0.0))
    body = chrono.ChBody()
    body.SetFixed(False)
    body.SetPos(chrono.ChVector3d(0.0, 1.0, 0.0))
    system.Add(body)

    initial_y = body.GetPos().y
    for _ in range(10):
        system.DoStepDynamics(0.01)
    final_y = body.GetPos().y

    if not final_y < initial_y:
        raise RuntimeError(
            f"Gravity smoke test failed: initial y={initial_y:.6f}, "
            f"final y={final_y:.6f}"
        )
    return initial_y, final_y


def main() -> int:
    """Run required checks and return a shell-compatible status code."""

    failures: list[str] = []
    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")

    try:
        import pychrono as chrono
    except ImportError as exc:
        print(f"PyChrono: FAIL ({exc})")
        print("Summary: FAIL (1 required check failed)")
        return 1

    print(f"PyChrono module: {chrono.__file__}")
    for class_name in REQUIRED_CLASSES:
        present = hasattr(chrono, class_name)
        print(f"Required class {class_name}: {'PASS' if present else 'FAIL'}")
        if not present:
            failures.append(class_name)

    capabilities = detect_visualization_capabilities()
    print(f"Irrlicht: {'available' if capabilities.irrlicht else 'unavailable'}")
    print(f"Postprocess: {'available' if capabilities.postprocess else 'unavailable'}")
    print(
        "VSG: "
        f"{'available' if capabilities.vsg else 'unavailable (optional; not a failure)'}"
    )
    if not capabilities.irrlicht:
        failures.append("pychrono.irrlicht")
    if not capabilities.postprocess:
        failures.append("pychrono.postprocess")

    if not failures:
        try:
            initial_y, final_y = run_gravity_smoke_test(chrono)
            print(f"Gravity smoke test: PASS (y {initial_y:.6f} -> {final_y:.6f})")
        except Exception as exc:  # Keep command-line diagnostics concise.
            failures.append("gravity smoke test")
            print(f"Gravity smoke test: FAIL ({exc})")

    if failures:
        print(f"Summary: FAIL ({len(failures)} required check(s) failed)")
        return 1

    print("Summary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
