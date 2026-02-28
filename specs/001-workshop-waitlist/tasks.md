# Tasks: Workshop SlotIn — Waitlist & Slot-Release

**Input**: Design documents from `/specs/001-workshop-waitlist/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Backend unit tests for capacity, waitlist promotion, and refund logic are required per Constitution (pytest). Included in Phase 2 (test structure) and Phase 9 (Polish).

**Organization**: Tasks grouped by user story (US1–US5) for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story (US1–US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [ ] T001 Create backend/ and frontend/ directory structure per plan (backend/main.py, services.py, models.py, tests/; frontend/src with components, pages, services, context)
- [ ] T002 Initialize backend with FastAPI, uvicorn, pydantic in backend/ (requirements.txt or pyproject.toml)
- [ ] T003 Initialize frontend with Vite React, Tailwind CSS, Lucide React in frontend/
- [ ] T004 [P] Configure backend formatting (black, ruff) and frontend Prettier

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend and API foundation; MUST be complete before any user story

- [ ] T005 [P] Create Pydantic models (Workshop, Booking, request/response DTOs) in backend/models.py
- [ ] T006 Implement workshop load/save from JSON file in backend/services.py (workshops.json path configurable)
- [ ] T007 Implement in-memory bookings store and accessors in backend/services.py
- [ ] T008 Create FastAPI app with CORS and base health route in backend/main.py
- [ ] T009 Seed backend/workshops.json with at least one sample workshop (id, title, date_time, capacity)
- [ ] T010 [P] Add pytest and test layout in backend/tests/ (test_services.py placeholder)

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — Browse Workshops & See Availability (Priority: P1) — MVP

**Goal**: User sees workshop list with title, date/time, capacity, confirmed and waitlisted counts.

**Independent Test**: Load app → workshop list displays with correct counts; confirmed ≤ capacity.

- [ ] T011 [P] [US1] Implement GET /workshops (or /api/workshops) returning list with counts in backend/main.py
- [ ] T012 [US1] Add getWorkshops() to frontend API client in frontend/src/services/api.js (or .ts)
- [ ] T013 [US1] Create WorkshopList component in frontend/src/components/WorkshopList.jsx (or .tsx)
- [ ] T014 [US1] Wire home page to fetch and display workshop list (title, date_time, capacity, confirmed_count, waitlisted_count) in frontend/src/App.jsx or pages/Home.jsx

**Checkpoint**: User Story 1 complete — catalog visible and testable

---

## Phase 4: User Story 2 — Request Seat & My Bookings (Priority: P2)

**Goal**: User can request a seat (confirm or waitlist with position); user can view "my bookings" by email.

**Independent Test**: Request seat when capacity available → confirmed; when full → waitlist position. View bookings by email → see state and position.

- [ ] T015 [US2] Implement request-seat logic (confirm or waitlist, first-request-wins) in backend/services.py
- [ ] T016 [US2] Implement POST /workshops/{workshop_id}/request-seat with email body in backend/main.py
- [ ] T017 [US2] Implement GET /bookings?email= in backend/main.py returning user's bookings with workshop summary
- [ ] T018 [US2] Add requestSeat() and getMyBookings(email) to frontend/src/services/api.js
- [ ] T019 [US2] Create RequestSeatForm component (workshop, email input) and My Bookings view in frontend/src/components/
- [ ] T020 [US2] Wire request-seat flow (from workshop list or detail) and my-bookings page (email input → list) in frontend

**Checkpoint**: User Stories 1 and 2 complete — sign-up and my bookings work

---

## Phase 5: User Story 3 — Slot Released (Cancel → Promote & Notify) (Priority: P3)

**Goal**: On cancel, first waitlisted is promoted and backend triggers "slot released" notification; or seat freed if waitlist empty.

**Independent Test**: Cancel confirmed when waitlist non-empty → first promoted, notification triggered; cancel when waitlist empty → seat available for new requests.

- [ ] T021 [US3] Implement cancel booking + promote first waitlisted + trigger notification stub in backend/services.py
- [ ] T022 [US3] Implement POST /bookings/{booking_id}/cancel (or cancel by workshop+email) in backend/main.py
- [ ] T023 [US3] Add cancelBooking() to frontend API client and cancel button/action in my-bookings or booking detail UI in frontend/src/

**Checkpoint**: User Stories 1–3 complete — waitlist promotion and cancel work

---

## Phase 6: User Story 4 — Cancellation & Refund Rules (Priority: P4)

**Goal**: Refund window (≥24h) yields pro-rata refund; last-minute (<24h) no refund. Cancel response includes refund info when applicable.

**Independent Test**: Cancel ≥24h before start → refund info in response (pro-rata); cancel <24h → no refund, cancellation only.

- [ ] T024 [US4] Implement refund window (24h) and pro-rata-by-time logic (e.g. 7 days = full, 3 days = 50%) in backend/services.py
- [ ] T025 [US4] Return refund_percentage or refund info in cancel response when within window; show refund message in frontend after cancel

**Checkpoint**: User Stories 1–4 complete — refund rules enforced

---

## Phase 7: User Story 5 — No-Show Handling (Priority: P5)

**Goal**: Admin can mark confirmed participant as no-show via /admin; no seat freed, no waitlist promotion.

**Independent Test**: Open /admin → mark confirmed booking no-show → state recorded; no promotion.

- [ ] T026 [US5] Implement POST /admin/bookings/{booking_id}/no-show in backend/main.py
- [ ] T027 [US5] Create Admin page at route /admin with list of confirmed bookings and no-show action in frontend/src/pages/Admin.jsx (or equivalent)
- [ ] T028 [US5] Add noShowBooking() to frontend API client and wire admin page to backend

**Checkpoint**: All user stories complete

---

## Phase 8: Polish & Cross-Cutting

**Purpose**: Tests, validation, and cleanup

- [ ] T029 [P] Add unit tests for workshop capacity, waitlist promotion, and refund-window logic in backend/tests/test_services.py
- [ ] T030 Run quickstart.md validation (backend + frontend start, manual test scenarios) and fix if needed
- [ ] T031 [P] Add .env.example for backend (API keys placeholder) and document in README or quickstart

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3–7 (US1–US5)**: Depend on Phase 2; can proceed sequentially (P1→P2→…→P5) or US2–US5 in parallel after US1
- **Phase 8 (Polish)**: Depends on Phase 7 (or earlier if skipping some stories)

### User Story Dependencies

- **US1 (P1)**: After Phase 2 only — no other story dependency
- **US2 (P2)**: After Phase 2; uses workshops and bookings from foundation
- **US3 (P3)**: After US2 (cancel and promote depend on request-seat and bookings)
- **US4 (P4)**: After US3 (refund logic applies to cancel flow)
- **US5 (P5)**: After US2 (no-show acts on confirmed bookings)

### Parallel Opportunities

- T004, T005, T010 can run in parallel within their phase
- After Phase 2, T011–T014 (US1) first; then T015–T020 (US2), etc.
- T029 and T031 can run in parallel in Phase 8

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 + Phase 2
2. Complete Phase 3 (US1)
3. Stop and validate: workshop list loads with correct counts
4. Demo MVP

### Incremental Delivery

1. Phase 1 + 2 → foundation
2. Phase 3 (US1) → catalog MVP
3. Phase 4 (US2) → request seat + my bookings
4. Phase 5 (US3) → slot released
5. Phase 6 (US4) → refund rules
6. Phase 7 (US5) → admin no-show
7. Phase 8 → tests and quickstart validation

---

## Notes

- [P] = parallelizable (different files, no dependency on incomplete tasks)
- [USn] = task belongs to User Story n for traceability
- Each user story is independently testable per spec
- Commit after each task or logical group
- Backend tests required per Constitution; frontend tests optional
