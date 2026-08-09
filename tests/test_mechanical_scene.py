"""Display-free tests for the Milestone 3 mechanical architecture."""

from __future__ import annotations

import math
import unittest

from chrono_ai_excavator.mechanical_scene import (
    JOINT_NAMES,
    PRIMARY_BODY_NAMES,
    assert_valid_mechanical_scene,
    build_mechanical_scene,
    run_constraint_smoke_test,
    validate_mechanical_scene,
)


class MechanicalSceneTests(unittest.TestCase):
    """Exercise mechanical topology and constraints without Irrlicht."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = build_mechanical_scene()

    def test_scene_construction(self) -> None:
        self.assertEqual(len(self.scene.system.GetBodies()), 41)
        self.assertEqual(len(self.scene.system.GetLinks()), 4)

    def test_exact_primary_body_topology(self) -> None:
        self.assertEqual(tuple(self.scene.bodies), PRIMARY_BODY_NAMES)
        self.assertEqual(len(self.scene.bodies), 5)

    def test_fixed_and_dynamic_body_status(self) -> None:
        self.assertTrue(self.scene.bodies["BASE"].IsFixed())
        for name in PRIMARY_BODY_NAMES[1:]:
            self.assertFalse(self.scene.bodies[name].IsFixed())

    def test_positive_mass_and_principal_inertia(self) -> None:
        for name, body in self.scene.bodies.items():
            with self.subTest(body=name):
                self.assertGreater(body.GetMass(), 0)
                inertia = body.GetInertiaXX()
                self.assertTrue(all(value > 0 for value in (inertia.x, inertia.y, inertia.z)))

    def test_exact_joint_names_and_count(self) -> None:
        self.assertEqual(tuple(self.scene.joints), JOINT_NAMES)
        self.assertEqual(len(self.scene.joints), 4)

    def test_joint_connectivity(self) -> None:
        expected = {
            "J0_SLEW": ("BASE", "UPPER"),
            "J1_BOOM": ("UPPER", "BOOM"),
            "J2_STICK": ("BOOM", "STICK"),
            "J3_BUCKET": ("STICK", "BUCKET"),
        }
        for name, connection in expected.items():
            joint = self.scene.joints[name]
            parent, child = connection
            self.assertEqual(joint.GetBody1(), self.scene.bodies[parent])
            self.assertEqual(joint.GetBody2(), self.scene.bodies[child])

    def test_slew_axis_is_vertical(self) -> None:
        axis = self.scene.joint_specs[0].axis
        self.assertEqual(axis, (0.0, 1.0, 0.0))

    def test_arm_joint_axes_are_parallel(self) -> None:
        axes = [spec.axis for spec in self.scene.joint_specs[1:]]
        for axis in axes:
            self.assertEqual(axis, (0.0, 0.0, 1.0))

    def test_arm_joint_and_decorative_marker_axes_use_scene_z(self) -> None:
        markers = (
            ("J1_BOOM", "UPPER", "excavator.boom_pivot"),
            ("J2_STICK", "BOOM", "excavator.elbow_pivot"),
            ("J3_BUCKET", "STICK", "excavator.bucket_pivot"),
        )
        for joint_name, body_name, marker_name in markers:
            with self.subTest(joint=joint_name, marker=marker_name):
                joint_axis = self.scene.joints[joint_name].GetFrame1Abs().GetRot().GetAxisZ()
                self.assertAlmostEqual(joint_axis.x, 0.0)
                self.assertAlmostEqual(joint_axis.y, 0.0)
                self.assertAlmostEqual(joint_axis.z, 1.0)

                spec = next(item for item in self.scene.body_specs if item.name == body_name)
                marker_index = spec.visual_names.index(marker_name)
                marker_frame = self.scene.bodies[body_name].GetVisualModel().GetShapeFrame(marker_index)
                marker_axis = self.scene.bodies[body_name].GetRot().Rotate(
                    marker_frame.GetRot().GetAxisZ()
                )
                self.assertAlmostEqual(marker_axis.x, 0.0)
                self.assertAlmostEqual(marker_axis.y, 0.0)
                self.assertAlmostEqual(marker_axis.z, 1.0)

    def test_y_axis_cylinder_visual_uses_scene_y(self) -> None:
        spec = next(item for item in self.scene.body_specs if item.name == "UPPER")
        shape_index = spec.visual_names.index("excavator.rotating_platform")
        shape_frame = self.scene.bodies["UPPER"].GetVisualModel().GetShapeFrame(shape_index)
        world_axis = self.scene.bodies["UPPER"].GetRot().Rotate(
            shape_frame.GetRot().GetAxisZ()
        )
        self.assertAlmostEqual(world_axis.x, 0.0)
        self.assertAlmostEqual(world_axis.y, 1.0)
        self.assertAlmostEqual(world_axis.z, 0.0)

    def test_joint_pivots_and_axes_are_finite(self) -> None:
        for spec in self.scene.joint_specs:
            with self.subTest(joint=spec.name):
                self.assertTrue(all(math.isfinite(value) for value in (*spec.pivot, *spec.axis)))
                self.assertAlmostEqual(math.sqrt(sum(value * value for value in spec.axis)), 1.0)

    def test_environment_and_thirty_cubes_are_retained(self) -> None:
        names = set(self.scene.environment_bodies)
        self.assertIn("platform", names)
        self.assertEqual(self.scene.cube_count, 30)
        self.assertTrue(all(f"container.{name}" in names for name in ("floor", "wall_front", "wall_back", "wall_left", "wall_right")))
        self.assertTrue(all(body.IsFixed() for body in self.scene.environment_bodies.values()))

    def test_no_motors_or_collision(self) -> None:
        self.assertFalse(any("Motor" in type(link).__name__ for link in self.scene.system.GetLinks()))
        self.assertTrue(all(not body.IsCollisionEnabled() for body in self.scene.bodies.values()))
        self.assertTrue(all(not body.IsCollisionEnabled() for body in self.scene.environment_bodies.values()))

    def test_zero_gravity_constraint_smoke_test(self) -> None:
        scene = build_mechanical_scene()
        self.assertAlmostEqual(run_constraint_smoke_test(scene), 0.005)

    def test_mechanical_metadata_is_deterministic(self) -> None:
        rebuilt = build_mechanical_scene()
        self.assertEqual(self.scene.body_specs, rebuilt.body_specs)
        self.assertEqual(self.scene.joint_specs, rebuilt.joint_specs)
        self.assertEqual(self.scene.environment_objects, rebuilt.environment_objects)

    def test_headless_validation_succeeds(self) -> None:
        self.assertEqual(validate_mechanical_scene(self.scene), ())
        self.assertIsNone(assert_valid_mechanical_scene(self.scene))


if __name__ == "__main__":
    unittest.main()
