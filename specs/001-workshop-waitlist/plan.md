# Implementation Plan: Workshop SlotIn — Waitlist & Slot-Release

**Branch**: `001-workshop-waitlist` | **Date**: 2026-03-01 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-workshop-waitlist/spec.md`

## Summary

Implement a workshop sign-up web app with catalog, request-seat (confirm or waitlist), slot-released promotion with backend notification, cancellation with pro-rata refund rules, and admin no-show handling. Frontend (React/Vite/Tailwind) talks only to backend API; backend (FastAPI) owns workshops (persisted to JSON), bookings (in-memory), waitlist promotion, refund logic, and notification triggering. No auth; participant identity by email. Admin entry via `/admin` route (no login).

## Technical Context

**Language/Version**: Python 3.10+ (backend), Node 18+ (frontend build)  
**Primary Dependencies**: FastAPI, Pydantic v2 (backend); React, Vite, Tailwind CSS, Lucide React (frontend)  
**Storage**: Workshops → local JSON file(s); Bookings → in-memory (Python dict/list). No external DB.  
**Testing**: pytest (backend unit tests for capacity, waitlist, refund logic); frontend tests optional per constitution.  
**Target Platform**: Local/dev server (backend and frontend); browser for UI.  
**Project Type**: Web application (frontend + backend).  
**Performance Goals**: Demo-scale; no strict latency/throughput targets.  
**Constraints**: No Redux; React Context + local state only. No external API calls from frontend. All notifications via backend.  
**Scale/Scope**: Single server, in-memory bookings; workshop list and counts visible to all users.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Frontend: React (Vite), Tailwind, Lucide | ✓ | Plan uses React + Vite + Tailwind. |
| Backend: Python 3.10+, FastAPI | ✓ | Plan uses FastAPI. |
| Persistence: in-memory or local JSON only | ✓ | Workshops → JSON; bookings → in-memory. |
| No external DB (MongoDB, PostgreSQL, SQLite) | ✓ | Not used. |
| Separation of concerns: frontend never calls 3rd party APIs | ✓ | All notifications and external integrations via backend. |
| Frontend only reads/updates via backend API | ✓ | All data flows through backend API. |
| No authentication / no user accounts | ✓ | Email-only identity; no JWT/OAuth/sessions. |
| No Redux; useState + useContext | ✓ | Plan assumes React Context + local state. |
| No class components; hooks only | ✓ | React hooks only. |
| No manual styling; Tailwind only | ✓ | Tailwind utility classes only. |
| Secrets from .env; never commit | ✓ | API keys (e.g. email) from .env. |
| Pydantic for request validation | ✓ | Backend uses Pydantic for payloads. |
| Unit tests for workshop/waitlist/refund logic (pytest) | ✓ | Backend tests in scope. |

**Result**: All gates pass. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-workshop-waitlist/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1 (API contract)
└── tasks.md             # Phase 2 (/speckit.tasks - not created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app, routes
├── services.py          # Workshop, booking, waitlist, refund logic
├── models.py            # Pydantic models (if not inline)
├── workshops.json       # Persisted workshops (or path in config)
└── tests/
    └── test_services.py # Unit tests (capacity, waitlist, refund)

frontend/
├── src/
│   ├── App.tsx (or .jsx)
│   ├── main.tsx
│   ├── components/      # Workshop list, request seat form, my bookings, admin
│   ├── pages/           # Home, Admin (e.g. /admin)
│   ├── services/        # API client (calls backend only)
│   └── context/         # React Context for app state
├── package.json
├── vite.config.*
└── tailwind.config.*
```

**Structure Decision**: Web application with separate `backend/` and `frontend/` directories. Backend holds all business logic and persistence; frontend is a thin client that calls the backend API only.

## Complexity Tracking

Not applicable; no constitution violations to justify.
