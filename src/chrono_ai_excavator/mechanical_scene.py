"""Build the Milestone 3 articulated mechanical excavator scene."""

from __future__ import annotations

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import pychrono as chrono

from chrono_ai_excavator.static_scene import (
    VisualObject,
    _make_body,
    _scene_objects,
)


Vector3 = tuple[float, float, float]

PRIMARY_BODY_NAMES = ("BASE", "UPPER", "BOOM", "STICK", "BUCKET")
JOINT_NAMES = ("J0_SLEW", "J1_BOOM", "J2_STICK", "J3_BUCKET")
VERTICAL_AXIS: Vector3 = (0.0, 1.0, 0.0)
ARM_HINGE_AXIS: Vector3 = (0.0, 0.0, 1.0)


@dataclass(frozen=True)
class MechanicalBodySpec:
    """Preliminary toy-model properties for one primary mechanical body."""

    name: str
    position: Vector3
    mass: float
    inertia: Vector3
    fixed: bool
    visual_names: tuple[str, ...]


@dataclass(frozen=True)
class JointSpec:
    """Deterministic topology and world-frame metadata for one revolute joint."""

    name: str
    parent: str
    child: str
    pivot: Vector3
    axis: Vector3


@dataclass(frozen=True)
class MechanicalScene:
    """Articulated Chrono system and display-free validation metadata."""

    system: chrono.ChSystemNSC
    bodies: Mapping[str, chrono.ChBody]
    joints: Mapping[str, chrono.ChLinkLockRevolute]
    body_specs: tuple[MechanicalBodySpec, ...]
    joint_specs: tuple[JointSpec, ...]
    environment_objects: tuple[VisualObject, ...]
    environment_bodies: Mapping[str, chrono.ChBody]
    camera_position: Vector3
    camera_target: Vector3

    @property
    def cube_count(self) -> int:
        """Return the retained fixed cube count."""

        return sum(item.group == "cube" for item in self.environment_objects)


class MechanicalValidationError(ValueError):
    """Raised when the Milestone 3 architecture violates an invariant."""


def _body_for_visual(item: VisualObject) -> str:
    """Map accepted excavator visuals to one of five mechanical bodies."""

    name = item.name
    if name in {
        "excavator.track_left",
        "excavator.track_right",
        "excavator.lower_chassis",
    } or name.startswith(("excavator.track_left_", "excavator.track_right_")):
        return "BASE"
    if name in {
        "excavator.rotating_platform",
        "excavator.rear_body",
        "excavator.counterweight",
        "excavator.cabin",
        "excavator.cabin_front_window",
        "excavator.cabin_side_window",
        "excavator.cabin_roof",
        "excavator.boom_pivot",
    }:
        return "UPPER"
    if name in {"excavator.boom", "excavator.elbow_pivot"}:
        return "BOOM"
    if name in {"excavator.stick", "excavator.bucket_pivot"}:
        return "STICK"
    if name in {
        "excavator.bucket",
        "excavator.bucket_back",
        "excavator.bucket_side_left",
        "excavator.bucket_side_right",
    }:
        return "BUCKET"
    raise ValueError(f"Unassigned excavator visual: {name}")


def _rotation(item: VisualObject) -> chrono.ChQuaterniond:
    """Return the accepted visual rotation as a Chrono quaternion."""

    rotation_x, rotation_y, rotation_z = item.rotation
    if rotation_x:
        return chrono.QuatFromAngleX(rotation_x)
    if rotation_y:
        return chrono.QuatFromAngleY(rotation_y)
    if rotation_z:
        return chrono.QuatFromAngleZ(rotation_z)
    return chrono.ChQuaterniond(1.0, 0.0, 0.0, 0.0)


