# Phase 5 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 5 (User Story 3 — Slot Released: Cancel → Promote & Notify) is complete before proceeding to Phase 6.  
**Phase 5 scope**: T021, T022, T023  
**Created**: 2026-03-01

---

## T021 — Cancel booking + promote first waitlisted + notification stub (backend)

- [x] **Backend** — `backend/services.py` defines `cancel_booking(booking_id)` (or equivalent)
- [x] **Backend** — Returns `(None, "not_found", None)` when booking does not exist
- [x] **Backend** — Returns `(None, "invalid_state", None)` when booking state is not confirmed or waitlisted (e.g. already cancelled)
- [x] **Backend** — Updates booking to state `"cancelled"` (and clears position if waitlisted)
- [x] **Backend** — When cancelled booking was **confirmed** and workshop has waitlisted: first waitlisted (by position) is promoted to `"confirmed"` and position cleared
- [x] **Backend** — Notification stub exists: e.g. `trigger_slot_released_notification(workshop_id, promoted_booking)` called when first waitlisted is promoted (backend-only; delivery out of scope)
- [x] **Backend** — Returns `(cancelled_booking, "cancelled", promoted_booking_or_none)` for success

---

## T022 — POST /bookings/{booking_id}/cancel (backend)

- [x] **Backend** — `backend/main.py` defines `POST /bookings/{booking_id}/cancel` (or `/api/...`)
- [x] **Backend** — **200 OK** when cancellation succeeds; response body includes cancellation confirmation (e.g. `cancelled`, `booking_id`, `state: "cancelled"`)
- [x] **Backend** — Response may include `promoted_booking_id` when first waitlisted was promoted (Phase 5)
- [x] **Backend** — **404 Not Found** when booking not found
- [x] **Backend** — **400 Bad Request** when booking cannot be cancelled (e.g. already cancelled or no_show)
- [x] **Manual** — `curl -X POST http://localhost:8000/bookings/{booking_id}/cancel` returns 200 (optional)

---

## T023 — Frontend API client and cancel action in My Bookings

- [x] **Frontend** — `frontend/src/services/api.js` exports `cancelBooking(bookingId)`
- [x] **Frontend** — `cancelBooking` sends `POST ${API_BASE}/bookings/${bookingId}/cancel` (no body or empty body)
- [x] **Frontend** — `cancelBooking` returns parsed JSON on success; throws on non-ok response
- [x] **Frontend** — My Bookings view (e.g. `MyBookings.jsx`) shows a cancel action per booking (e.g. "Cancel booking" button)
- [x] **Frontend** — Cancel action only offered for bookings in `confirmed` or `waitlisted` state (not cancelled / no_show)
- [x] **Frontend** — On cancel success: list is refreshed (e.g. re-fetch `getMyBookings(email)`) or cancelled item removed/updated
- [x] **Frontend** — Loading/disabled state while cancel request in progress (e.g. "Cancelling…")
- [x] **Constitution** — No direct call to external 3rd party API; only backend URL

---

## tasks.md and Git

- [x] **tasks.md** — T021, T022, T023 are marked complete: `- [x] T021 ...` … `- [x] T023 ...`
- [x] **Git** — Phase 5 commits exist (e.g. T021, T022, T023) in `git log --oneline`
- [x] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Contract alignment (backend-api.md)

- [x] **Cancel booking** — Method POST (or DELETE); path `/bookings/{booking_id}/cancel`
- [x] **Cancel booking** — **200 OK**; body may include refund info in Phase 6; for Phase 5 at least `cancelled`, `booking_id`
- [x] **Side effect** — If was confirmed and waitlist non-empty: first waitlisted promoted, "slot released" notification triggered (backend-only)

---

## User Story 3 — Independent test (MVP)

- [x] **E2E** — Load My Bookings with an email that has a confirmed or waitlisted booking → Cancel button visible
- [x] **E2E** — Click Cancel → booking moves to cancelled (or disappears from active list); list refreshes
- [x] **E2E** — Cancel a **confirmed** booking when workshop has waitlisted → first waitlisted becomes confirmed (verify via My Bookings with that user’s email or workshop confirmed count)
- [x] **E2E** — Cancel when waitlist empty → seat available for new request-seat (optional: request seat again and get confirmed)

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 5 complete when all checkboxes above are checked.** Proceed to Phase 6 (T024–T025) after sign-off.
