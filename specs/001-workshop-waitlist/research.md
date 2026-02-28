# Research: 001-workshop-waitlist

**Branch**: `001-workshop-waitlist` | **Date**: 2026-03-01

Technical choices are driven by the project Constitution and the clarified spec. This document records decisions and rationale; no unresolved NEEDS CLARIFICATION remained after spec clarify.

## 1. Backend framework (FastAPI)

- **Decision**: FastAPI with Pydantic v2.
- **Rationale**: Constitution mandates Python 3.10+ and FastAPI; Pydantic for validation. No alternative evaluation needed.
- **Alternatives considered**: None; constitution is binding.

## 2. Frontend stack (React + Vite + Tailwind)

- **Decision**: React with Vite, Tailwind CSS, Lucide React; React Context + local state only (no Redux).
- **Rationale**: Constitution mandates this stack and forbids Redux and class components.
- **Alternatives considered**: None; constitution is binding.

## 3. Persistence (hybrid: workshops on disk, bookings in-memory)

- **Decision**: Workshops persisted to local JSON file(s); bookings stored in-memory (e.g. dict/list keyed by workshop and email).
- **Rationale**: Clarification outcome: hybrid. Workshop catalog survives restart; booking state is ephemeral for demo.
- **Alternatives considered**: Full in-memory (rejected per clarify); full persistence (accepted as optional future step).

## 4. Participant identity (email, no password)

- **Decision**: User supplies email when requesting a seat; backend links bookings and notifications to that email. "My bookings" retrieved by email.
- **Rationale**: Clarification outcome (Option C). Enables notifications and "my bookings" without auth.
- **Alternatives considered**: Session-only, localStorage ID, or no identity; email chosen for contact and clarity.

## 5. Concurrent last seat (first request wins)

- **Decision**: When two requests contend for the last seat, the request processed first by the server gets the seat; the other is added to the waitlist.
- **Rationale**: Clarification outcome (Option A). Simple, no distributed lock required.
- **Alternatives considered**: Random tie-break, timestamp-based, or both to waitlist; first-accepted chosen for simplicity.

## 6. Refund policy (pro-rata by time)

- **Decision**: Within refund window (≥24h before start), refund is pro-rata by time (e.g. 7 days = full, 3 days = 50%). Last-minute (<24h) = no refund.
- **Rationale**: Clarification outcome (Option C). Exact tiers configurable in code/config.
- **Alternatives considered**: Full refund only, fixed %, or credit-only; pro-rata chosen per clarify.

## 7. Admin entry (same app, /admin, no login)

- **Decision**: Single React app with an admin entry (e.g. route `/admin` or "Admin" link). No login; anyone with the link can mark no-show (demo trust).
- **Rationale**: Clarification outcome (Option B). Keeps one codebase and no auth.
- **Alternatives considered**: No admin UI (API only), shared secret, or defer no-show; in-app admin route chosen.
