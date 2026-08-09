"""Display-free tests for Milestone 5 NSC contact dynamics."""

from __future__ import annotations

import math
import unittest

import pychrono as chrono

from chrono_ai_excavator.contact_scene import (
    BUCKET_NAMES,
    CONTAINER_NAMES,
    CUBE_COUNT,
    CUBE_INERTIA,
    CUBE_MASS,
    FINAL_LINEAR_SPEED_LIMIT,
    GRAVITY,
    MATERIAL_SPECS,
    PLATFORM_PENETRATION_TOLERANCE,
    assert_valid_contact_scene,
    build_contact_scene,
    run_contact_validation_suite,
    validate_contact_scene,
)
from chrono_ai_excavator.controlled_scene import build_controlled_scene


class ContactSceneTests(unittest.TestCase):
    """Exercise construction and the complete deterministic contact result."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = build_contact_scene()
        cls.result = run_contact_validation_suite()

    def test_nsc_system_and_gravity(self) -> None:
        self.assertIsInstance(self.scene.system, chrono.ChSystemNSC)
        gravity = self.scene.system.GetGravitationalAcceleration()
        self.assertEqual((gravity.x, gravity.y, gravity.z), GRAVITY)
        self.assertIsNotNone(self.scene.system.GetCollisionSystem())

    def test_exactly_thirty_dynamic_collidable_cubes(self) -> None:
        self.assertEqual(len(self.scene.cubes), CUBE_COUNT)
        self.assertTrue(all(not body.IsFixed() for body in self.scene.cubes))
        self.assertTrue(all(body.IsCollisionEnabled() for body in self.scene.cubes))

    def test_cube_mass_and_inertia(self) -> None:
        for body in self.scene.cubes:
            self.assertAlmostEqual(body.GetMass(), CUBE_MASS)
            inertia = body.GetInertiaXX()
            for actual, expected in zip((inertia.x, inertia.y, inertia.z), CUBE_INERTIA):
                self.assertAlmostEqual(actual, expected)
                self.assertGreater(actual, 0.0)

    def test_fixed_contact_geometry(self) -> None:
        bodies = (
            self.scene.platform,
            *self.scene.container_bodies.values(),
            *self.scene.bucket_bodies.values(),
        )
        self.assertTrue(all(body.IsFixed() for body in bodies))
        self.assertTrue(all(body.IsCollisionEnabled() for body in bodies))
        self.assertEqual(tuple(self.scene.container_bodies), CONTAINER_NAMES)
        self.assertEqual(tuple(self.scene.bucket_bodies), BUCKET_NAMES)

    def test_contact_material_metadata(self) -> None:
        self.assertEqual((MATERIAL_SPECS["cube"].friction, MATERIAL_SPECS["cube"].restitution), (0.45, 0.05))
        self.assertEqual((MATERIAL_SPECS["environment"].friction, MATERIAL_SPECS["environment"].restitution), (0.55, 0.03))
        self.assertEqual((MATERIAL_SPECS["bucket"].friction, MATERIAL_SPECS["bucket"].restitution), (0.60, 0.02))

    def test_release_configuration_is_deterministic_and_separated(self) -> None:
        rebuilt = build_contact_scene()
        self.assertEqual(self.scene.cube_specs, rebuilt.cube_specs)
        for index, first in enumerate(self.scene.cube_specs):
            for second in self.scene.cube_specs[index + 1 :]:
                self.assertFalse(
                    all(
                        abs(a - b) < first.dimensions[axis]
                        for axis, (a, b) in enumerate(zip(first.position, second.position))
                    )
                )

    def test_scene_validation_and_no_motors(self) -> None:
        self.assertEqual(validate_contact_scene(self.scene), ())
        self.assertIsNone(assert_valid_contact_scene(self.scene))
        self.assertFalse(any("Motor" in type(link).__name__ for link in self.scene.system.GetLinks()))

    def test_pile_is_finite_and_contacts_occur(self) -> None:
        pile = self.result.pile
        self.assertTrue(pile.finite)
        self.assertGreater(pile.peak_contact_count, 0)
        self.assertGreater(pile.final_contact_count, 0)
        self.assertTrue(pile.cubes_fell)
        self.assertTrue(pile.cubes_within_platform)

    def test_platform_penetration_and_final_speed(self) -> None:
        pile = self.result.pile
        self.assertEqual(pile.penetration_tolerance, PLATFORM_PENETRATION_TOLERANCE)
        self.assertTrue(pile.platform_penetration_passed)
        self.assertLessEqual(pile.maximum_final_linear_speed, FINAL_LINEAR_SPEED_LIMIT)

    def test_all_required_contact_pairs_pass(self) -> None:
        self.assertTrue(self.result.pile.cube_platform_passed)
        self.assertTrue(self.result.cube_cube.passed)
        self.assertTrue(self.result.cube_container.passed)
        self.assertTrue(self.result.cube_bucket.passed)

    def test_metadata_and_results_are_finite(self) -> None:
        values = (
            self.result.pile.maximum_final_linear_speed,
            self.result.pile.maximum_final_angular_speed,
            self.result.simulation_wall_seconds,
        )
        self.assertTrue(all(math.isfinite(value) and value >= 0.0 for value in values))

    def test_controlled_scene_configuration_remains_accepted(self) -> None:
        controllers = build_controlled_scene().controllers.values()
        self.assertEqual(
            tuple((item.joint_name, item.kp, item.kd, item.hold_kp, item.hold_kd, item.tau_max) for item in controllers),
            (
                ("J0_SLEW", 1500.0, 2500.0, 1500.0, 2500.0, 800.0),
                ("J1_BOOM", 2000.0, 1200.0, 6500.0, 2800.0, 800.0),
                ("J2_STICK", 1500.0, 700.0, 6000.0, 2200.0, 600.0),
                ("J3_BUCKET", 800.0, 200.0, 1600.0, 500.0, 300.0),
            ),
        )


if __name__ == "__main__":
    unittest.main()
