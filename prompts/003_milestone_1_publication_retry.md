# Milestone 1 — Acceptance Correction and Publication Preparation

## Objective

Correct the administrative and tracking records created by the failed publication attempt, complete the Milestone 1 acceptance update, and prepare the repository for its first commit and public GitHub publication.

This task is documentation, tracking, and verification work only.

Do not implement any new simulation, mechanics, visualization, or project features.

Do not install packages.

Do not commit, push, create a Git remote, create a GitHub repository, or perform any GitHub operation. Those actions will be performed separately after human review of this task.

---

## Project principles

The project priority is:

> **Fast, clear, and visually strong. No unnecessary depth.**

All repository content must remain in English.

The repository is intended to become public.

Do not add proprietary, confidential, trademark-dependent, or ambiguously licensed material.

---

## Confirmed Milestone 1 result

Milestone 1 was completed and explicitly accepted by the project owner.

The accepted milestone contains only:

* the public repository scaffold;
* English project documentation;
* the MIT License;
* the Python package foundation;
* the Project Chrono environment smoke test;
* display-free automated tests;
* the project time, tooling, iteration, and cost ledger;
* the preserved Milestone 1 Codex prompt.

Verified Milestone 1 findings:

* PyChrono imports successfully;
* `ChSystemNSC`, `ChBody`, and `ChLinkMotorRotationTorque` are available;
* Irrlicht is available;
* postprocess is available;
* VSG is unavailable and non-blocking;
* the gravity smoke test passes;
* six display-free tests previously passed through `unittest`;
* Python compilation passed;
* the tracking schema and summary passed;
* no package was installed;
* no large accidental file was found;
* no Cyrillic repository text was found;
* no Git remote existed;
* no commit or push had been performed.

`pytest` is not installed in the existing `chrono` Conda environment. This is not a Milestone 1 defect because package installation was prohibited and the tests are executable through the Python standard-library `unittest` runner.

---

## Failed publication attempt

A publication orchestration attempt ran from:

* started: `2026-08-04T09:22:08+03:00`
* ended: `2026-08-04T09:22:15+03:00`

The repository was not committed or published.

Two orchestration defects occurred.

### Defect 1 — Codex CLI invocation

The command placed the global approval argument after the `exec` subcommand.

Codex CLI rejected:

```text
--ask-for-approval
```

Codex did not begin task execution.

### Defect 2 — src-layout test invocation

The unittest command was executed without adding the repository `src` directory to `PYTHONPATH`.

This caused:

```text
ModuleNotFoundError: No module named 'chrono_ai_excavator'
```

This was an orchestration defect, not an implementation defect.

The following checks still passed during that attempt:

* environment check;
* tracking summary;
* Python compilation.

The failed attempt must remain visible in the project ledger. Do not delete or conceal it.

---

# Required changes

## 1. Correct the failed Codex event

Inspect:

```text
project_tracking/events.csv
```

Find:

```text
M1-CODEX-ACCEPTANCE-001
```

Update it to accurately state:

* Codex task execution did not start;
* Codex CLI rejected a misplaced global approval argument;
* `ai_wall_seconds` remains `0`;
* `iteration_type` is `correction`;
* `ai_result_status` is `rejected`;
* `estimate_quality` remains `measured`;
* evidence remains:

```text
/tmp/chrono_ai_excavator_step_02_publish_m1.txt
```

Do not treat this as successful AI-assisted development.

---

## 2. Correct the failed verification event

Find:

```text
M1-VERIFICATION-002
```

Update it to accurately state:

* environment verification passed;
* tracking-summary verification passed;
* Python compilation passed;
* unittest discovery failed because the src-layout package was not included in `PYTHONPATH`;
* this was an orchestration defect rather than a source-code defect;
* `iteration_type` remains `repeat`;
* `ai_result_status` is `accepted_with_corrections`;
* preserve its existing measured timestamps and compute duration;
* preserve its evidence path.

Do not change the recorded compute duration unless the existing record is demonstrably malformed.

---

## 3. Add the accepted Milestone 1 human-review event

Add this event if it does not already exist:

```text
event_id: M1-HUMAN-REVIEW-001
milestone: M1
started_at: 2026-08-04T09:14:35+03:00
ended_at: 2026-08-04T09:18:04+03:00
activity_category: human_review
actor: project_owner
tool: ChatGPT
description: Reviewed the Milestone 1 completion report and accepted the scaffold for publication.
human_active_minutes: 3.48
ai_wall_seconds:
compute_wall_seconds:
iteration_type: not_applicable
ai_result_status: accepted
cost_amount:
cost_currency:
evidence: Conversation timestamps and Milestone 1 completion report
estimate_quality: derived_from_timestamps
notes: Duration derived from the continuous review and confirmation interval.
```