def _add_visual_shape(
    body: chrono.ChBody, item: VisualObject, body_position: Vector3
) -> None:
    """Attach one accepted primitive to a primary body in its initial pose."""

    if item.primitive == "box":
        shape = chrono.ChVisualShapeBox(chrono.ChVector3d(*item.dimensions))
        rotation = _rotation(item)
    elif item.primitive == "cylinder":
        if item.cylinder_axis == "y":
            radius = item.dimensions[0] / 2
            height = item.dimensions[1]
            rotation = chrono.QuatFromAngleX(-math.pi / 2)
        elif item.cylinder_axis == "z":
            radius = item.dimensions[0] / 2
            height = item.dimensions[2]
            rotation = chrono.ChQuaterniond(1.0, 0.0, 0.0, 0.0)
        else:
            raise ValueError(f"Unsupported cylinder axis: {item.cylinder_axis}")
        shape = chrono.ChVisualShapeCylinder(radius, height)
    else:
        raise ValueError(f"Unsupported primitive: {item.primitive}")

    shape.SetColor(chrono.ChColor(*item.color))
    local_position = chrono.ChVector3d(
        item.position[0] - body_position[0],
        item.position[1] - body_position[1],
        item.position[2] - body_position[2],
    )
    body.AddVisualShape(shape, chrono.ChFramed(local_position, rotation))


def _body_specs(objects: tuple[VisualObject, ...]) -> tuple[MechanicalBodySpec, ...]:
    """Return deterministic placeholder body properties and visual ownership."""

    visual_names: dict[str, list[str]] = {name: [] for name in PRIMARY_BODY_NAMES}
    for item in objects:
        if item.group.startswith("excavator"):
            visual_names[_body_for_visual(item)].append(item.name)

    return (
        MechanicalBodySpec(
            "BASE", (-3.05, 1.02, 0.0), 200.0, (180.0, 220.0, 180.0), True,
            tuple(visual_names["BASE"]),
        ),
        MechanicalBodySpec(
            "UPPER", (-3.05, 1.28, 0.0), 120.0, (95.0, 120.0, 95.0), False,
            tuple(visual_names["UPPER"]),
        ),
        MechanicalBodySpec(
            "BOOM", (-2.40, 1.82, 0.0), 35.0, (14.0, 45.0, 45.0), False,
            tuple(visual_names["BOOM"]),
        ),
        MechanicalBodySpec(
            "STICK", (-0.05, 3.35, 0.0), 22.0, (9.0, 24.0, 24.0), False,
            tuple(visual_names["STICK"]),
        ),
        MechanicalBodySpec(
            "BUCKET", (1.66, 0.98, 0.0), 15.0, (5.0, 8.0, 8.0), False,
            tuple(visual_names["BUCKET"]),
        ),
    )


def _joint_specs() -> tuple[JointSpec, ...]:
    """Return the agreed four-joint topology in the accepted initial pose."""

    return (
        JointSpec("J0_SLEW", "BASE", "UPPER", (-3.05, 1.28, 0.0), VERTICAL_AXIS),
        JointSpec("J1_BOOM", "UPPER", "BOOM", (-2.40, 1.82, 0.0), ARM_HINGE_AXIS),
        JointSpec("J2_STICK", "BOOM", "STICK", (-0.05, 3.35, 0.0), ARM_HINGE_AXIS),
        JointSpec("J3_BUCKET", "STICK", "BUCKET", (1.66, 0.98, 0.0), ARM_HINGE_AXIS),
    )


def _joint_frame(spec: JointSpec) -> chrono.ChFramed:
    """Create an absolute frame whose Z-axis is the desired revolute axis."""

    rotation = (
        chrono.QuatFromAngleX(-math.pi / 2)
        if spec.name == "J0_SLEW"
        else chrono.ChQuaterniond(1.0, 0.0, 0.0, 0.0)
    )
    return chrono.ChFramed(chrono.ChVector3d(*spec.pivot), rotation)


