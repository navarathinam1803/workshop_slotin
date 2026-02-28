# Phase 2 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify all Phase 2 (Foundational) tasks are complete before proceeding to Phase 3.  
**Phase 2 scope**: T005, T006, T007, T008, T009, T010  
**Created**: 2026-03-01

---

## T005 — Pydantic models

- [ ] **Backend** — `backend/models.py` exists
- [ ] **Backend** — Workshop model(s): WorkshopBase, WorkshopOut, WorkshopCreate, or WorkshopIn
- [ ] **Backend** — Booking model(s): BookingState enum, BookingOut, BookingCreate
- [ ] **Backend** — Request/response DTOs: RequestSeatRequest, RequestSeatResponse (or equivalent)
- [ ] **Backend** — Email validation: EmailStr or equivalent for email fields
- [ ] **Backend** — `requirements.txt` includes `pydantic` (or `pydantic[email-validator]`)

---

## T006 — Workshop load/save from JSON

- [ ] **Backend** — `backend/services.py` defines `load_workshops()` returning list of workshop dicts
- [ ] **Backend** — `backend/services.py` defines `save_workshops(workshops)` persisting to file
- [ ] **Backend** — Workshop file path is configurable (e.g. env `WORKSHOPS_JSON` or default path)
- [ ] **Backend** — Load reads from JSON file; save writes with valid JSON (e.g. `default=str` for dates)

---

## T007 — In-memory bookings store

- [ ] **Backend** — In-memory store for bookings (e.g. `_bookings` list) in `backend/services.py`
- [ ] **Backend** — `add_booking(workshop_id, email, state, position?)` creates and appends booking with `id`, `created_at`
- [ ] **Backend** — `get_booking_by_id(booking_id)` returns one booking or None
- [ ] **Backend** — `get_bookings_by_email(email)` returns list of bookings for that email
- [ ] **Backend** — `get_bookings_by_workshop(workshop_id)` returns list of bookings for that workshop
- [ ] **Backend** — `update_booking_state(booking_id, state, position?)` updates and returns booking or None

---

## T008 — FastAPI app with CORS and health route

- [ ] **Backend** — `backend/main.py` creates FastAPI app
- [ ] **Backend** — CORSMiddleware added with allow_origins (e.g. `["*"]` for demo)
- [ ] **Backend** — `GET /health` route returns JSON (e.g. `{"status": "ok"}`)
- [ ] **Backend** — Running `uvicorn main:app --reload` from `backend/` starts server (optional run)

---

## T009 — Seed workshops.json

- [ ] **Backend** — `backend/workshops.json` exists
- [ ] **Backend** — File contains at least one workshop object
- [ ] **Backend** — Each workshop has `id`, `title`, `date_time`, `capacity` (ISO8601 for date_time)

---

## T010 — Pytest test layout

- [ ] **Backend** — `backend/tests/conftest.py` exists (or path setup so tests can import from backend)
- [ ] **Backend** — `backend/tests/test_services.py` exists
- [ ] **Backend** — At least one test in test_services.py (e.g. test_load_workshops or placeholder)
- [ ] **Backend** — `pytest` in `backend/requirements.txt`
- [ ] **Backend** — `python -m pytest backend/tests/` or `cd backend && pytest tests/` runs (optional; after pip install)

---

## tasks.md and Git

- [ ] **tasks.md** — T005 through T010 are marked complete: `- [x] T005 ...` … `- [x] T010 ...`
- [ ] **Git** — Six Phase 2 commits exist (one per task): T005, T006, T007, T008, T009, T010 in `git log --oneline`
- [ ] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Constitution alignment (Phase 2)

- [ ] **No external DB** — Only in-memory bookings and local JSON for workshops
- [ ] **Pydantic** — Request/response and validation use Pydantic
- [ ] **Backend tests** — pytest layout present for capacity, waitlist, refund (full tests in Phase 8)

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 2 complete when all checkboxes above are checked.** Proceed to Phase 3 (T011–T014) after sign-off.
