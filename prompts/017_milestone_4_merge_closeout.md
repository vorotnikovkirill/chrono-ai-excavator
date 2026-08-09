# Milestone 4 — Merge Closeout

## Objective

Fully close Milestone 4 after the accepted bounded joint-actuation and control implementation was successfully fast-forward merged into `main` and published.

This task is strictly limited to:

* recording the Milestone 4 closeout commit/push;
* recording the fast-forward merge/push to `main`;
* updating README to mark Milestone 4 complete;
* updating the living technical report to mark Milestone 4 complete;
* preserving this Codex task;
* running the established display-free verification.

Do not start contacts or any next milestone.

Do not change the accepted control implementation.

If anything unexpected appears outside this task, STOP and report it.

---

# Canonical project rule

Proceed strictly according to the agreed project plan.

No deviation, cleanup, refactoring, improvement, side task, or future-milestone work is allowed without explicit project-owner approval.

Project priority:

> **Fast, clear, and visually strong. No unnecessary depth.**

---

# Repository state

Repository:

`/Users/kirillvorotnikov/Projects/chrono-ai-excavator`

Required branch:

`main`

Expected HEAD:

`1fd4218e948797f53c27398efe735ad6704d1e50`

Expected origin:

`https://github.com/vorotnikovkirill/chrono-ai-excavator.git`

Local and remote `main` were verified at the same commit.

Do not:

* switch branches;
* commit;
* push;
* delete branches;
* modify remotes.

---

# Accepted Milestone 4 result

Milestone 4 implemented bounded torque-based actuation for:

* `J0_SLEW`
* `J1_BOOM`
* `J2_STICK`
* `J3_BUCKET`

Architecture:

* four `ChLinkMotorRotationTorque` links;
* no duplicate revolute constraints;
* bounded PD motion control;
* distinct holding gains;
* smooth deterministic one-second target trajectory;
* two-second settling period;
* zero gravity;
* fixed cubes;
* no contacts.

Final automated verification:

* controlled headless check: **PASS**
* combined four-joint smoke test: **PASS**
* 38/38 unittests: **PASS**
* compilation: **PASS**
* `git diff --check`: **PASS**

Final accepted independent results:

* `J0_SLEW`: target `+12.00°`, final `+12.71°`, error `−0.71°`, max hold deviation `0.09°`, peak torque `454.59 / 800 N·m`
* `J1_BOOM`: target `+8.00°`, final `+8.12°`, error `−0.12°`, max hold deviation `0.42°`, peak torque `183.00 / 800 N·m`
* `J2_STICK`: target `−8.00°`, final `−7.89°`, error `−0.11°`, max hold deviation `0.44°`, peak torque `82.01 / 600 N·m`
* `J3_BUCKET`: target `+10.00°`, final `+10.00°`, error approximately `0.00°`, max hold deviation `0.03°`, peak torque `8.31 / 300 N·m`

---

# Human visual result

Control motion was visually accepted.

A lighting regression was found and corrected by restoring lighting parity with the accepted Milestone 2/3 viewers.

Final lighting visual review:

* viewer exit status: `0`
* result: `accepted`
* project-owner verdict: `все хорошо`

The bucket moving below the platform remains an explicitly accepted limitation because contacts are outside Milestone 4 scope.

Do not add contacts in this task.

---

# Confirmed Git history

Accepted Milestone 4 implementation:

`9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`

Commit:

`feat: add bounded joint actuation control`

Feature-branch closeout:

`1fd4218e948797f53c27398efe735ad6704d1e50`

Commit:

`docs: close milestone 4`

---

# Confirmed feature closeout commit/push

Measured operation:

* started: `2026-08-09T22:54:49+03:00`
* ended: `2026-08-09T22:54:51+03:00`
* duration: `2 seconds`
* commit: `1fd4218e948797f53c27398efe735ad6704d1e50`
* push: PASS

Evidence:

`/tmp/chrono_ai_excavator_step_08h_commit_m4_closeout.txt`

---

# Confirmed merge to main

Measured operation:

* started: `2026-08-09T22:56:55+03:00`
* ended: `2026-08-09T22:56:58+03:00`
* duration: `3 seconds`

Result:

* fetch: PASS
* switch to main: PASS
* pull `--ff-only`: PASS
* fast-forward merge: PASS
* push `origin/main`: PASS
* local main:
  `1fd4218e948797f53c27398efe735ad6704d1e50`
* remote main:
  `1fd4218e948797f53c27398efe735ad6704d1e50`
* worktree:
  clean

Evidence:

`/tmp/chrono_ai_excavator_step_08i_merge_m4_to_main.txt`

---

# Required changes

## 1. Record feature closeout commit/push

Add exactly one event if absent:

* event_id: `M4-CLOSEOUT-COMMIT-PUSH-001`
* milestone: `M4`
* started_at: `2026-08-09T22:54:49+03:00`
* ended_at: `2026-08-09T22:54:51+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Committed and pushed the accepted Milestone 4 closeout documentation on the joint-actuation-control feature branch.`
* human_active_minutes: `0.03`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `/tmp/chrono_ai_excavator_step_08h_commit_m4_closeout.txt and Git commit 1fd4218e948797f53c27398efe735ad6704d1e50`
* estimate_quality: `measured`
* notes:
  `Network time is not simulation or computation time.`