def build_mechanical_scene() -> MechanicalScene:
    """Build the articulated system without importing a visualization module."""

    system = chrono.ChSystemNSC()
    system.SetGravitationalAcceleration(chrono.ChVector3d(0.0, 0.0, 0.0))
    objects = _scene_objects()
    objects_by_name = {item.name: item for item in objects}
    body_specs = _body_specs(objects)

    bodies: dict[str, chrono.ChBody] = {}
    for spec in body_specs:
        body = chrono.ChBody()
        body.SetName(spec.name)
        body.SetPos(chrono.ChVector3d(*spec.position))
        body.SetMass(spec.mass)
        body.SetInertiaXX(chrono.ChVector3d(*spec.inertia))
        body.SetFixed(spec.fixed)
        body.EnableCollision(False)
        for visual_name in spec.visual_names:
            _add_visual_shape(body, objects_by_name[visual_name], spec.position)
        system.AddBody(body)
        bodies[spec.name] = body

    environment_objects = tuple(
        item for item in objects if not item.group.startswith("excavator")
    )
    environment_bodies: dict[str, chrono.ChBody] = {}
    for item in environment_objects:
        body = _make_body(item)
        system.AddBody(body)
        environment_bodies[item.name] = body

    joint_specs = _joint_specs()
    joints: dict[str, chrono.ChLinkLockRevolute] = {}
    for spec in joint_specs:
        joint = chrono.ChLinkLockRevolute()
        joint.SetName(spec.name)
        joint.Initialize(bodies[spec.parent], bodies[spec.child], _joint_frame(spec))
        system.AddLink(joint)
        joints[spec.name] = joint

    return MechanicalScene(
        system=system,
        bodies=MappingProxyType(bodies),
        joints=MappingProxyType(joints),
        body_specs=body_specs,
        joint_specs=joint_specs,
        environment_objects=environment_objects,
        environment_bodies=MappingProxyType(environment_bodies),
        camera_position=(10.4, 7.2, 11.2),
        camera_target=(-0.1, 1.20, -0.45),
    )


def _vector_tuple(vector: chrono.ChVector3d) -> Vector3:
    """Convert a Chrono vector to an immutable tuple."""

    return (vector.x, vector.y, vector.z)


def _finite(values: tuple[float, ...]) -> bool:
    """Return whether all values are finite."""

    return all(math.isfinite(value) for value in values)


def _normalized(axis: Vector3) -> bool:
    """Return whether an axis is unit length within validation tolerance."""

    return math.isclose(math.sqrt(sum(value * value for value in axis)), 1.0, abs_tol=1e-9)


def _parallel(first: Vector3, second: Vector3) -> bool:
    """Return whether two normalized axes are parallel in either direction."""

    dot = sum(a * b for a, b in zip(first, second))
    return math.isclose(abs(dot), 1.0, abs_tol=1e-9)


