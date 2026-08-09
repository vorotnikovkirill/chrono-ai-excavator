"""Display-free tests for Milestone 4 torque actuation and control."""

from __future__ import annotations

import math
import unittest

import pychrono as chrono

from chrono_ai_excavator.controlled_scene import (
    JOINT_NAMES,
    bounded_pd_torque,
    build_controlled_scene,
    run_control_validation,
    smooth_target,
    validate_controlled_scene,
)


class ControlledSceneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = build_controlled_scene()
        cls.result = run_control_validation()

    def test_controlled_topology_and_motors(self) -> None:
        self.assertEqual(tuple(self.scene.bodies), ("BASE", "UPPER", "BOOM", "STICK", "BUCKET"))
        self.assertEqual(tuple(self.scene.motors), JOINT_NAMES)
        self.assertEqual(len(self.scene.system.GetLinks()), 4)
        self.assertTrue(all(type(motor) is chrono.ChLinkMotorRotationTorque for motor in self.scene.motors.values()))
        self.assertEqual(tuple(link.GetName() for link in self.scene.system.GetLinks()), JOINT_NAMES)
        self.assertEqual(validate_controlled_scene(self.scene), ())

    def test_motor_connectivity_and_axes(self) -> None:
        specs = {spec.name: spec for spec in self.scene.mechanical.joint_specs}
        for name in JOINT_NAMES:
            motor, spec = self.scene.motors[name], specs[name]
            self.assertEqual(motor.GetBody1(), self.scene.bodies[spec.parent])
            self.assertEqual(motor.GetBody2(), self.scene.bodies[spec.child])
            axis = motor.GetFrame1Abs().GetRot().GetAxisZ()
            self.assertAlmostEqual(abs(axis.x * spec.axis[0] + axis.y * spec.axis[1] + axis.z * spec.axis[2]), 1.0)

    def test_controller_configs_and_targets(self) -> None:
        expected = {"J0_SLEW": 12.0, "J1_BOOM": 8.0, "J2_STICK": -8.0, "J3_BUCKET": 10.0}
        for name, degrees in expected.items():
            config = self.scene.controllers[name]
            self.assertGreater(config.kp, 0)
            self.assertGreaterEqual(config.kd, 0)
            self.assertGreater(config.hold_kp, 0)
            self.assertGreaterEqual(config.hold_kd, 0)
            self.assertGreater(config.tau_max, 0)
            self.assertAlmostEqual(config.target_delta, math.radians(degrees))

    def test_smooth_trajectory_endpoints(self) -> None:
        self.assertEqual(smooth_target(0.0, 1.0), (0.0, 0.0))
        self.assertEqual(smooth_target(1.0, 1.0), (1.0, 0.0))
        self.assertEqual(smooth_target(2.0, 1.0), (1.0, 0.0))

    def test_pd_torque_saturates(self) -> None:
        config = self.scene.controllers["J3_BUCKET"]
        self.assertEqual(bounded_pd_torque(config, 10.0, 0.0, 0.0, 0.0), config.tau_max)
        self.assertEqual(bounded_pd_torque(config, -10.0, 0.0, 0.0, 0.0), -config.tau_max)

    def test_independent_joint_results_meet_acceptance(self) -> None:
        for result in self.result.independent:
            self.assertTrue(result.finite)
            self.assertLessEqual(abs(result.final_error), math.radians(1.5))
            self.assertLessEqual(result.peak_abs_torque, result.tau_max + 1e-9)
            self.assertLessEqual(result.max_hold_deviation, math.radians(0.5))

    def test_combined_control_smoke_passes(self) -> None:
        self.assertEqual(len(self.result.combined), 4)
        for result in self.result.combined:
            self.assertTrue(result.finite)
            self.assertLess(abs(result.final_error), abs(result.target_angle))
            self.assertLessEqual(result.peak_abs_torque, result.tau_max + 1e-9)

    def test_environment_and_metadata_are_deterministic(self) -> None:
        rebuilt = build_controlled_scene()
        self.assertEqual(self.scene.cube_count, 30)
        self.assertTrue(all(body.IsFixed() for body in self.scene.environment_bodies.values()))
        self.assertEqual(tuple(self.scene.controllers.values()), tuple(rebuilt.controllers.values()))
        self.assertTrue(all(not body.IsCollisionEnabled() for body in (*self.scene.bodies.values(), *self.scene.environment_bodies.values())))


if __name__ == "__main__":
    unittest.main()
