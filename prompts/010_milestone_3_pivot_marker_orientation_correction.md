# Milestone 3 — Decorative Pivot Marker Orientation Correction

## Objective

Correct only the visual orientation of the decorative boom, stick, and bucket pivot markers in the current Milestone 3 mechanical scene.

The actual Project Chrono revolute joints have been diagnosed and are mechanically correct.

Do not modify joint frames, joint axes, pivot positions, mechanical topology, masses, inertias, or any next-stage functionality.

---

# Confirmed diagnostic result

Installed Project Chrono convention:

`ChLinkLockRevolute` rotates about the joint frame local Z axis.

Scene vertical:

`(0, 1, 0)`

Actual joint axes:

- `J0_SLEW`: approximately `(0, 1, 0)` — correct
- `J1_BOOM`: `(0, 0, 1)` — correct
- `J2_STICK`: `(0, 0, 1)` — correct
- `J3_BUCKET`: `(0, 0, 1)` — correct

The boom/stick/bucket mechanism moves approximately in the scene X-Y plane, so the correct transverse joint axis is scene Z.

Confirmed pivot positions are also correct:

- `J1_BOOM`: `(-2.40, 1.82, 0.0)`
- `J2_STICK`: `(-0.05, 3.35, 0.0)`
- `J3_BUCKET`: `(1.66, 0.98, 0.0)`

Do not change any of these.

---

# Confirmed visual defect

Only the decorative pivot markers are incorrectly oriented:

- `excavator.boom_pivot`
- `excavator.elbow_pivot`
- `excavator.bucket_pivot`

Their current visual axes are approximately vertical:

`(0, -1, 0)`

They must visually align with the actual mechanical axes:

`(0, 0, 1)`

---

# Root cause

`ChVisualShapeCylinder` is intrinsically aligned with its local Z axis.

The current visual helper incorrectly assumes the cylinder is intrinsically Y-aligned.

The diagnosed minimal correction is:

- for `cylinder_axis == "z"`:
  use identity rotation;
- for `cylinder_axis == "y"`:
  rotate the intrinsic Z axis to scene Y using:

```python
chrono.QuatFromAngleX(-math.pi / 2.0)
```

Do not change the actual Project Chrono revolute-joint frames.

---

# Required correction

Modify only the minimum code required for correct cylinder visual-axis handling.

The correction must make the three pivot markers visually transverse while preserving the intended orientation of any legitimate Y-axis cylinders.

Do not redesign the helper.

Do not refactor unrelated geometry.

Do not alter the accepted static Milestone 2 scene.

If the helper is shared by other mechanical-scene cylinder visuals, ensure their previously intended axis argument continues to produce the requested world orientation.

Do not change dimensions, locations, colors, or proportions.

---

# Tests

Update tests only as needed to verify the corrected visual-axis convention.

Add or retain checks that confirm:

- `J1/J2/J3` actual mechanical axes remain `(0,0,1)` within tolerance;
- their decorative pivot markers are also intended to align with scene Z;
- any `cylinder_axis="y"` conversion still produces scene Y;
- no mechanical topology changed.

Do not weaken any existing test.

---

# Preserve this task

Save this specification as:

`prompts/010_milestone_3_pivot_marker_orientation_correction.md`

Do not alter prompts 001 through 009.

---

# Verification

Run only:

```bash
python scripts/show_mechanical_scene.py --headless-check
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
git diff --check
git status --short --branch
```

If any prescribed check fails, STOP and report it.

Do not broaden the repair.

Do not open Irrlicht automatically.

Human visual review will be performed separately after these checks pass.

---

# Strict exclusions

Do not:

- change `J0_SLEW`;
- change `J1_BOOM`;
- change `J2_STICK`;
- change `J3_BUCKET`;
- change joint frames;
- change pivot coordinates;
- change mechanical-body topology;
- change masses or inertias;
- add motors;
- add control;
- add contacts;
- add telemetry;
- add cameras;
- add HUD;
- add PDF;
- add presentation;
- add video;
- install packages;
- commit;
- push;
- switch branches;
- perform unrelated cleanup.

---

# Completion report

Report only:

1. exact code correction made;
2. files modified or created;
3. confirmation that actual joint frames and pivots were unchanged;
4. confirmation that J1/J2/J3 mechanical axes remain scene Z;
5. confirmation that decorative pivot markers now use scene Z;
6. mechanical headless-check result;
7. unittest result;
8. compilation result;
9. `git diff --check` result;
10. branch/worktree status;
11. confirmation that no next-stage functionality was added;
12. confirmation that no package installation, commit, push, branch switch, or remote modification occurred.

Do not commit or push.
