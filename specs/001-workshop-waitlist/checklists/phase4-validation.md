# Phase 4 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 4 (User Story 2 — Request Seat & My Bookings) is complete before proceeding to Phase 5.  
**Phase 4 scope**: T015, T016, T017, T018, T019, T020  
**Created**: 2026-03-01

---

## T015 — Request-seat logic (backend)

- [ ] **Backend** — `backend/services.py` defines `request_seat(workshop_id, email)` (or equivalent)
- [ ] **Backend** — Returns `(None, "not_found")` when workshop does not exist
- [ ] **Backend** — Returns `(None, "already_booked")` when email already has confirmed or waitlisted booking for that workshop
- [ ] **Backend** — When capacity available: creates booking with state `"confirmed"`, returns `(booking, "confirmed")`
- [ ] **Backend** — When at capacity: creates booking with state `"waitlisted"` and next position; returns `(booking, "waitlisted")`
- [ ] **Backend** — First-request-wins: capacity checked in one logical step (no race for last seat)

---

## T016 — POST /workshops/{workshop_id}/request-seat (backend)

- [ ] **Backend** — `backend/main.py` defines `POST /workshops/{workshop_id}/request-seat` (or `/api/...`)
- [ ] **Backend** — Request body validated with Pydantic (e.g. `RequestSeatRequest` with `email: EmailStr`)
- [ ] **Backend** — **201 Created** when seat confirmed; response body includes `booking_id`, `state`, `workshop_id`, `email` (and `position` when waitlisted)
- [ ] **Backend** — **202 Accepted** when waitlisted; response includes `position`
- [ ] **Backend** — **404 Not Found** when workshop not found
- [ ] **Backend** — **409 Conflict** when user already has a booking for this workshop (optional business rule)
- [ ] **Backend** — **400 Bad Request** on invalid email (Pydantic validation)
- [ ] **Manual** — `curl -X POST http://localhost:8000/workshops/{id}/request-seat -H "Content-Type: application/json" -d '{"email":"a@b.com"}'` returns 201 or 202 (optional)

---

## T017 — GET /bookings?email= (backend)

- [ ] **Backend** — `backend/main.py` defines `GET /bookings` with required query param `email`
- [ ] **Backend** — Returns JSON array of bookings for that email only
- [ ] **Backend** — Each item includes: `id`, `workshop_id`, `email`, `state`, `position`, `workshop_title`, `workshop_date_time`
- [ ] **Backend** — `workshop_title` and `workshop_date_time` derived from `load_workshops()` (enriched response)
- [ ] **Manual** — `curl "http://localhost:8000/bookings?email=user@example.com"` returns 200 and array (optional)

---

## T018 — Frontend API client (requestSeat, getMyBookings)

- [ ] **Frontend** — `frontend/src/services/api.js` exports `requestSeat(workshopId, email)`
- [ ] **Frontend** — `requestSeat` sends `POST ${API_BASE}/workshops/${workshopId}/request-seat` with body `{ email }`
- [ ] **Frontend** — `requestSeat` returns parsed JSON on success; throws on non-ok response
- [ ] **Frontend** — `frontend/src/services/api.js` exports `getMyBookings(email)`
- [ ] **Frontend** — `getMyBookings` sends `GET ${API_BASE}/bookings?email=...` and returns parsed JSON (or throws)
- [ ] **Constitution** — No direct call to external 3rd party API; only backend URL

---

## T019 — RequestSeatForm and MyBookings components

- [ ] **Frontend** — `frontend/src/components/RequestSeatForm.jsx` exists (or .tsx)
- [ ] **Frontend** — RequestSeatForm accepts `workshop` prop (id, title, date_time) and optional `onClose`
- [ ] **Frontend** — RequestSeatForm has email input and submit; calls `requestSeat(workshop.id, email)`
- [ ] **Frontend** — RequestSeatForm shows success: confirmed vs waitlisted (with position) and booking_id
- [ ] **Frontend** — RequestSeatForm shows error message on failure (e.g. 404, 409)
- [ ] **Frontend** — `frontend/src/components/MyBookings.jsx` exists (or .tsx)
- [ ] **Frontend** — MyBookings has email input and "Load my bookings" (or equivalent) action
- [ ] **Frontend** — MyBookings calls `getMyBookings(email)` and displays list: state, position, workshop title, date
- [ ] **Frontend** — Both use Tailwind; function components (hooks)

---

## T020 — Wire request-seat and my-bookings in App

- [ ] **Frontend** — `frontend/src/App.jsx` imports `RequestSeatForm` and `MyBookings`
- [ ] **Frontend** — Workshop list (or each workshop) has a "Request seat" action that opens/shows RequestSeatForm for that workshop
- [ ] **Frontend** — RequestSeatForm can be closed (e.g. onClose clears selected workshop)
- [ ] **Frontend** — "My bookings" section present: user can enter email and see MyBookings list
- [ ] **Manual** — E2E: Click "Request seat" on a workshop → submit email → see confirmed or waitlisted; then load "My bookings" with same email → see the booking (optional)

---

## tasks.md and Git

- [ ] **tasks.md** — T015 through T020 are marked complete: `- [x] T015 ...` … `- [x] T020 ...`
- [ ] **Git** — Phase 4 commits exist (e.g. T015–T020) in `git log --oneline`
- [ ] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Contract alignment (backend-api.md)

- [ ] **Request-seat** — Email required and valid format (Pydantic EmailStr or equivalent)
- [ ] **Request-seat** — 201 body: `booking_id`, `state`, `workshop_id`, `email`; 202 adds `position`
- [ ] **My bookings** — GET `/bookings?email=...` returns array with `id`, `workshop_id`, `email`, `state`, `position`, `workshop_title`, `workshop_date_time`
- [ ] **Errors** — 400 for validation (e.g. invalid email), 404 workshop not found, 409 already booked

---

## User Story 2 — Independent test (MVP)

- [ ] **E2E** — Request seat when capacity available → user sees confirmed message and booking ID
- [ ] **E2E** — Request seat when workshop full → user sees waitlisted message with position
- [ ] **E2E** — Same email requests same workshop again → error (already booked) or no duplicate
- [ ] **E2E** — Enter email in "My bookings" → list shows state, position, workshop title, date

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 4 complete when all checkboxes above are checked.** Proceed to Phase 5 (T021–T023) after sign-off.
