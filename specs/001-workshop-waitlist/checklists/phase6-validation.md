# Phase 6 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 6 (User Story 4 — Cancellation & Refund Rules) is complete before proceeding to Phase 7.  
**Phase 6 scope**: T024, T025  
**Created**: 2026-03-01

---

## T024 — Refund window (24h) and pro-rata-by-time logic (backend)

- [x] **Backend** — `backend/services.py` defines refund window (e.g. 24h before workshop start)
- [x] **Backend** — Cancel &lt;24h before start: no refund (refund_percentage 0 or not in window)
- [x] **Backend** — Cancel ≥24h before start: pro-rata refund computed (e.g. 7 days = full/100%, 3 days = 50%)
- [x] **Backend** — Refund logic uses workshop `date_time` (from `load_workshops()`) and current time
- [x] **Backend** — Function such as `compute_refund(workshop_id)` returns `{"refund_percentage": int}` or None when workshop not found / no date
- [x] **Backend** — Pro-rata scale is documented or configurable (e.g. constants for 7 days full, 3 days half)

---

## T025 — Refund in cancel response and frontend message

- [x] **Backend** — Cancel endpoint (POST `/bookings/{booking_id}/cancel`) includes `refund_percentage` in 200 response when applicable
- [x] **Backend** — Response body may include `refund_percentage` (0 when within 24h, or pro-rata value when within window)
- [x] **Frontend** — After cancel success, user sees a refund message (e.g. "Cancelled. Refund: 50%." or "Cancelled. No refund (within 24h of start).")
- [x] **Frontend** — Message derived from cancel API response (e.g. `refund_percentage`); shown in My Bookings area after cancel
- [x] **Frontend** — Refund message is cleared on next load or next cancel action (no stale message)

---

## tasks.md and Git

- [x] **tasks.md** — T024 and T025 are marked complete: `- [x] T024 ...` and `- [x] T025 ...`
- [x] **Git** — Phase 6 commits exist (e.g. T024, T025) in `git log --oneline`
- [x] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Contract alignment (backend-api.md)

- [x] **Cancel booking** — **200 OK** response body may include refund info when within refund window (e.g. `refund_percentage` or pro-rata value)
- [x] **Refund rules** — ≥24h before start → refund (pro-rata); &lt;24h → no refund, cancellation only

---

## User Story 4 — Independent test (MVP)

- [x] **E2E** — Cancel a booking ≥24h before workshop start → response includes `refund_percentage`; frontend shows "Refund: X%"
- [x] **E2E** — Cancel a booking &lt;24h before start (or mock time) → response includes `refund_percentage: 0` or no refund; frontend shows no-refund message
- [x] **E2E** — Pro-rata: cancel 7+ days before → 100%; cancel ~3 days before → ~50% (optional manual check)

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 6 complete when all checkboxes above are checked.** Proceed to Phase 7 (T026–T028) after sign-off.
