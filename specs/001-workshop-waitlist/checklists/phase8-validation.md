# Phase 8 Validation Checklist — Workshop SlotIn (001-workshop-waitlist)

**Purpose**: Verify Phase 8 (Polish & Cross-Cutting) is complete.  
**Phase 8 scope**: T029, T030, T031  
**Created**: 2026-03-01

---

## T029 — Unit tests (backend)

- [x] **Backend** — `backend/tests/test_services.py` exists and is runnable with `pytest tests/` from `backend/`
- [x] **Backend** — Tests cover **workshop capacity**: request_seat when capacity available → confirmed; when at capacity → waitlisted with position
- [x] **Backend** — Tests cover **waitlist promotion**: cancel confirmed when waitlist non-empty → first waitlisted promoted to confirmed; cancel when waitlist empty → no promotion
- [x] **Backend** — Tests cover **refund-window logic**: &lt;24h before start → refund_percentage 0; ≥24h with pro-rata (e.g. 7 days = 100%, ~4 days = 50–100%); workshop not found → None
- [x] **Backend** — Tests use isolated state (e.g. clear bookings or monkeypatch load_workshops) so they are deterministic
- [x] **Manual** — From `backend/`: `pytest tests/` (or `python -m pytest tests/`) passes

---

## T030 — Quickstart validation

- [x] **Docs** — `specs/001-workshop-waitlist/quickstart.md` (or repo quickstart) describes backend and frontend run steps
- [x] **Docs** — Backend: create venv, install deps (e.g. `pip install -r requirements.txt`), run `uvicorn main:app --reload` from backend dir
- [x] **Docs** — Frontend: `npm install`, `npm run dev`; API base URL config (e.g. `VITE_API_URL`)
- [x] **Docs** — Manual test scenarios listed (catalog, request seat confirm/waitlist, my bookings, cancel/promotion, refund window, admin no-show, concurrent last seat)
- [x] **Docs** — Backend tests: run `pytest tests/` from backend
- [x] **Manual** — Backend and frontend start per quickstart; at least one manual scenario verified (optional)

---

## T031 — .env.example and documentation

- [x] **Backend** — `backend/.env.example` exists with placeholders (e.g. `WORKSHOPS_JSON`, optional API keys for notification)
- [x] **Backend** — .env.example documents that .env is optional for core flows
- [x] **Docs** — README or quickstart references `backend/.env.example` (e.g. "See backend/.env.example for placeholders")

---

## tasks.md and Git

- [x] **tasks.md** — T029, T030, T031 are marked complete: `- [x] T029 ...` … `- [x] T031 ...`
- [x] **Git** — Phase 8 commits exist (e.g. T029, T030, T031) in `git log --oneline`
- [x] **Git** — Branch `001-workshop-waitlist` pushed to `origin` (optional)

---

## Constitution alignment

- [x] **pytest** — Backend unit tests for capacity, waitlist promotion, and refund-window logic per constitution/spec

---

## Sign-off

| Role        | Name | Date | Notes |
|------------|------|------|--------|
| Developer  |      |      |        |
| Reviewer   |      |      |        |

**Phase 8 complete when all checkboxes above are checked.** All phases (1–8) and user stories (US1–US5) are then complete.