Use the existing CSV schema and field order.

---

## 4. Add the failed-publication review event

Add this event if it does not already exist:

```text
event_id: M1-PUBLISH-FAILURE-REVIEW-001
milestone: M1
started_at: 2026-08-04T09:22:23+03:00
ended_at: 2026-08-04T09:25:44+03:00
activity_category: human_review
actor: project_owner
tool: Terminal and ChatGPT
description: Reviewed the failed publication report, identified the orchestration defects, and returned the workflow for correction.
human_active_minutes: 3.35
ai_wall_seconds:
compute_wall_seconds:
iteration_type: correction
ai_result_status: accepted_with_corrections
cost_amount:
cost_currency:
evidence: /tmp/chrono_ai_excavator_step_02_publish_m1.txt and conversation timestamps
estimate_quality: derived_from_timestamps
notes: Review interval covers report submission through the request for the corrected canonical Codex task.
```

---

## 5. Resolve original Milestone 1 pending statuses

Inspect all existing entries with:

```text
ai_result_status = pending_review
```

Change an entry to `accepted` only when all of the following are true:

* it directly belongs to the completed Milestone 1 scaffold;
* its output was included in the completion report;
* the project owner explicitly accepted the milestone;
* no later evidence shows that the specific result failed.

Do not change:

* unrelated pending entries;
* the failed Codex CLI event;
* historical preflight entries already marked `accepted_with_corrections`.

Do not rewrite historical durations, costs, or estimate-quality values.

---

## 6. Update project status documentation

Update only the necessary parts of:

```text
README.md
docs/technical_report.md
```

Record that:

* Milestone 1 is accepted and complete;
* the scaffold is ready for its initial public commit and publication;
* publication has not yet occurred;
* the failed publication attempt was an orchestration correction and did not invalidate the scaffold;
* Milestone 2 is the future first visual static scene;
* no Milestone 2 functionality has been implemented;
* no excavator geometry, joints, motors, contacts, control, telemetry, cameras, rendering, PDF, presentation, or video exists yet;
* PDF and presentation generation remain deferred until a visually meaningful milestone.

Keep the README concise.

Do not add an excessive incident report to the README. Detailed tracking information belongs in the ledger and technical report.

---

## 7. Preserve the corrected task

Save this complete task specification as:

```text
prompts/003_milestone_1_publication_retry.md
```

Do not overwrite:

```text
prompts/001_repository_scaffold.md
prompts/002_milestone_1_acceptance.md
```

The failed orchestration prompt and the corrected prompt are part of the reproducible AI-assisted development history.

---

# Verification

Run all verification inside the existing `chrono` Conda environment.

Do not install the package and do not install pytest.

Run:

```bash
python scripts/check_environment.py
python scripts/summarize_project_tracking.py
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
```

Also perform:

```bash
git diff --check
git status --short --branch
```

Inspect for:

* accidental large files;
* generated caches that should be ignored;
* accidental non-English public repository content;
* accidental Git remotes;
* accidental commits;
* accidental implementation outside the current milestone.

Do not invoke an Irrlicht display window.

---

# Explicit scope exclusions

Do not create or implement:

* excavator geometry;
* platform geometry;
* cube geometry;
* container geometry;
* rigid-body assembly;
* joints;
* motors;
* torque control;
* state-machine control;
* contact materials;
* telemetry;
* HUD overlays;
* active-joint visualization;
* main cinematic camera;
* bucket-mounted camera;
* cabin/operator camera;
* rendering;
* plots;
* image output;
* PDF;
* presentation;
* video;
* FFmpeg integration;
* CI;
* GitHub Actions;
* speculative future modules.

The future camera requirements remain documented roadmap items only.

---

# Completion report

At the end, report:

1. every file modified or created;
2. the exact correction made to `M1-CODEX-ACCEPTANCE-001`;
3. the exact correction made to `M1-VERIFICATION-002`;
4. the human-review events added;
5. pending statuses changed to accepted;
6. verification commands executed;
7. environment-check result;
8. tracking-summary result;
9. unittest result;
10. compilation result;
11. current Git status;
12. current remote status;
13. updated tracking totals;
14. assumptions or unresolved unknowns;
15. exact confirmation that no package installation, commit, push, remote creation, GitHub repository creation, or new simulation functionality was performed.
