"""Fast, display-free tests for the Milestone 1 scaffold."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import pychrono

import chrono_ai_excavator
from scripts.check_environment import (
    REQUIRED_CLASSES,
    detect_visualization_capabilities,
    run_gravity_smoke_test,
)
from scripts.summarize_project_tracking import (
    EVENT_FIELDS,
    SOFTWARE_FIELDS,
    SchemaError,
    read_csv,
    summarize,
)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    """Write a temporary tracking fixture."""

    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class ScaffoldTests(unittest.TestCase):
    """Exercise package, environment, and tracking behavior."""

    def test_package_import_and_version(self) -> None:
        self.assertEqual(chrono_ai_excavator.__version__, "0.1.0")

    def test_required_project_chrono_classes(self) -> None:
        self.assertTrue(
            all(hasattr(pychrono, class_name) for class_name in REQUIRED_CLASSES)
        )

    def test_gravity_smoke_test_moves_body_downward(self) -> None:
        initial_y, final_y = run_gravity_smoke_test(pychrono)
        self.assertLess(final_y, initial_y)

    def test_visualization_capability_detection_allows_missing_vsg(self) -> None:
        capabilities = detect_visualization_capabilities()
        self.assertTrue(capabilities.irrlicht)
        self.assertTrue(capabilities.postprocess)
        self.assertIsInstance(capabilities.vsg, bool)

    def test_tracking_schema_rejects_wrong_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.csv"
            invalid.write_text("wrong,header\n", encoding="utf-8")
            with self.assertRaises(SchemaError):
                read_csv(invalid, EVENT_FIELDS)

    def test_tracking_summary_calculations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            events_path = Path(directory) / "events.csv"
            software_path = Path(directory) / "software.csv"
            base = {field: "" for field in EVENT_FIELDS}
            rows = [
                {
                    **base,
            "event_id": "A",
                    "activity_category": "codex_development",
                    "actor": "codex",
                    "started_at": "2026-08-04T10:00:00+03:00",
                    "ended_at": "2026-08-04T10:10:00+03:00",
                    "human_active_minutes": "5",
                    "ai_wall_seconds": "600",
                    "iteration_type": "initial",
                    "ai_result_status": "accepted",
                    "estimate_quality": "measured",
                },
                {
                    **base,
                    "event_id": "B",
                    "activity_category": "verification",
                    "actor": "system",
                    "started_at": "2026-08-04T10:05:00+03:00",
                    "ended_at": "2026-08-04T10:15:00+03:00",
                    "compute_wall_seconds": "120",
                    "iteration_type": "correction",
                    "ai_result_status": "accepted_with_corrections",
                    "estimate_quality": "derived_from_timestamps",
                },
            ]
            software_base = {field: "" for field in SOFTWARE_FIELDS}
            software = [
                {
                    **software_base,
                    "software_name": "Tool",
                    "cost_amount": "2.5",
                    "cost_currency": "USD",
                }
            ]
            write_csv(events_path, EVENT_FIELDS, rows)
            write_csv(software_path, SOFTWARE_FIELDS, software)

            result = summarize(
                read_csv(events_path, EVENT_FIELDS),
                read_csv(software_path, SOFTWARE_FIELDS),
            )

        self.assertEqual(result["calendar_seconds"], 900)
        self.assertEqual(result["human_minutes"], 5)
        self.assertEqual(result["ai_seconds"], 600)
        self.assertEqual(result["compute_seconds"], 120)
        self.assertEqual(result["costs"], {"USD": 2.5})
        self.assertEqual(result["iterations"]["initial"], 1)
        self.assertEqual(result["iterations"]["correction"], 1)
        self.assertEqual(result["results"]["accepted"], 1)
        self.assertEqual(result["results"]["accepted_with_corrections"], 1)


if __name__ == "__main__":
    unittest.main()