---

## 2. Record merge into main

Add exactly one event if absent:

* event_id: `M4-MERGE-MAIN-001`
* milestone: `M4`
* started_at: `2026-08-09T22:56:55+03:00`
* ended_at: `2026-08-09T22:56:58+03:00`
* activity_category: `project_management`
* actor: `project_owner`
* tool: `Git`
* description:
  `Fast-forward merged the accepted Milestone 4 bounded joint-actuation and control implementation into main and pushed the synchronized main branch.`
* human_active_minutes: `0.05`
* iteration_type: `initial`
* ai_result_status: `not_applicable`
* evidence:
  `/tmp/chrono_ai_excavator_step_08i_merge_m4_to_main.txt and Git commit 1fd4218e948797f53c27398efe735ad6704d1e50`
* estimate_quality: `measured`
* notes:
  `Local and remote main were verified at the same commit. Merge and network time are not simulation or computation time.`

Preserve LF line endings.

Do not alter unrelated ledger records.

Do not invent missing historical timing.

---

# 3. Update README

Update `README.md` minimally.

Milestone 4 must now be marked:

* implemented;
* numerically verified;
* human visually accepted;
* committed;
* pushed;
* fast-forward merged into `main`;
* publicly available;
* **complete**.

Current implemented capabilities now include:

* accepted static visual scene;
* five-body articulated mechanical architecture;
* four functional joint axes;
* four torque-actuated controlled joints;
* bounded PD motion and hold control;
* deterministic target trajectories;
* zero-gravity control verification.

Future work remains:

* contacts;
* dynamic cubes;
* bucket/cube interaction;
* scoop/dump sequence;
* excavation state machine;
* telemetry/HUD;
* active-joint visualization;
* bucket camera;
* cabin camera;
* final video.

Do not add or define a new milestone in detail.

---

# 4. Update technical report

Update:

`docs/technical_report.md`

State explicitly:

> **Milestone 4 is complete.**

Record:

* four torque motors;
* bounded PD control;
* motion and hold gains;
* torque limits;
* one-second trajectory;
* two-second settling interval;
* independent joint results;
* combined-control PASS;
* 38/38 tests;
* human motion acceptance;
* PD/holding correction;
* lighting-parity correction;
* final lighting acceptance;
* accepted bucket-below-platform no-contact limitation;
* implementation commit `9102f846191c71ec29ccd8fa1c7a2dcb84ab889b`;
* feature closeout commit `1fd4218e948797f53c27398efe735ad6704d1e50`;
* final merged main commit `1fd4218e948797f53c27398efe735ad6704d1e50`;
* measured feature closeout interval;
* measured merge interval;
* synchronized local/remote `main`;
* updated project-tracking totals.

Retain separate reporting of:

* human effort;
* AI-assisted effort;
* simulation/computation wall time;
* cost;
* corrections/iterations.

Do not describe contacts or excavation behavior as implemented.

---

# 5. Preserve this task

Save this full specification as:

`prompts/017_milestone_4_merge_closeout.md`

Do not alter prompts 001 through 016.

---

# Verification

Run only:

```text
python scripts/show_mechanical_scene.py --headless-check
python scripts/show_controlled_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
python scripts/summarize_project_tracking.py
git diff --check
git status --short --branch
```

Verify only:

* current branch is `main`;
* committed base remains `1fd4218e948797f53c27398efe735ad6704d1e50`;
* origin unchanged;
* `controlled_scene.py` unchanged;
* `show_controlled_scene.py` unchanged;
* no package installation;
* no display window;
* no contacts or next-stage functionality.

If a prescribed check fails:

STOP and report it.

Do not repair or broaden scope automatically.

---

# Strict scope exclusions

Do not:

* modify control source;
* modify motors;
* modify gains;
* modify torque limits;
* modify trajectories;
* modify settling;
* modify mechanics;
* modify lighting;
* modify camera;
* add contacts;
* add collision response;
* make cubes dynamic;
* add scoop/dump logic;
* add state machine;
* add telemetry;
* add HUD;
* add active-joint visualization;
* add bucket camera;
* add cabin camera;
* add PDF;
* add presentation;
* add video;
* add dependencies;
* refactor;
* switch branches;
* delete branches;
* commit;
* push.

---

# Completion report

Report only:

1. files modified or created;
2. `M4-CLOSEOUT-COMMIT-PUSH-001` status;
3. `M4-MERGE-MAIN-001` status;
4. README Milestone 4 status;
5. technical-report Milestone 4 status;
6. preserved prompt path;
7. mechanical headless result;
8. controlled headless result;
9. final four independent control results;
10. combined control result;
11. unittest result;
12. compilation result;
13. tracking-summary result;
14. `git diff --check` result;
15. branch, HEAD, upstream, and worktree status;
16. updated tracking totals;
17. confirmation that Milestone 4 is documented as complete;
18. confirmation that controlled-scene source was unchanged;
19. confirmation that contacts/next-stage work were not started;
20. confirmation that no package installation, commit, push, branch deletion, remote modification, PDF, presentation, or video work occurred.

Do not commit or push.
