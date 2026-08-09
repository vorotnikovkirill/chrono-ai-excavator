"""Build and control the Milestone 4 torque-actuated excavator scene."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

import pychrono as chrono

from chrono_ai_excavator.mechanical_scene import (
    ARM_HINGE_AXIS,
    JOINT_NAMES,
    PRIMARY_BODY_NAMES,
    VERTICAL_AXIS,
    JointSpec,
    MechanicalScene,
    _joint_frame,
    build_mechanical_scene,
)


Vector3 = tuple[float, float, float]
TRAJECTORY_DURATION = 1.0
CONTROL_TIMESTEP = 0.002
SCENARIO_DURATION = 3.0


@dataclass(frozen=True)
class ControllerConfig:
    """Toy-model PD gains and bounded torque in SI units."""

    joint_name: str
    parent: str
    child: str
    axis: Vector3
    kp: float  # N*m/rad
    kd: float  # N*m*s/rad
    hold_kp: float  # N*m/rad
    hold_kd: float  # N*m*s/rad
    tau_max: float  # N*m
    target_delta: float  # rad
    trajectory_duration: float  # s


@dataclass(frozen=True)
class JointControlResult:
    """Deterministic result metadata for one controlled motor."""

    joint_name: str
    initial_angle: float
    target_angle: float
    final_angle: float
    final_error: float
    peak_abs_torque: float
    tau_max: float
    max_hold_deviation: float
    finite: bool


@dataclass(frozen=True)
class ControlValidationResult:
    """Independent and combined control results plus measured loop wall time."""

    independent: tuple[JointControlResult, ...]
    combined: tuple[JointControlResult, ...]
    simulation_wall_seconds: float


@dataclass
class ControlledScene:
    """Actuated system, exact motor references, and controller state."""

    system: chrono.ChSystemNSC
    mechanical: MechanicalScene
    motors: Mapping[str, chrono.ChLinkMotorRotationTorque]
    torque_functions: Mapping[str, chrono.ChFunctionSetpoint]
    controllers: Mapping[str, ControllerConfig]
    last_torque_commands: dict[str, float]

    @property
    def bodies(self) -> Mapping[str, chrono.ChBody]:
        return self.mechanical.bodies

    @property
    def environment_bodies(self) -> Mapping[str, chrono.ChBody]:
        return self.mechanical.environment_bodies

    @property
    def cube_count(self) -> int:
        return self.mechanical.cube_count


class ControlValidationError(ValueError):
    """Raised when the bounded Milestone 4 control contract is violated."""


def _controller_configs() -> tuple[ControllerConfig, ...]:
    """Return deterministic demonstrator placeholders, not calibrated gains."""

    degrees = math.radians
    return (
        ControllerConfig("J0_SLEW", "BASE", "UPPER", VERTICAL_AXIS, 1500.0, 2500.0, 1500.0, 2500.0, 800.0, degrees(12.0), TRAJECTORY_DURATION),
        ControllerConfig("J1_BOOM", "UPPER", "BOOM", ARM_HINGE_AXIS, 2000.0, 1200.0, 6500.0, 2800.0, 800.0, degrees(8.0), TRAJECTORY_DURATION),
        ControllerConfig("J2_STICK", "BOOM", "STICK", ARM_HINGE_AXIS, 1500.0, 700.0, 6000.0, 2200.0, 600.0, degrees(-8.0), TRAJECTORY_DURATION),
        ControllerConfig("J3_BUCKET", "STICK", "BUCKET", ARM_HINGE_AXIS, 800.0, 200.0, 1600.0, 500.0, 300.0, degrees(10.0), TRAJECTORY_DURATION),
    )


def smooth_target(time_value: float, delta: float, duration: float = TRAJECTORY_DURATION) -> tuple[float, float]:
    """Return cubic target angle and analytic angular velocity."""

    if duration <= 0:
        raise ValueError("Trajectory duration must be positive")
    if time_value <= 0:
        return 0.0, 0.0
    if time_value >= duration:
        return delta, 0.0
    u = time_value / duration
    position = delta * (3.0 * u * u - 2.0 * u * u * u)
    velocity = delta * (6.0 * u - 6.0 * u * u) / duration
    return position, velocity


def bounded_pd_torque(config: ControllerConfig, target_angle: float, angle: float, target_rate: float, rate: float, *, holding: bool = False) -> float:
    """Return saturated PD torque in N*m."""

    kp = config.hold_kp if holding else config.kp
    kd = config.hold_kd if holding else config.kd
    raw = kp * (target_angle - angle) + kd * (target_rate - rate)
    return max(-config.tau_max, min(config.tau_max, raw))


def build_controlled_scene() -> ControlledScene:
    """Replace reference revolutes with exactly four torque-motor constraints."""

    mechanical = build_mechanical_scene()
    for joint in mechanical.joints.values():
        mechanical.system.RemoveLink(joint)

    configs = _controller_configs()
    config_map = {config.joint_name: config for config in configs}
    spec_map: dict[str, JointSpec] = {spec.name: spec for spec in mechanical.joint_specs}
    motors: dict[str, chrono.ChLinkMotorRotationTorque] = {}
    functions: dict[str, chrono.ChFunctionSetpoint] = {}
    for name in JOINT_NAMES:
        spec = spec_map[name]
        motor = chrono.ChLinkMotorRotationTorque()
        motor.SetName(name)
        motor.Initialize(mechanical.bodies[spec.parent], mechanical.bodies[spec.child], _joint_frame(spec))
        torque_function = chrono.ChFunctionSetpoint()
        motor.SetTorqueFunction(torque_function)
        mechanical.system.AddLink(motor)
        motors[name] = motor
        functions[name] = torque_function

    return ControlledScene(
        system=mechanical.system,
        mechanical=mechanical,
        motors=MappingProxyType(motors),
        torque_functions=MappingProxyType(functions),
        controllers=MappingProxyType(config_map),
        last_torque_commands={name: 0.0 for name in JOINT_NAMES},
    )


def validate_controlled_scene(scene: ControlledScene) -> tuple[str, ...]:
    """Return topology and controller failures without running dynamics."""

    errors: list[str] = []
    if tuple(scene.bodies) != PRIMARY_BODY_NAMES or len(scene.bodies) != 5:
        errors.append("Controlled scene must retain exactly five primary bodies")
    if tuple(scene.motors) != JOINT_NAMES or len(scene.system.GetLinks()) != 4:
        errors.append("Controlled scene must contain exactly four named motor links")
    specs = {spec.name: spec for spec in scene.mechanical.joint_specs}
    for name in JOINT_NAMES:
        motor = scene.motors.get(name)
        config = scene.controllers.get(name)
        spec = specs[name]
        if motor is None or type(motor) is not chrono.ChLinkMotorRotationTorque:
            errors.append(f"{name} must be a torque motor")
            continue
        if motor.GetBody1() != scene.bodies[spec.parent] or motor.GetBody2() != scene.bodies[spec.child]:
            errors.append(f"{name} has incorrect connectivity")
        axis = motor.GetFrame1Abs().GetRot().GetAxisZ()
        dot = axis.x * spec.axis[0] + axis.y * spec.axis[1] + axis.z * spec.axis[2]
        if not math.isclose(abs(dot), 1.0, abs_tol=1e-9):
            errors.append(f"{name} has incorrect motor axis")
        if config is None or config.kp <= 0 or config.kd < 0 or config.hold_kp <= 0 or config.hold_kd < 0 or config.tau_max <= 0:
            errors.append(f"{name} has invalid controller parameters")
    if tuple(link.GetName() for link in scene.system.GetLinks()) != JOINT_NAMES:
        errors.append("Controlled scene contains a duplicate or unexpected joint constraint")
    if scene.cube_count != 30 or any(not body.IsFixed() for body in scene.environment_bodies.values()):
        errors.append("Controlled scene must retain 30 fixed cubes and fixed environment")
    if any(body.IsCollisionEnabled() for body in (*scene.bodies.values(), *scene.environment_bodies.values())):
        errors.append("Contacts and collision must remain disabled")
    return tuple(errors)


def assert_valid_controlled_scene(scene: ControlledScene) -> None:
    errors = validate_controlled_scene(scene)
    if errors:
        raise ControlValidationError("; ".join(errors))


def advance_controlled_step(scene: ControlledScene, active_targets: Mapping[str, float], timestep: float = CONTROL_TIMESTEP) -> None:
    """Update all torque setpoints once and advance one fixed step."""

    current_time = scene.system.GetChTime()
    for name in JOINT_NAMES:
        config = scene.controllers[name]
        delta = active_targets.get(name, 0.0)
        target_angle, target_rate = smooth_target(current_time, delta, config.trajectory_duration)
        motor = scene.motors[name]
        torque = bounded_pd_torque(
            config,
            target_angle,
            motor.GetMotorAngle(),
            target_rate,
            motor.GetMotorAngleDt(),
            holding=name not in active_targets,
        )
        scene.torque_functions[name].SetSetpoint(torque, current_time)
        scene.last_torque_commands[name] = torque
    scene.system.DoStepDynamics(timestep)


def _run_scenario(active_targets: Mapping[str, float]) -> tuple[tuple[JointControlResult, ...], float]:
    scene = build_controlled_scene()
    assert_valid_controlled_scene(scene)
    initial = {name: scene.motors[name].GetMotorAngle() for name in JOINT_NAMES}
    peaks = {name: 0.0 for name in JOINT_NAMES}
    max_hold = {name: 0.0 for name in JOINT_NAMES}
    finite = True
    steps = round(SCENARIO_DURATION / CONTROL_TIMESTEP)
    started = time.perf_counter()
    for _ in range(steps):
        advance_controlled_step(scene, active_targets)
        for name in JOINT_NAMES:
            motor = scene.motors[name]
            angle = motor.GetMotorAngle()
            rate = motor.GetMotorAngleDt()
            torque = scene.last_torque_commands[name]
            peaks[name] = max(peaks[name], abs(torque))
            if name not in active_targets:
                max_hold[name] = max(max_hold[name], abs(angle))
            finite = finite and all(math.isfinite(value) for value in (angle, rate, torque))
    elapsed = time.perf_counter() - started

    results = []
    for name in JOINT_NAMES:
        target = active_targets.get(name, 0.0)
        final = scene.motors[name].GetMotorAngle()
        results.append(JointControlResult(name, initial[name], target, final, target - final, peaks[name], scene.controllers[name].tau_max, max_hold[name], finite))
    return tuple(results), elapsed


def _assert_scenario(results: tuple[JointControlResult, ...], active: frozenset[str]) -> None:
    angle_tolerance = math.radians(1.5)
    hold_tolerance = math.radians(0.5)
    for result in results:
        if not result.finite:
            raise ControlValidationError(f"{result.joint_name} produced a non-finite state")
        if result.peak_abs_torque > result.tau_max + 1e-9:
            raise ControlValidationError(f"{result.joint_name} exceeded its torque limit")
        if result.joint_name in active:
            if result.final_angle * result.target_angle <= 0:
                raise ControlValidationError(f"{result.joint_name} moved in the wrong direction")
            if abs(result.final_error) > angle_tolerance or abs(result.final_error) >= abs(result.target_angle - result.initial_angle):
                raise ControlValidationError(f"{result.joint_name} did not reach its target tolerance")
        elif result.max_hold_deviation > hold_tolerance:
            raise ControlValidationError(f"{result.joint_name} exceeded hold tolerance")


def run_control_validation() -> ControlValidationResult:
    """Run four independent scenarios and one combined control smoke test."""

    independent: list[JointControlResult] = []
    wall_seconds = 0.0
    configs = {config.joint_name: config for config in _controller_configs()}
    for name in JOINT_NAMES:
        results, elapsed = _run_scenario({name: configs[name].target_delta})
        _assert_scenario(results, frozenset({name}))
        active_result = next(result for result in results if result.joint_name == name)
        scenario_hold = max(
            result.max_hold_deviation
            for result in results
            if result.joint_name != name
        )
        independent.append(replace(active_result, max_hold_deviation=scenario_hold))
        wall_seconds += elapsed
    targets = {name: configs[name].target_delta for name in JOINT_NAMES}
    combined, elapsed = _run_scenario(targets)
    _assert_scenario(combined, frozenset(JOINT_NAMES))
    wall_seconds += elapsed
    return ControlValidationResult(tuple(independent), combined, wall_seconds)
