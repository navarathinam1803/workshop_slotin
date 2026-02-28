# Quickstart: Workshop SlotIn (001-workshop-waitlist)

**Branch**: `001-workshop-waitlist` | **Date**: 2026-03-01

Minimal steps to run and manually test the feature after implementation.

## Prerequisites

- Python 3.10+
- Node 18+ and npm (or pnpm/yarn)
- (Optional) `.env` in backend root for any API keys (e.g. notification service); not required for core flows.

## Backend

1. From repo root: `cd backend`
2. Create virtualenv: `python -m venv .venv` (or use uv/poetry per team).
3. Activate: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows).
4. Install: `pip install fastapi uvicorn pydantic`
5. Ensure `workshops.json` exists or is created on first run (see data-model: workshops persisted to JSON).
6. Run: `uvicorn main:app --reload` (or `python -m uvicorn main:app --reload`). Default: `http://localhost:8000`.

## Frontend

1. From repo root: `cd frontend`
2. Install: `npm install`
3. Run: `npm run dev` (Vite). Default: `http://localhost:5173`.
4. Configure API base URL to backend (e.g. `http://localhost:8000`) via env (e.g. `VITE_API_URL`) or hardcoded for demo.

## Manual test scenarios (after implementation)

1. **Catalog**: Open frontend → see workshop list with title, date/time, capacity, confirmed and waitlisted counts.
2. **Request seat (confirm)**: Pick a workshop with capacity → enter email → submit → see confirmation; count increases.
3. **Request seat (waitlist)**: Fill workshop to capacity (or use pre-seeded data) → request with new email → see waitlist position.
4. **My bookings**: Enter same email → see "my bookings" with state and (if waitlisted) position.
5. **Cancel (release slot)**: Cancel a confirmed booking when waitlist non-empty → first waitlisted becomes confirmed; backend triggers "slot released" (check backend log or notification stub).
6. **Refund window**: Cancel ≥24h before start → expect refund path (pro-rata); cancel <24h → no refund, cancellation only.
7. **Admin no-show**: Open `/admin` → mark a confirmed participant no-show → state recorded; no promotion from waitlist.
8. **Concurrent last seat**: Two requests for last seat (e.g. two tabs or scripts) → one confirmed, one waitlisted (first-accepted wins).

## Running backend tests

- From `backend/`: `pytest tests/` (or `python -m pytest tests/`). Covers unit tests for capacity, waitlist promotion, refund-window logic per constitution.
