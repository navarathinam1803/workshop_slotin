<!-- Project Constitution — The Workshop SlotIn -->

This document is the authoritative guide for architecture, security, development standards, and non-goals for "The Workshop SlotIn" repository. As a course demo project, clarity and simplicity are prioritized over enterprise scale.

## Table of contents

- Project Overview
- Core Tech Stack
- Architectural Principles
- Security & Integrity
- Development Standards
- Non-Goals & Constraints

---

## Project Overview

"The Workshop SlotIn" is a web application for workshop sign-up with waitlist and slot-release behavior. It features:

- **Workshop catalog** — list workshops with title, date/time, capacity, and current confirmed + waitlisted counts.
- **Sign-up & waitlist** — request a seat (confirmed when capacity allows; otherwise join waitlist with position).
- **Slot released** — when a confirmed participant cancels, the first waitlisted user is promoted and notified (via backend).
- **Cancellation & refund rules** — refund window (e.g. cancel ≥24h before start) vs no-refund (last-minute); no-show handling.
- **Notifications** — all email/calendar/notification sending is done by the backend only; the frontend never calls external notification APIs.

## Core Tech Stack

- **Frontend:** React (Vite) with Tailwind CSS and Lucide React icons.
- **Backend:** Python 3.10+ with FastAPI.
- **Persistence:** In-memory Python structures or simple local JSON files (no external database).
- **Validation:** Pydantic v2 for request/response and business rules.

## Architectural Principles

- **Separation of concerns:** The frontend must never call third-party APIs (email, calendar, SMS, etc.) directly. All notifications and external integrations are proxied through the backend.
- **Frontend as client:** The frontend only reads and updates data via the backend API (list workshops, request seat, cancel, view my bookings and waitlist position).
- **Simplicity over scale:** Keep backend logic consolidated (e.g. `main.py` for routes, `services.py` for workshop/waitlist/refund logic). Avoid unnecessary folder depth.

## Security & Integrity

- **No authentication:** The app is open and requires no login (demo-only constraint).
- **Secrets management:** Any API keys (e.g. for email or notifications) must be loaded from a `.env` file. Never commit secrets to the repository.
- **Input hygiene:** Use Pydantic to validate all request payloads (sign-up, cancel, admin actions) before applying business logic.

## Development Standards

- **Testing:** Provide unit tests for workshop capacity, waitlist promotion, and refund-window logic using `pytest`.
- **Formatting:** Use Prettier for frontend code and `black`/`ruff` for Python.
- **Documentation:** Include comments that explain why specific Spec-Kit commands were used (for educational purposes).

## Non-Goals & Constraints

- **No external databases:** Do not install or configure MongoDB, PostgreSQL, or SQLite; use in-memory or local JSON only.
- **No user accounts:** Do not implement JWT, OAuth, or session cookies.
- **No Redux:** Use React `useState` and `useContext` instead of Redux.
- **No class components:** Use React hooks only.
- **No manual styling:** All styles must use Tailwind utility classes.

---

**Version:** 1.0.0 (Demo Edition)  •  **Ratified:** 2026-01-09
