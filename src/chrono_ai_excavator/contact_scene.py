"""Build and validate the Milestone 5 NSC contact scene."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import pychrono as chrono

from chrono_ai_excavator.static_scene import (
    CUBE_COLORS,
    VisualObject,
    _make_body,
    _scene_objects,
)


Vector3 = tuple[float, float, float]
Color = tuple[float, float, float]

GRAVITY: Vector3 = (0.0, -9.81, 0.0)
CUBE_COUNT = 30
CUBE_DIMENSIONS: Vector3 = (0.46, 0.46, 0.46)
CUBE_MASS = 0.25
TIMESTEP = 0.002
PILE_DURATION = 3.0
PLATFORM_PENETRATION_TOLERANCE = 0.02
FINAL_LINEAR_SPEED_LIMIT = 0.25

PLATFORM_NAME = "platform"
CONTAINER_NAMES = (
    "container.floor",
    "container.wall_front",
    "container.wall_back",
    "container.wall_left",
    "container.wall_right",
)
BUCKET_NAMES = (
    "excavator.bucket",
    "excavator.bucket_back",
    "excavator.bucket_side_left",
    "excavator.bucket_side_right",
)


@dataclass(frozen=True)
class ContactMaterialSpec:
    """Deterministic NSC material metadata."""

    name: str
    friction: float
    restitution: float


MATERIAL_SPECS: Mapping[str, ContactMaterialSpec] = MappingProxyType(
    {
        "cube": ContactMaterialSpec("cube", 0.45, 0.05),
        "environment": ContactMaterialSpec("environment", 0.55, 0.03),
        "bucket": ContactMaterialSpec("bucket", 0.60, 0.02),
    }
)


@dataclass(frozen=True)
class CubeSpec:
    """Mass properties and deterministic initial state for one cube."""

    name: str
    position: Vector3
    dimensions: Vector3
    color: Color
    mass: float
    inertia: Vector3


@dataclass(frozen=True)
class ContactScene:
    """Contact-enabled system and display-independent metadata."""

    system: chrono.ChSystemNSC
    cubes: tuple[chrono.ChBody, ...]
    cube_specs: tuple[CubeSpec, ...]
    platform: chrono.ChBody
    platform_spec: VisualObject
    container_bodies: Mapping[str, chrono.ChBody]
    bucket_bodies: Mapping[str, chrono.ChBody]
    visual_bodies: Mapping[str, chrono.ChBody]
    material_specs: Mapping[str, ContactMaterialSpec]
    camera_position: Vector3
    camera_target: Vector3


@dataclass(frozen=True)
class PileResult:
    """Measured outcome of the deterministic 30-cube scenario."""

    cube_count: int
    simulated_duration: float
    timestep: float
    peak_contact_count: int
    final_contact_count: int
    maximum_final_linear_speed: float
    maximum_final_angular_speed: float
    minimum_cube_bottom: float
    platform_top: float
    penetration_tolerance: float
    platform_penetration_passed: bool
    cube_platform_passed: bool
    cubes_fell: bool
    cubes_within_platform: bool
    finite: bool
    settled: bool
    simulation_wall_seconds: float


@dataclass(frozen=True)
class ProbeResult:
    """Outcome of one small deterministic contact-pair probe."""

    name: str
    passed: bool
    peak_contact_count: int
    final_contact_count: int
    final_position: Vector3
    final_linear_speed: float
    finite: bool
    simulation_wall_seconds: float


@dataclass(frozen=True)
class ContactValidationResult:
    """Complete headless Milestone 5 contact result."""

    pile: PileResult
    cube_cube: ProbeResult
    cube_container: ProbeResult
    cube_bucket: ProbeResult

    @property
    def simulation_wall_seconds(self) -> float:
        """Return time measured only inside required dynamics loops."""

        return (
            self.pile.simulation_wall_seconds
            + self.cube_cube.simulation_wall_seconds
            + self.cube_container.simulation_wall_seconds
            + self.cube_bucket.simulation_wall_seconds
        )


class ContactValidationError(ValueError):
    """Raised when a Milestone 5 contact invariant fails."""


def _box_inertia(mass: float, dimensions: Vector3) -> Vector3:
    """Return principal inertia of a solid box about its center."""

    x, y, z = dimensions
    return (
        mass * (y * y + z * z) / 12.0,
        mass * (x * x + z * z) / 12.0,
        mass * (x * x + y * y) / 12.0,
    )


CUBE_INERTIA = _box_inertia(CUBE_MASS, CUBE_DIMENSIONS)


def _material(spec: ContactMaterialSpec) -> chrono.ChContactMaterialNSC:
    """Create one minimal binding-compatible NSC material."""

    material = chrono.ChContactMaterialNSC()
    material.SetFriction(spec.friction)
    material.SetRestitution(spec.restitution)
    return material


def _set_rotation(body: chrono.ChBody, rotation: Vector3) -> None:
    """Apply accepted single-axis visual metadata rotation."""

    rotation_x, rotation_y, rotation_z = rotation
    if rotation_x:
        body.SetRot(chrono.QuatFromAngleX(rotation_x))
    elif rotation_y:
        body.SetRot(chrono.QuatFromAngleY(rotation_y))
    elif rotation_z:
        body.SetRot(chrono.QuatFromAngleZ(rotation_z))


def _contact_box(
    item: VisualObject,
    material: chrono.ChContactMaterialNSC,
    *,
    fixed: bool,
    mass: float | None = None,
) -> chrono.ChBody:
    """Create a visual box whose collision geometry matches its metadata."""

    volume = math.prod(item.dimensions)
    density = (mass / volume) if mass is not None else 1000.0
    body = chrono.ChBodyEasyBox(
        *item.dimensions,
        density,
        True,
        True,
        material,
    )
    body.SetName(item.name)
    body.SetFixed(fixed)
    body.SetPos(chrono.ChVector3d(*item.position))
    _set_rotation(body, item.rotation)
    body.GetVisualShape(0).SetColor(chrono.ChColor(*item.color))
    body.EnableCollision(True)
    if mass is not None:
        body.SetMass(mass)
        body.SetInertiaXX(chrono.ChVector3d(*_box_inertia(mass, item.dimensions)))
    return body


def _release_specs() -> tuple[CubeSpec, ...]:
    """Return a compact two-layer release grid with 0.04 m separation."""

    positions: list[Vector3] = []
    for layer in range(2):
        y = 0.48 + 0.50 * layer
        for z_index in range(3):
            z = -0.50 + 0.50 * z_index
            for x_index in range(5):
                x = 2.85 + 0.50 * x_index
                positions.append((x, y, z))
    return tuple(
        CubeSpec(
            name=f"cube.{index:02d}",
            position=position,
            dimensions=CUBE_DIMENSIONS,
            color=CUBE_COLORS[index % len(CUBE_COLORS)],
            mass=CUBE_MASS,
            inertia=CUBE_INERTIA,
        )
        for index, position in enumerate(positions)
    )


def _new_system() -> chrono.ChSystemNSC:
    """Create NSC system with the installed Bullet backend explicitly selected."""

    system = chrono.ChSystemNSC()
    system.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
    system.SetGravitationalAcceleration(chrono.ChVector3d(*GRAVITY))
    return system


def build_contact_scene() -> ContactScene:
    """Build the separate fixed-excavator Milestone 5 contact scene."""

    system = _new_system()
    objects = _scene_objects()
    objects_by_name = {item.name: item for item in objects}
    cube_material = _material(MATERIAL_SPECS["cube"])
    environment_material = _material(MATERIAL_SPECS["environment"])
    bucket_material = _material(MATERIAL_SPECS["bucket"])

    platform = _contact_box(
        objects_by_name[PLATFORM_NAME], environment_material, fixed=True
    )
    system.AddBody(platform)

    container_bodies: dict[str, chrono.ChBody] = {}
    for name in CONTAINER_NAMES:
        body = _contact_box(objects_by_name[name], environment_material, fixed=True)
        system.AddBody(body)
        container_bodies[name] = body

    bucket_bodies: dict[str, chrono.ChBody] = {}
    for name in BUCKET_NAMES:
        body = _contact_box(objects_by_name[name], bucket_material, fixed=True)
        system.AddBody(body)
        bucket_bodies[name] = body

    contact_names = {PLATFORM_NAME, *CONTAINER_NAMES, *BUCKET_NAMES}
    visual_bodies: dict[str, chrono.ChBody] = {}
    for item in objects:
        if item.group == "cube" or item.name in contact_names:
            continue
        body = _make_body(item)
        system.AddBody(body)
        visual_bodies[item.name] = body

    cube_specs = _release_specs()
    cubes: list[chrono.ChBody] = []
    for spec in cube_specs:
        item = VisualObject(
            spec.name,
            "cube",
            "box",
            spec.position,
            spec.dimensions,
            spec.color,
        )
        body = _contact_box(item, cube_material, fixed=False, mass=spec.mass)
        system.AddBody(body)
        cubes.append(body)

    return ContactScene(
        system=system,
        cubes=tuple(cubes),
        cube_specs=cube_specs,
        platform=platform,
        platform_spec=objects_by_name[PLATFORM_NAME],
        container_bodies=MappingProxyType(container_bodies),
        bucket_bodies=MappingProxyType(bucket_bodies),
        visual_bodies=MappingProxyType(visual_bodies),
        material_specs=MATERIAL_SPECS,
        camera_position=(10.4, 7.2, 11.2),
        camera_target=(-0.1, 1.20, -0.45),
    )


def _vector_tuple(vector: chrono.ChVector3d) -> Vector3:
    return (vector.x, vector.y, vector.z)


def _finite_body(body: chrono.ChBody) -> bool:
    position = _vector_tuple(body.GetPos())
    velocity = _vector_tuple(body.GetLinVel())
    angular = _vector_tuple(body.GetAngVelLocal())
    rotation = body.GetRot()
    return all(
        math.isfinite(value)
        for value in (
            *position,
            *velocity,
            *angular,
            rotation.e0,
            rotation.e1,
            rotation.e2,
            rotation.e3,
        )
    )


def _speed(vector: chrono.ChVector3d) -> float:
    return math.sqrt(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z)


def validate_contact_scene(scene: ContactScene) -> tuple[str, ...]:
    """Return construction failures without advancing dynamics."""

    errors: list[str] = []
    if not isinstance(scene.system, chrono.ChSystemNSC):
        errors.append("Contact scene must use ChSystemNSC")
    gravity = _vector_tuple(scene.system.GetGravitationalAcceleration())
    if any(not math.isclose(a, b, abs_tol=1e-12) for a, b in zip(gravity, GRAVITY)):
        errors.append("Contact scene gravity must be (0, -9.81, 0)")
    if scene.system.GetCollisionSystem() is None:
        errors.append("Contact collision system is not initialized")
    if len(scene.cubes) != CUBE_COUNT or len(scene.cube_specs) != CUBE_COUNT:
        errors.append("Exactly 30 dynamic cubes are required")
    for body, spec in zip(scene.cubes, scene.cube_specs):
        if body.IsFixed():
            errors.append(f"{spec.name} must be dynamic")
        if not body.IsCollisionEnabled():
            errors.append(f"{spec.name} must have collision enabled")
        if not math.isclose(body.GetMass(), spec.mass, abs_tol=1e-12):
            errors.append(f"{spec.name} has incorrect mass")
        inertia = _vector_tuple(body.GetInertiaXX())
        if any(value <= 0 for value in inertia):
            errors.append(f"{spec.name} must have positive inertia")
        if not _finite_body(body):
            errors.append(f"{spec.name} has a non-finite initial state")
    fixed_contact_bodies = (
        scene.platform,
        *scene.container_bodies.values(),
        *scene.bucket_bodies.values(),
    )
    if any(not body.IsFixed() for body in fixed_contact_bodies):
        errors.append("Platform, container, and bucket contact bodies must remain fixed")
    if any(not body.IsCollisionEnabled() for body in fixed_contact_bodies):
        errors.append("Platform, container, and bucket collision must be enabled")
    if tuple(scene.container_bodies) != CONTAINER_NAMES:
        errors.append("Container collision body set is incomplete")
    if tuple(scene.bucket_bodies) != BUCKET_NAMES:
        errors.append("Bucket collision body set is incomplete")
    if any("Motor" in type(link).__name__ for link in scene.system.GetLinks()):
        errors.append("Motors are excluded from the contact-isolation scene")

    half = CUBE_DIMENSIONS[0] / 2.0
    platform_top = (
        scene.platform_spec.position[1] + scene.platform_spec.dimensions[1] / 2.0
    )
    if min(spec.position[1] - half for spec in scene.cube_specs) <= platform_top:
        errors.append("Release cubes must start above the platform")
    for index, first in enumerate(scene.cube_specs):
        for second in scene.cube_specs[index + 1 :]:
            if all(
                abs(a - b) < CUBE_DIMENSIONS[axis]
                for axis, (a, b) in enumerate(zip(first.position, second.position))
            ):
                errors.append(f"Initial cube overlap: {first.name} and {second.name}")
                break
    return tuple(errors)


def assert_valid_contact_scene(scene: ContactScene) -> None:
    """Raise a concise exception for construction errors."""

    errors = validate_contact_scene(scene)
    if errors:
        raise ContactValidationError("; ".join(errors))


def run_pile_scenario(scene: ContactScene) -> PileResult:
    """Advance the deterministic pile and return acceptance metadata."""

    assert_valid_contact_scene(scene)
    initial_average_y = sum(spec.position[1] for spec in scene.cube_specs) / CUBE_COUNT
    peak_contacts = 0
    steps = round(PILE_DURATION / TIMESTEP)
    wall_start = time.perf_counter()
    for _ in range(steps):
        scene.system.DoStepDynamics(TIMESTEP)
        peak_contacts = max(peak_contacts, scene.system.GetNumContacts())
    wall_seconds = time.perf_counter() - wall_start

    positions = [_vector_tuple(body.GetPos()) for body in scene.cubes]
    finite = all(_finite_body(body) for body in scene.cubes)
    max_linear = max(_speed(body.GetLinVel()) for body in scene.cubes)
    max_angular = max(_speed(body.GetAngVelLocal()) for body in scene.cubes)
    half = CUBE_DIMENSIONS[1] / 2.0
    minimum_bottom = min(position[1] - half for position in positions)
    platform_top = (
        scene.platform_spec.position[1] + scene.platform_spec.dimensions[1] / 2.0
    )
    penetration_passed = (
        minimum_bottom >= platform_top - PLATFORM_PENETRATION_TOLERANCE
    )
    half_x = scene.platform_spec.dimensions[0] / 2.0
    half_z = scene.platform_spec.dimensions[2] / 2.0
    platform_x = scene.platform_spec.position[0]
    platform_z = scene.platform_spec.position[2]
    cubes_within_platform = all(
        platform_x - half_x <= x <= platform_x + half_x
        and platform_z - half_z <= z <= platform_z + half_z
        for x, _, z in positions
    )
    final_average_y = sum(position[1] for position in positions) / CUBE_COUNT
    cubes_fell = final_average_y < initial_average_y - 0.02
    final_contacts = scene.system.GetNumContacts()
    cube_platform_passed = peak_contacts > 0 and penetration_passed
    return PileResult(
        cube_count=len(scene.cubes),
        simulated_duration=PILE_DURATION,
        timestep=TIMESTEP,
        peak_contact_count=peak_contacts,
        final_contact_count=final_contacts,
        maximum_final_linear_speed=max_linear,
        maximum_final_angular_speed=max_angular,
        minimum_cube_bottom=minimum_bottom,
        platform_top=platform_top,
        penetration_tolerance=PLATFORM_PENETRATION_TOLERANCE,
        platform_penetration_passed=penetration_passed,
        cube_platform_passed=cube_platform_passed,
        cubes_fell=cubes_fell,
        cubes_within_platform=cubes_within_platform,
        finite=finite,
        settled=max_linear <= FINAL_LINEAR_SPEED_LIMIT,
        simulation_wall_seconds=wall_seconds,
    )


def _probe_cube(
    system: chrono.ChSystemNSC,
    material: chrono.ChContactMaterialNSC,
    name: str,
    position: Vector3,
) -> chrono.ChBody:
    spec = VisualObject(
        name,
        "probe",
        "box",
        position,
        CUBE_DIMENSIONS,
        CUBE_COLORS[0],
    )
    body = _contact_box(spec, material, fixed=False, mass=CUBE_MASS)
    system.AddBody(body)
    return body


def run_cube_cube_probe() -> ProbeResult:
    """Collide two dynamic cubes in zero gravity to identify cube/cube contact."""

    system = _new_system()
    system.SetGravitationalAcceleration(chrono.ChVector3d(0.0, 0.0, 0.0))
    material = _material(MATERIAL_SPECS["cube"])
    first = _probe_cube(system, material, "probe.cube_a", (-0.40, 1.0, 0.0))
    second = _probe_cube(system, material, "probe.cube_b", (0.40, 1.0, 0.0))
    first.SetLinVel(chrono.ChVector3d(1.0, 0.0, 0.0))
    second.SetLinVel(chrono.ChVector3d(-1.0, 0.0, 0.0))
    peak = 0
    wall_start = time.perf_counter()
    for _ in range(round(0.60 / TIMESTEP)):
        system.DoStepDynamics(TIMESTEP)
        peak = max(peak, system.GetNumContacts())
    wall_seconds = time.perf_counter() - wall_start
    finite = _finite_body(first) and _finite_body(second)
    position = _vector_tuple(first.GetPos())
    return ProbeResult(
        "cube/cube",
        peak > 0 and finite,
        peak,
        system.GetNumContacts(),
        position,
        _speed(first.GetLinVel()),
        finite,
        wall_seconds,
    )


def _build_fixed_probe_boxes(
    system: chrono.ChSystemNSC,
    names: tuple[str, ...],
    material_spec: ContactMaterialSpec,
) -> dict[str, chrono.ChBody]:
    objects = {item.name: item for item in _scene_objects()}
    material = _material(material_spec)
    bodies: dict[str, chrono.ChBody] = {}
    for name in names:
        body = _contact_box(objects[name], material, fixed=True)
        system.AddBody(body)
        bodies[name] = body
    return bodies


def run_cube_container_probe() -> ProbeResult:
    """Drop one cube into the actual fixed receiving container geometry."""

    system = _new_system()
    bodies = _build_fixed_probe_boxes(
        system, CONTAINER_NAMES, MATERIAL_SPECS["environment"]
    )
    cube = _probe_cube(
        system,
        _material(MATERIAL_SPECS["cube"]),
        "probe.container_cube",
        (2.20, 1.80, -3.05),
    )
    peak = 0
    wall_start = time.perf_counter()
    for _ in range(round(1.50 / TIMESTEP)):
        system.DoStepDynamics(TIMESTEP)
        peak = max(peak, system.GetNumContacts())
    wall_seconds = time.perf_counter() - wall_start
    finite = _finite_body(cube)
    position = _vector_tuple(cube.GetPos())
    floor = next(item for item in _scene_objects() if item.name == "container.floor")
    floor_top = floor.position[1] + floor.dimensions[1] / 2.0
    supported = position[1] - CUBE_DIMENSIONS[1] / 2.0 >= floor_top - PLATFORM_PENETRATION_TOLERANCE
    inside_walls = 0.96 <= position[0] <= 3.44 and -4.07 <= position[2] <= -2.03
    speed = _speed(cube.GetLinVel())
    return ProbeResult(
        "cube/container",
        peak > 0 and finite and supported and inside_walls and speed <= FINAL_LINEAR_SPEED_LIMIT,
        peak,
        system.GetNumContacts(),
        position,
        speed,
        finite,
        wall_seconds,
    )


def run_cube_bucket_probe() -> ProbeResult:
    """Drop one cube onto the actual fixed bucket collision geometry."""

    system = _new_system()
    _build_fixed_probe_boxes(system, BUCKET_NAMES, MATERIAL_SPECS["bucket"])
    cube = _probe_cube(
        system,
        _material(MATERIAL_SPECS["cube"]),
        "probe.bucket_cube",
        (2.05, 1.25, 0.0),
    )
    peak = 0
    wall_start = time.perf_counter()
    for _ in range(round(0.60 / TIMESTEP)):
        system.DoStepDynamics(TIMESTEP)
        peak = max(peak, system.GetNumContacts())
    wall_seconds = time.perf_counter() - wall_start
    finite = _finite_body(cube)
    position = _vector_tuple(cube.GetPos())
    did_not_pass_through = position[1] > 0.20
    return ProbeResult(
        "cube/bucket",
        peak > 0 and finite and did_not_pass_through,
        peak,
        system.GetNumContacts(),
        position,
        _speed(cube.GetLinVel()),
        finite,
        wall_seconds,
    )


def run_contact_validation_suite() -> ContactValidationResult:
    """Run the pile and three pair-specific validation probes."""

    scene = build_contact_scene()
    pile = run_pile_scenario(scene)
    result = ContactValidationResult(
        pile=pile,
        cube_cube=run_cube_cube_probe(),
        cube_container=run_cube_container_probe(),
        cube_bucket=run_cube_bucket_probe(),
    )
    failures: list[str] = []
    if pile.cube_count != CUBE_COUNT:
        failures.append("pile cube count")
    if not pile.finite:
        failures.append("finite pile state")
    if pile.peak_contact_count <= 0:
        failures.append("positive contact count")
    if not pile.platform_penetration_passed:
        failures.append("platform penetration")
    if not pile.cubes_within_platform:
        failures.append("platform bounds")
    if not pile.cubes_fell:
        failures.append("gravity fall")
    if not pile.settled:
        failures.append("final linear speed")
    for probe in (result.cube_cube, result.cube_container, result.cube_bucket):
        if not probe.passed:
            failures.append(probe.name)
    if failures:
        raise ContactValidationError("Failed contact criteria: " + ", ".join(failures))
    return result
