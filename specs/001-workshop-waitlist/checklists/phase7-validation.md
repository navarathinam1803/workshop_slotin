# Phase 7 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 7 (User Story 5 — No-Show Handling) is complete before proceeding to Phase 8.  
**Phase 7 scope**: T026, T027, T028  
**Created**: 2026-03-01

---

## T026 — POST /admin/bookings/{booking_id}/no-show (backend)

- [x] **Backend** — `backend/main.py` defines `POST /admin/bookings/{booking_id}/no-show` (or `/api/admin/...`)
- [x] **Backend** — Only **confirmed** bookings can be marked no-show (400 if waitlisted/cancelled/no_show)
- [x] **Backend** — **200 OK** when no-show recorded; response body e.g. `{ "marked_no_show": true, "booking_id": "...", "state": "no_show" }`
- [x] **Backend** — **404 Not Found** when booking not found
- [x] **Backend** — **400 Bad Request** when booking state is not confirmed
- [x] **Backend** — No seat freed; no waitlist promotion (state change only; logic in `services.mark_no_show`)
- [x] **Backend** — Admin list: `GET /admin/bookings` returns confirmed bookings with workshop_title, workshop_date_time, email (for admin UI)

---

## T027 — Admin page at route /admin

- [x] **Frontend** — Route `/admin` exists (e.g. via react-router-dom: `Route path="/admin"`)
- [x] **Frontend** — Admin page at `frontend/src/pages/Admin.jsx` (or equivalent)
- [x] **Frontend** — Page fetches list of confirmed bookings (e.g. `getAdminBookings()` → GET `/admin/bookings`)
- [x] **Frontend** — Displays workshop title, date/time, email per confirmed booking
- [x] **Frontend** — Each row has a "Mark no-show" (or equivalent) action
- [x] **Frontend** — Navigation to /admin from home (e.g. "Admin" link in App header) and back (e.g. "← Workshop SlotIn" on admin page)
- [x] **Frontend** — Uses Tailwind; function component (hooks)

---

## T028 — noShowBooking() in API client and wire to backend

- [x] **Frontend** — `frontend/src/services/api.js` exports `noShowBooking(bookingId)`
- [x] **Frontend** — `noShowBooking` sends `POST ${API_BASE}/admin/bookings/${bookingId}/no-show` (no body or empty body)
- [x] **Frontend** — `noShowBooking` returns parsed JSON on success; throws on non-ok response
- [x] **Frontend** — `frontend/src/services/api.js` exports `getAdminBookings()` for admin list (GET `/admin/bookings`)
- [x] **Frontend** — Admin page calls `noShowBooking(bookingId)` when user clicks "Mark no-show"; list refreshes after success
- [x] **Frontend** — Loading/disabled state while marking (e.g. "Marking…")
- [x] **Constitution** — No direct call to external 3rd party API; only backend URL

---

## tasks.md and Git

- [x] **tasks.md** — T026, T027, T028 are marked complete: `- [x] T026 ...` … `- [x] T028 ...`
- [x] **Git** — Phase 7 commits exist (e.g. T026, T027/T028) in `git log --oneline`
- [x] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Contract alignment (backend-api.md)

- [x] **Mark no-show (admin)** — Method POST; path `/admin/bookings/{booking_id}/no-show`
- [x] **Mark no-show (admin)** — **200 OK** — No-show recorded. No seat freed; no waitlist promotion.
- [x] **Note** — No auth; demo trust. Frontend admin page at `/admin` calls this endpoint.

---

## User Story 5 — Independent test (MVP)

- [x] **E2E** — Open `/admin` → list of confirmed bookings displays (or "No confirmed bookings")
- [x] **E2E** — Click "Mark no-show" on a confirmed booking → state recorded (booking moves to no_show or leaves list); list refreshes
- [x] **E2E** — After marking no-show: workshop confirmed count unchanged (no promotion); seat not freed for new requests

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 7 complete when all checkboxes above are checked.** Proceed to Phase 8 (T029–T031) after sign-off.
