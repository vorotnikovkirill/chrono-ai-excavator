"""Display-free tests for the Milestone 2 static scene."""

from __future__ import annotations

import math
import unittest

from chrono_ai_excavator.static_scene import (
    REQUIRED_OBJECT_NAMES,
    assert_valid_static_scene,
    build_static_scene,
    validate_static_scene,
)


class StaticSceneTests(unittest.TestCase):
    """Exercise scene construction and metadata without importing Irrlicht."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scene = build_static_scene()

    def test_scene_construction_registers_every_body(self) -> None:
        self.assertEqual(len(self.scene.system.GetBodies()), len(self.scene.objects))
        self.assertEqual(set(self.scene.object_names), set(self.scene.bodies))
        self.assertTrue(all(body.IsFixed() for body in self.scene.bodies.values()))

    def test_named_components_are_unique(self) -> None:
        self.assertEqual(len(self.scene.object_names), len(set(self.scene.object_names)))

    def test_required_excavator_and_scene_components_exist(self) -> None:
        self.assertTrue(REQUIRED_OBJECT_NAMES.issubset(self.scene.object_names))
        for component in (
            "excavator.track_left",
            "excavator.track_right",
            "excavator.boom",
            "excavator.stick",
            "excavator.bucket",
        ):
            self.assertIn(component, self.scene.bodies)

    def test_cube_count_is_in_milestone_range(self) -> None:
        self.assertGreaterEqual(self.scene.cube_count, 24)
        self.assertLessEqual(self.scene.cube_count, 36)

    def test_scene_metadata_is_deterministic(self) -> None:
        rebuilt = build_static_scene()
        self.assertEqual(self.scene.objects, rebuilt.objects)
        self.assertEqual(self.scene.camera_position, rebuilt.camera_position)
        self.assertEqual(self.scene.camera_target, rebuilt.camera_target)

    def test_dimensions_are_positive(self) -> None:
        for item in self.scene.objects:
            with self.subTest(item=item.name):
                self.assertTrue(all(value > 0 for value in item.dimensions))

    def test_transforms_are_finite(self) -> None:
        for item in self.scene.objects:
            with self.subTest(item=item.name):
                self.assertTrue(
                    all(math.isfinite(value) for value in (*item.position, *item.rotation))
                )

    def test_headless_validation_succeeds(self) -> None:
        self.assertEqual(validate_static_scene(self.scene), ())
        self.assertIsNone(assert_valid_static_scene(self.scene))


if __name__ == "__main__":
    unittest.main()
