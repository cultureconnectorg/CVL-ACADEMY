# CVLN Academy — Delivery Mode Funnel Matrix

```
MODE = DOCUMENTATION_ONLY. Derived entirely from
docs/ACADEMY_DELIVERY_MODE_AUDIT.md (evidence) and
docs/ACADEMY_DELIVERY_MODE_ARCHITECTURE.md (proposal). No code changed.
STOP_AFTER_DELIVERY = TRUE.
```

| Column | E_LEARNING | PHYSICAL | HYBRID |
|---|---|---|---|
| **DISCOVERY** | Public, real today: `GET /formations`, `GET /formations/{code}` via `get_current_user_optional` (`backend/auth.py:217-226`) — full detail, unauth | Same routes/mechanism could carry real session summary once `TrainingSession` exists; today shows only the aspirational `delivery_formats` label, no session data | Same base discovery; would show composition topology once `HybridComposition` exists |
| **IDENTITY_REQUIRED** | For learning (write paths), yes — no for browsing | Yes, for registration/enrollment (identity always required before an application is submitted) | Yes, for any step's progress to persist |
| **ACCESS_RULE** | `is_module_unlocked` / `is_formation_unlocked` (`lx.py`) — real, working | None exists — would be `SessionEnrollment.status == CONFIRMED` (proposed) | Per-step: e-learning steps use existing unlock logic; physical steps use proposed `SessionEnrollment` |
| **SCHEDULING_REQUIRED** | No | Yes — no model exists (`TrainingSession` proposed) | Yes, for physical steps only |
| **LOCATION_REQUIRED** | No | Yes — no model exists (`TrainingLocation` proposed); `User.territoire` is learner geography, not venue | Yes, for physical steps only |
| **CAPACITY_REQUIRED** | No | Yes — zero hits anywhere in repo; `TrainingSession.capacity` proposed | Yes, for physical steps only |
| **ATTENDANCE_REQUIRED** | No — completion ≠ attendance (mission §3) | Yes — no model exists (`AttendanceRecord` proposed) | Yes, for physical steps only |
| **ONLINE_PROGRESS** | Yes — real, `ModuleProgress` + quiz/mission engines | No | Yes, for e-learning steps only |
| **ASSESSMENT** | Quiz + mini-mission engines (real) | Practical/jury assessment — no model exists (`AssessmentResult` proposed) | Combination per that formation's `HybridComposition` |
| **PROOF** | Module completion / quiz / deliverable / mini-mission / skill (real) | Verified attendance + trainer validation + assessment result (proposed, none built) | Union of whichever steps the composition contains |
| **CERTIFICATION** | Existing certification/badge engine (real) | Same engine, but its physical-mode inputs (attendance/assessment) don't exist yet | Same engine; inputs depend on composition |
| **PAYMENT_OR_FUNDING** | Not implemented (`MISSING`, audit §Monetization) | Not implemented; `funding_options` is `INTERFACE_ONLY` placeholder (`needs_external_calibration`) | Not implemented; would combine both, never a shared status enum (architecture §6) |
| **RETURN_FLOW** | Dashboard / `next_action` — real, shared | Would extend `next_action` with session-relative state ("session in 3 days," "attendance pending") — not built | Same extension, mode-aware per current step |
| **CURRENT_STATUS** | Fully operational, production | Label only (`delivery_formats` marketing tag); zero operational backing | Label only; zero operational backing; naming collision risk with `HOS-01` content |
| **GAP** | Presentational labeling only (flow isn't explicitly named as "e-learning" in UI) | Session/Location/Capacity/Attendance/Enrollment/Assessment models entirely absent | All of PHYSICAL's gaps, plus the composition model itself |
| **BACKEND_TRUTH** | Yes — `ModuleProgress`, quiz/mission results, certification records are authoritative and real | No — nothing to be authoritative about yet | No — depends entirely on PHYSICAL's backend truth existing first |
| **FRONTEND_TRUTH** | Yes — dashboard/roadmap read real progress | No — zero frontend consumption of `delivery_formats` confirmed by grep (audit) | No |

## Reading notes

- Every "MISSING"/"not built"/"proposed" cell traces directly to a
  specific finding in `ACADEMY_DELIVERY_MODE_AUDIT.md`; nothing here
  introduces a new gap the audit didn't already surface.
- This matrix is a snapshot of **today's repository state plus the
  architecture proposal**, not a build plan with dates — no timeline or
  implementation commitment is implied.
