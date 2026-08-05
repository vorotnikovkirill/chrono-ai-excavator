# Project Effort, Tooling, and Cost Ledger

This reproducible ledger keeps engineering effort, machine execution, and cost evidence separate. Add an event when work begins or ends at a meaningful boundary. Use ISO 8601 timestamps with timezone offsets and preserve reproducible evidence whenever possible.

## Event schema

`events.csv` uses these fields:

- `event_id`: stable unique identifier.
- `milestone`: project milestone label.
- `started_at`, `ended_at`: ISO 8601 timestamps with timezone offsets.
- `activity_category`: one controlled activity value.
- `actor`: one controlled actor value.
- `tool`, `description`: execution context and concise result.
- `human_active_minutes`: active project-owner effort only.
- `ai_wall_seconds`: Codex or other AI execution wall time only.
- `compute_wall_seconds`: computation or simulation wall time only.
- `iteration_type`: initial, correction, repeat, rework, or not applicable.
- `ai_result_status`: accepted, accepted with corrections, rejected, pending review, or not applicable.
- `cost_amount`, `cost_currency`: attributable project expense; leave the amount empty when it is unavailable or not separately measurable.
- `evidence`: reproducible command output, prompt, or artifact reference.
- `estimate_quality`: measured, derived from timestamps, or approximate estimate.
- `notes`: qualifications, ranges, and unknowns.

Activity categories are `chatgpt_discussion`, `human_task_definition`, `human_execution`, `human_review`, `codex_development`, `verification`, `computation`, `simulation`, `debugging`, `rework`, `documentation`, and `project_management`.

Actors are `project_owner`, `chatgpt`, `codex`, `project_chrono`, `system`, and `mixed`.

AI result statuses are `accepted`, `accepted_with_corrections`, `rejected`, `pending_review`, and `not_applicable`.

Estimate qualities are `measured`, `derived_from_timestamps`, and `approximate_estimate`. Iteration types are `initial`, `correction`, `repeat`, `rework`, and `not_applicable`.

ChatGPT discussion and engineering decisions, project-owner task definition/execution/review/verification, Codex wall time, computation and simulation wall time, debugging, corrections, repeated runs, rework, documentation, tool versions/licenses/costs, infrastructure expenses, and AI-result disposition must remain identifiable. Overlapping human, AI, and computation periods remain separate and must never be added as though they were sequential labor. Historical estimates must state their uncertainty; unknown historical generation or review time stays blank.

`software_inventory.csv` records verified or explicitly qualified versions, roles, licenses, cost bases, and evidence. A zero incremental charge must not be presented as proof that a subscription product is free.
