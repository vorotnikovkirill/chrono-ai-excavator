"""Build the Milestone 2 fixed, procedural Project Chrono scene."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import pychrono as chrono


Color = tuple[float, float, float]
Vector3 = tuple[float, float, float]

YELLOW: Color = (1.00, 0.62, 0.05)
WARM_YELLOW: Color = (1.00, 0.78, 0.08)
DARK: Color = (0.10, 0.12, 0.15)
METAL: Color = (0.28, 0.31, 0.35)
WINDOW: Color = (0.08, 0.27, 0.38)
PLATFORM_GRAY: Color = (0.29, 0.32, 0.35)
CONTAINER_ORANGE: Color = (0.95, 0.25, 0.08)

CUBE_COLORS: tuple[Color, ...] = (
    (0.93, 0.16, 0.18),
    (0.10, 0.55, 0.95),
    (0.15, 0.78, 0.35),
    (1.00, 0.78, 0.05),
    (0.67, 0.25, 0.90),
    (1.00, 0.42, 0.08),
)

REQUIRED_OBJECT_NAMES = frozenset(
    {
        "platform",
        "excavator.track_left",
        "excavator.track_right",
        "excavator.lower_chassis",
        "excavator.rotating_platform",
        "excavator.cabin",
        "excavator.counterweight",
        "excavator.boom",
        "excavator.stick",
        "excavator.bucket",
        "container.floor",
        "container.wall_front",
        "container.wall_back",
        "container.wall_left",
        "container.wall_right",
    }
)


@dataclass(frozen=True)
class VisualObject:
    """Display-free description of one named Chrono visual body."""

    name: str
    group: str
    primitive: str
    position: Vector3
    dimensions: Vector3
    color: Color
    rotation: Vector3 = (0.0, 0.0, 0.0)
    cylinder_axis: str = "y"


@dataclass(frozen=True)
class StaticScene:
    """Built Chrono system and deterministic metadata used by the viewer and tests."""

    system: chrono.ChSystemNSC
    objects: tuple[VisualObject, ...]
    bodies: Mapping[str, chrono.ChBody]
    camera_position: Vector3
    camera_target: Vector3

    @property
    def cube_count(self) -> int:
        """Return the number of colored cube bodies."""

        return sum(item.group == "cube" for item in self.objects)

    @property
    def object_names(self) -> tuple[str, ...]:
        """Return names in deterministic construction order."""

        return tuple(item.name for item in self.objects)


class SceneValidationError(ValueError):
    """Raised when a built static scene violates a Milestone 2 invariant."""


def _box_between(
    name: str,
    group: str,
    start: tuple[float, float],
    end: tuple[float, float],
    thickness: float,
    width: float,
    color: Color,
) -> VisualObject:
    """Create box metadata spanning two points in the X-Y plane."""

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return VisualObject(
        name=name,
        group=group,
        primitive="box",
        position=((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, 0.0),
        dimensions=(math.hypot(dx, dy), thickness, width),
        color=color,
        rotation=(0.0, 0.0, math.atan2(dy, dx)),
    )


def _scene_objects() -> tuple[VisualObject, ...]:
    """Return the complete deterministic visual composition."""

    objects: list[VisualObject] = [
        VisualObject(
            "platform",
            "platform",
            "box",
            (0.0, 0.0, -0.65),
            (12.0, 0.40, 9.0),
            PLATFORM_GRAY,
        ),
        VisualObject(
            "excavator.track_left",
            "excavator",
            "box",
            (-3.05, 0.54, 0.82),
            (3.15, 0.68, 0.48),
            DARK,
        ),
        VisualObject(
            "excavator.track_right",
            "excavator",
            "box",
            (-3.05, 0.54, -0.82),
            (3.15, 0.68, 0.48),
            DARK,
        ),
    ]

    for side, z_position in (("left", 0.82), ("right", -0.82)):
        for label, x_position in (("rear", -4.05), ("middle", -3.05), ("front", -2.05)):
            objects.append(
                VisualObject(
                    f"excavator.track_{side}_roller_{label}",
                    "excavator_detail",
                    "cylinder",
                    (x_position, 0.54, z_position),
                    (0.50, 0.50, 0.54),
                    METAL,
                    cylinder_axis="z",
                )
            )

    objects.extend(
        [
            VisualObject(
                "excavator.lower_chassis",
                "excavator",
                "box",
                (-3.05, 1.02, 0.0),
                (2.65, 0.34, 1.75),
                DARK,
            ),
            VisualObject(
                "excavator.rotating_platform",
                "excavator",
                "cylinder",
                (-3.05, 1.28, 0.0),
                (2.20, 0.34, 2.20),
                YELLOW,
            ),
            VisualObject(
                "excavator.rear_body",
                "excavator",
                "box",
                (-3.55, 1.72, -0.10),
                (1.65, 0.75, 1.55),
                YELLOW,
            ),
            VisualObject(
                "excavator.counterweight",
                "excavator",
                "box",
                (-4.34, 1.72, -0.10),
                (0.42, 0.78, 1.48),
                WARM_YELLOW,
            ),
            VisualObject(
                "excavator.cabin",
                "excavator",
                "box",
                (-2.70, 2.18, 0.43),
                (1.15, 1.35, 0.76),
                YELLOW,
            ),
            VisualObject(
                "excavator.cabin_front_window",
                "excavator_detail",
                "box",
                (-2.10, 2.31, 0.43),
                (0.06, 0.82, 0.66),
                WINDOW,
            ),
            VisualObject(
                "excavator.cabin_side_window",
                "excavator_detail",
                "box",
                (-2.72, 2.34, 0.83),
                (0.86, 0.80, 0.05),
                WINDOW,
            ),
            VisualObject(
                "excavator.cabin_roof",
                "excavator_detail",
                "box",
                (-2.69, 2.88, 0.43),
                (1.28, 0.15, 0.90),
                WARM_YELLOW,
            ),
        ]
    )

    objects.extend(
        [
            _box_between(
                "excavator.boom",
                "excavator",
                (-2.40, 1.82),
                (-0.05, 3.35),
                0.42,
                0.48,
                YELLOW,
            ),
            _box_between(
                "excavator.stick",
                "excavator",
                (-0.05, 3.35),
                (1.66, 0.98),
                0.36,
                0.42,
                WARM_YELLOW,
            ),
            VisualObject(
                "excavator.boom_pivot",
                "excavator_detail",
                "cylinder",
                (-2.40, 1.82, 0.0),
                (0.52, 0.52, 0.62),
                METAL,
                cylinder_axis="z",
            ),
            VisualObject(
                "excavator.elbow_pivot",
                "excavator_detail",
                "cylinder",
                (-0.05, 3.35, 0.0),
                (0.46, 0.46, 0.58),
                METAL,
                cylinder_axis="z",
            ),
            VisualObject(
                "excavator.bucket_pivot",
                "excavator_detail",
                "cylinder",
                (1.66, 0.98, 0.0),
                (0.42, 0.42, 0.54),
                METAL,
                cylinder_axis="z",
            ),
            VisualObject(
                "excavator.bucket",
                "excavator",
                "box",
                (2.05, 0.49, 0.0),
                (1.18, 0.20, 1.12),
                YELLOW,
                rotation=(0.0, 0.0, -0.10),
            ),
            VisualObject(
                "excavator.bucket_back",
                "excavator_detail",
                "box",
                (1.62, 0.73, 0.0),
                (0.24, 0.76, 1.12),
                WARM_YELLOW,
                rotation=(0.0, 0.0, -0.32),
            ),
            VisualObject(
                "excavator.bucket_side_left",
                "excavator_detail",
                "box",
                (2.03, 0.61, 0.58),
                (1.05, 0.48, 0.10),
                YELLOW,
                rotation=(0.0, 0.0, -0.10),
            ),
            VisualObject(
                "excavator.bucket_side_right",
                "excavator_detail",
                "box",
                (2.03, 0.61, -0.58),
                (1.05, 0.48, 0.10),
                YELLOW,
                rotation=(0.0, 0.0, -0.10),
            ),
        ]
    )

    cube_layers = (
        (0.45, ((2.76, -0.78), (3.30, -0.82), (3.85, -0.76), (4.39, -0.81),
                (2.72, -0.25), (3.27, -0.20), (3.82, -0.27), (4.35, -0.22),
                (2.78, 0.30), (3.33, 0.25), (3.87, 0.32), (4.42, 0.27),
                (2.74, 0.82), (3.29, 0.78), (3.84, 0.84), (4.38, 0.79))),
        (0.92, ((3.02, -0.52), (3.59, -0.48), (4.13, -0.54),
                (3.06, 0.02), (3.63, -0.03), (4.17, 0.04),
                (3.01, 0.55), (3.57, 0.51), (4.12, 0.57))),
        (1.39, ((3.34, -0.28), (3.90, -0.24), (3.31, 0.29), (3.88, 0.25))),
        (1.86, ((3.61, 0.01),)),
    )
    cube_index = 0
    for y_position, coordinates in cube_layers:
        for x_position, z_position in coordinates:
            objects.append(
                VisualObject(
                    f"cube.{cube_index:02d}",
                    "cube",
                    "box",
                    (x_position, y_position, z_position),
                    (0.46, 0.46, 0.46),
                    CUBE_COLORS[cube_index % len(CUBE_COLORS)],
                    rotation=(0.0, math.radians((cube_index * 17) % 28 - 14), 0.0),
                )
            )
            cube_index += 1

    container_x = 2.20
    container_z = -3.05
    objects.extend(
        [
            VisualObject(
                "container.floor",
                "container",
                "box",
                (container_x, 0.32, container_z),
                (2.65, 0.18, 2.20),
                CONTAINER_ORANGE,
            ),
            VisualObject(
                "container.wall_front",
                "container",
                "box",
                (container_x, 0.91, container_z + 1.02),
                (2.65, 1.35, 0.16),
                CONTAINER_ORANGE,
            ),
            VisualObject(
                "container.wall_back",
                "container",
                "box",
                (container_x, 0.91, container_z - 1.02),
                (2.65, 1.35, 0.16),
                CONTAINER_ORANGE,
            ),
            VisualObject(
                "container.wall_left",
                "container",
                "box",
                (container_x - 1.24, 0.91, container_z),
                (0.16, 1.35, 1.90),
                CONTAINER_ORANGE,
            ),
            VisualObject(
                "container.wall_right",
                "container",
                "box",
                (container_x + 1.24, 0.91, container_z),
                (0.16, 1.35, 1.90),
                CONTAINER_ORANGE,
            ),
        ]
    )
    return tuple(objects)


def _make_body(item: VisualObject) -> chrono.ChBody:
    """Create one fixed, collision-free body from metadata."""

    if item.primitive == "box":
        body = chrono.ChBodyEasyBox(*item.dimensions, 1000.0, True, False)
    elif item.primitive == "cylinder":
        if item.cylinder_axis == "y":
            axis = chrono.ChAxis_Y
            radius = item.dimensions[0] / 2
            height = item.dimensions[1]
        elif item.cylinder_axis == "z":
            axis = chrono.ChAxis_Z
            radius = item.dimensions[0] / 2
            height = item.dimensions[2]
        else:
            raise ValueError(f"Unsupported cylinder axis: {item.cylinder_axis}")
        body = chrono.ChBodyEasyCylinder(axis, radius, height, 1000.0, True, False)
    else:
        raise ValueError(f"Unsupported primitive: {item.primitive}")

    body.SetName(item.name)
    body.SetFixed(True)
    body.SetPos(chrono.ChVector3d(*item.position))
    rotation_x, rotation_y, rotation_z = item.rotation
    if rotation_x:
        body.SetRot(chrono.QuatFromAngleX(rotation_x))
    elif rotation_y:
        body.SetRot(chrono.QuatFromAngleY(rotation_y))
    elif rotation_z:
        body.SetRot(chrono.QuatFromAngleZ(rotation_z))
    body.GetVisualShape(0).SetColor(chrono.ChColor(*item.color))
    return body


def build_static_scene() -> StaticScene:
    """Build and return the complete static scene without creating a display."""

    system = chrono.ChSystemNSC()
    system.SetGravitationalAcceleration(chrono.ChVector3d(0.0, 0.0, 0.0))
    objects = _scene_objects()
    bodies: dict[str, chrono.ChBody] = {}
    for item in objects:
        body = _make_body(item)
        system.AddBody(body)
        bodies[item.name] = body

    return StaticScene(
        system=system,
        objects=objects,
        bodies=MappingProxyType(bodies),
        camera_position=(10.4, 7.2, 11.2),
        camera_target=(-0.1, 1.20, -0.45),
    )


def validate_static_scene(scene: StaticScene) -> tuple[str, ...]:
    """Return validation failures without opening a display."""

    errors: list[str] = []
    names = scene.object_names
    missing = sorted(REQUIRED_OBJECT_NAMES.difference(names))
    if missing:
        errors.append("Missing required objects: " + ", ".join(missing))
    if len(names) != len(set(names)):
        errors.append("Object names must be unique")
    if set(names) != set(scene.bodies):
        errors.append("Body registry does not match scene metadata")
    if len(scene.system.GetBodies()) != len(scene.objects):
        errors.append("Chrono system body count does not match scene metadata")
    if not 24 <= scene.cube_count <= 36:
        errors.append(f"Cube count {scene.cube_count} is outside the range 24-36")

    for item in scene.objects:
        if any(not math.isfinite(value) for value in (*item.position, *item.rotation)):
            errors.append(f"{item.name} has a non-finite transform")
        if any(not math.isfinite(value) or value <= 0 for value in item.dimensions):
            errors.append(f"{item.name} has invalid dimensions")
        if any(abs(item.position[index]) + item.dimensions[index] / 2 > limit
               for index, limit in enumerate((8.0, 6.0, 6.0))):
            errors.append(f"{item.name} exceeds the scene bounding region")
        body = scene.bodies.get(item.name)
        if body is None or body.GetName() != item.name:
            errors.append(f"{item.name} is not correctly registered")
        elif not body.IsFixed():
            errors.append(f"{item.name} is not fixed")

    for label, vector in (
        ("camera position", scene.camera_position),
        ("camera target", scene.camera_target),
    ):
        if any(not math.isfinite(value) for value in vector):
            errors.append(f"The {label} is not finite")
    return tuple(errors)


def assert_valid_static_scene(scene: StaticScene) -> None:
    """Raise a concise error when static validation fails."""

    errors = validate_static_scene(scene)
    if errors:
        raise SceneValidationError("; ".join(errors))


def summarize_static_scene(scene: StaticScene) -> str:
    """Return a compact deterministic object summary."""

    counts = Counter(item.group for item in scene.objects)
    return (
        f"{len(scene.objects)} fixed visual bodies; "
        f"{counts['excavator']} excavator components; "
        f"{counts['excavator_detail']} excavator details; "
        f"{counts['cube']} cubes; {counts['container']} container parts; "
        f"{counts['platform']} platform"
    )
