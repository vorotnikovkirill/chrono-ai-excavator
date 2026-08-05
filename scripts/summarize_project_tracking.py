#!/usr/bin/env python3
"""Validate and summarize the standard-library project ledger."""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


EVENT_FIELDS = [
    "event_id",
    "milestone",
    "started_at",
    "ended_at",
    "activity_category",
    "actor",
    "tool",
    "description",
    "human_active_minutes",
    "ai_wall_seconds",
    "compute_wall_seconds",
    "iteration_type",
    "ai_result_status",
    "cost_amount",
    "cost_currency",
    "evidence",
    "estimate_quality",
    "notes",
]

SOFTWARE_FIELDS = [
    "software_name",
    "version",
    "role",
    "license",
    "cost_amount",
    "cost_currency",
    "cost_basis",
    "verification_source",
    "notes",
]

CONTROLLED_VALUES = {
    "activity_category": {
        "chatgpt_discussion",
        "human_task_definition",
        "human_execution",
        "human_review",
        "codex_development",
        "verification",
        "computation",
        "simulation",
        "debugging",
        "rework",
        "documentation",
        "project_management",
    },
    "actor": {
        "project_owner",
        "chatgpt",
        "codex",
        "project_chrono",
        "system",
        "mixed",
    },
    "iteration_type": {
        "initial",
        "correction",
        "repeat",
        "rework",
        "not_applicable",
    },
    "ai_result_status": {
        "accepted",
        "accepted_with_corrections",
        "rejected",
        "pending_review",
        "not_applicable",
    },
    "estimate_quality": {
        "measured",
        "derived_from_timestamps",
        "approximate_estimate",
    },
}


class SchemaError(ValueError):
    """Raised when a tracking CSV does not match its required schema."""