def validate_mechanical_scene(scene: MechanicalScene) -> tuple[str, ...]:
    """Return architecture validation failures without opening a display."""

    errors: list[str] = []
    if tuple(scene.bodies) != PRIMARY_BODY_NAMES:
        errors.append("Primary mechanical bodies must be BASE, UPPER, BOOM, STICK, BUCKET")
    if len(scene.bodies) != 5:
        errors.append("Exactly five primary mechanical bodies are required")
    if scene.bodies.get("BASE") is None or not scene.bodies["BASE"].IsFixed():
        errors.append("BASE must be fixed")
    for name in PRIMARY_BODY_NAMES[1:]:
        body = scene.bodies.get(name)
        if body is None or body.IsFixed():
            errors.append(f"{name} must be dynamic")

    for spec in scene.body_specs:
        body = scene.bodies.get(spec.name)
        if body is None:
            continue
        position = _vector_tuple(body.GetPos())
        rotation = body.GetRot()
        quaternion = (rotation.e0, rotation.e1, rotation.e2, rotation.e3)
        inertia = _vector_tuple(body.GetInertiaXX())
        if not _finite((*position, *quaternion)):
            errors.append(f"{spec.name} has a non-finite transform")
        if not math.isfinite(body.GetMass()) or body.GetMass() <= 0:
            errors.append(f"{spec.name} must have positive finite mass")
        if not _finite(inertia) or any(value <= 0 for value in inertia):
            errors.append(f"{spec.name} must have positive finite principal inertia")
        if body.IsCollisionEnabled():
            errors.append(f"{spec.name} must remain collision-free")

    if tuple(scene.joints) != JOINT_NAMES or len(scene.joints) != 4:
        errors.append("Exactly four named revolute joints are required")
    for spec in scene.joint_specs:
        joint = scene.joints.get(spec.name)
        if joint is None:
            continue
        if (
            joint.GetBody1() != scene.bodies[spec.parent]
            or joint.GetBody2() != scene.bodies[spec.child]
        ):
            errors.append(f"{spec.name} has incorrect body connectivity")
        if not _finite(spec.pivot):
            errors.append(f"{spec.name} has a non-finite pivot")
        if not _finite(spec.axis) or not _normalized(spec.axis):
            errors.append(f"{spec.name} has an invalid axis")
        actual_axis = _vector_tuple(joint.GetFrame1Abs().GetRot().GetAxisZ())
        if not _parallel(actual_axis, spec.axis):
            errors.append(f"{spec.name} frame axis does not match its metadata")

    joint_specs = {spec.name: spec for spec in scene.joint_specs}
    if "J0_SLEW" in joint_specs and not _parallel(joint_specs["J0_SLEW"].axis, VERTICAL_AXIS):
        errors.append("J0_SLEW must align with scene vertical")
    arm_axes = [joint_specs[name].axis for name in JOINT_NAMES[1:] if name in joint_specs]
    if len(arm_axes) != 3 or any(not _parallel(arm_axes[0], axis) for axis in arm_axes[1:]):
        errors.append("J1_BOOM, J2_STICK, and J3_BUCKET must have parallel axes")

    environment_names = {item.name for item in scene.environment_objects}
    if "platform" not in environment_names:
        errors.append("The platform is missing")
    if scene.cube_count != 30:
        errors.append(f"Expected 30 fixed cubes, found {scene.cube_count}")
    required_container = {f"container.{name}" for name in ("floor", "wall_front", "wall_back", "wall_left", "wall_right")}
    if not required_container.issubset(environment_names):
        errors.append("The receiving container is incomplete")
    if any(not body.IsFixed() for body in scene.environment_bodies.values()):
        errors.append("All environment bodies and cubes must remain fixed")
    if any(body.IsCollisionEnabled() for body in scene.environment_bodies.values()):
        errors.append("Contact and collision must remain disabled")
    if any("Motor" in type(link).__name__ for link in scene.system.GetLinks()):
        errors.append("Motor links are outside Milestone 3 scope")
    return tuple(errors)


def assert_valid_mechanical_scene(scene: MechanicalScene) -> None:
    """Raise a concise error when architecture validation fails."""

    errors = validate_mechanical_scene(scene)
    if errors:
        raise MechanicalValidationError("; ".join(errors))


def run_constraint_smoke_test(
    scene: MechanicalScene, steps: int = 5, step_size: float = 0.001
) -> float:
    """Advance a zero-gravity, zero-velocity architecture stability check."""

    if steps <= 0 or step_size <= 0:
        raise ValueError("Smoke-test steps and step size must be positive")
    scene.system.SetGravitationalAcceleration(chrono.ChVector3d(0.0, 0.0, 0.0))
    zero = chrono.ChVector3d(0.0, 0.0, 0.0)
    for body in scene.bodies.values():
        body.SetLinVel(zero)
        body.SetAngVelLocal(zero)
    for _ in range(steps):
        scene.system.DoStepDynamics(step_size)
    for name, body in scene.bodies.items():
        position = _vector_tuple(body.GetPos())
        rotation = body.GetRot()
        state = (*position, rotation.e0, rotation.e1, rotation.e2, rotation.e3)
        if not _finite(state) or any(abs(value) > 100.0 for value in position):
            raise MechanicalValidationError(f"{name} became unstable during smoke test")
    return scene.system.GetChTime()


def summarize_mechanical_scene(scene: MechanicalScene) -> str:
    """Return a compact deterministic architecture summary."""

    dynamic_count = sum(not body.IsFixed() for body in scene.bodies.values())
    return (
        f"{len(scene.bodies)} primary bodies; {dynamic_count} dynamic; "
        f"BASE fixed={scene.bodies['BASE'].IsFixed()}; "
        f"{len(scene.joints)} revolute joints: {', '.join(scene.joints)}"
    )