def read_csv(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    """Read a CSV after validating its exact ordered header."""

    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != expected_fields:
            raise SchemaError(
                f"Invalid schema in {path}: expected {expected_fields}, "
                f"found {reader.fieldnames}"
            )
        return list(reader)


def number(value: str, field_name: str) -> float:
    """Convert an optional numeric field safely."""

    if not value.strip():
        return 0.0
    try:
        return float(value)
    except ValueError as exc:
        raise SchemaError(f"Invalid numeric value for {field_name}: {value!r}") from exc


def parse_intervals(events: list[dict[str, str]]) -> list[tuple[datetime, datetime]]:
    """Parse complete event intervals and reject invalid timestamps."""

    intervals = []
    for event in events:
        try:
            start = datetime.fromisoformat(event["started_at"])
            end = datetime.fromisoformat(event["ended_at"])
        except ValueError as exc:
            raise SchemaError(f"Invalid timestamp in {event['event_id']}") from exc
        if start.tzinfo is None or end.tzinfo is None:
            raise SchemaError(f"Timestamp lacks timezone offset in {event['event_id']}")
        if end < start:
            raise SchemaError(f"Event ends before it starts: {event['event_id']}")
        intervals.append((start, end))
    return intervals


def validate_events(events: list[dict[str, str]]) -> None:
    """Validate identifiers and controlled values in event rows."""

    identifiers: set[str] = set()
    for event in events:
        event_id = event["event_id"].strip()
        if not event_id:
            raise SchemaError("Event identifier is empty")
        if event_id in identifiers:
            raise SchemaError(f"Duplicate event identifier: {event_id}")
        identifiers.add(event_id)
        for field_name, allowed in CONTROLLED_VALUES.items():
            value = event[field_name].strip()
            if value not in allowed:
                raise SchemaError(
                    f"Invalid {field_name} in {event_id}: {value!r}"
                )


def union_seconds(intervals: list[tuple[datetime, datetime]]) -> float:
    """Return the duration of interval union so overlaps are not double-counted."""

    if not intervals:
        return 0.0
    ordered = sorted(intervals)
    current_start, current_end = ordered[0]
    total = 0.0
    for start, end in ordered[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            total += (current_end - current_start).total_seconds()
            current_start, current_end = start, end
    return total + (current_end - current_start).total_seconds()


def summarize(
    events: list[dict[str, str]], software: list[dict[str, str]]
) -> dict[str, object]:
    """Build independent duration, iteration, result, and cost totals."""

    validate_events(events)
    intervals = parse_intervals(events)
    quality = Counter(event["estimate_quality"] for event in events)
    iterations = Counter(event["iteration_type"] for event in events)
    results = Counter(event["ai_result_status"] for event in events)

    costs: dict[str, float] = defaultdict(float)
    for row in [*events, *software]:
        amount = number(row["cost_amount"], "cost_amount")
        if amount:
            currency = row["cost_currency"].strip()
            if not currency:
                raise SchemaError("A nonzero cost is missing its currency")
            costs[currency] += amount

    return {
        "calendar_seconds": union_seconds(intervals),
        "human_minutes": sum(number(row["human_active_minutes"], "human_active_minutes") for row in events),
        "ai_seconds": sum(number(row["ai_wall_seconds"], "ai_wall_seconds") for row in events),
        "compute_seconds": sum(number(row["compute_wall_seconds"], "compute_wall_seconds") for row in events),
        "costs": dict(sorted(costs.items())),
        "iterations": iterations,
        "results": results,
        "quality": quality,
    }


def format_duration(seconds: float) -> str:
    """Format seconds as a compact reproducible duration."""

    whole = round(seconds)
    hours, remainder = divmod(whole, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:d}h {minutes:02d}m {secs:02d}s"


def print_summary(summary: dict[str, object]) -> None:
    """Print the required project metrics."""

    iterations: Counter[str] = summary["iterations"]  # type: ignore[assignment]
    results: Counter[str] = summary["results"]  # type: ignore[assignment]
    costs: dict[str, float] = summary["costs"]  # type: ignore[assignment]
    quality: Counter[str] = summary["quality"]  # type: ignore[assignment]

    print("Project tracking summary")
    print(f"Calendar duration (overlap-safe): {format_duration(float(summary['calendar_seconds']))}")
    print(f"Human active effort: {float(summary['human_minutes']):.1f} minutes")
    print(f"Codex/AI wall time: {format_duration(float(summary['ai_seconds']))}")
    print(f"Simulation/computation wall time: {format_duration(float(summary['compute_seconds']))}")
    if costs:
        print("Documented attributable cost: " + ", ".join(f"{value:.2f} {currency}" for currency, value in costs.items()))
    else:
        print("Documented attributable cost: none measurable")
    print(f"Initial iterations: {iterations['initial']}")
    print(f"Corrections: {iterations['correction']}")
    print(f"Repeated runs: {iterations['repeat']}")
    print(f"Rework events: {iterations['rework']}")
    print(f"AI results accepted: {results['accepted']}")
    print(f"AI results accepted with corrections: {results['accepted_with_corrections']}")
    print(f"AI results rejected: {results['rejected']}")
    print(f"AI results pending review: {results['pending_review']}")
    print(
        "Estimate quality: "
        f"{quality['measured']} measured, "
        f"{quality['derived_from_timestamps']} timestamp-derived, "
        f"{quality['approximate_estimate']} approximate"
    )
    print("Human, AI, and compute totals are independent and must not be added together.")


def main(argv: list[str] | None = None) -> int:
    """Validate input files, print a summary, and return an exit status."""

    args = argv if argv is not None else sys.argv[1:]
    root = Path(__file__).resolve().parents[1]
    events_path = Path(args[0]) if len(args) >= 1 else root / "project_tracking/events.csv"
    software_path = Path(args[1]) if len(args) >= 2 else root / "project_tracking/software_inventory.csv"
    try:
        events = read_csv(events_path, EVENT_FIELDS)
        software = read_csv(software_path, SOFTWARE_FIELDS)
        print_summary(summarize(events, software))
    except (OSError, SchemaError) as exc:
        print(f"Tracking summary: FAIL ({exc})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
