# Data Model: 001-workshop-waitlist

**Branch**: `001-workshop-waitlist` | **Date**: 2026-03-01

Entities and rules derived from [spec.md](./spec.md) and clarifications.

## Entities

### Workshop

- **Purpose**: A single workshop event; persisted to disk; survives server restart.
- **Attributes**:
  - `id`: Stable unique identifier (e.g. string or UUID).
  - `title`: string.
  - `date_time`: ISO 8601 or equivalent (date and time of workshop start).
  - `capacity`: positive integer (max confirmed participants).
  - Derived / computed: `confirmed_count`, `waitlisted_count` (from bookings).
- **Validation**: capacity > 0; confirmed_count ≤ capacity.
- **Persistence**: Stored in local JSON file (e.g. `workshops.json` or one file per workshop). Loaded at startup; written on create/update.

### Booking (registration)

- **Purpose**: A participant’s request for a seat; keyed by email; state can be confirmed, waitlisted, cancelled, or no-show.
- **Attributes**:
  - `id`: Unique identifier (e.g. UUID).
  - `workshop_id`: Reference to Workshop.
  - `email`: string (participant identity; no password).
  - `state`: enum — `confirmed` | `waitlisted` | `cancelled` | `no_show`.
  - `position`: integer, optional (waitlist position, 1-based; only when state = waitlisted).
  - `created_at`: timestamp (for ordering / first-request-wins).
- **Uniqueness**: One active booking per (workshop_id, email) per workshop — e.g. one confirmed or one waitlisted per email per workshop; cancelled/no_show may be retained for history.
- **Persistence**: In-memory only (e.g. list or dict); lost on server restart.

### Refund window (policy, not stored entity)

- **Rule**: Cancellation at least 24 hours before workshop start → eligible for pro-rata refund (e.g. 7 days = full, 3 days = 50%). Less than 24 hours → no refund.
- **Implementation**: Computed from workshop `date_time` and cancellation time; refund tiers can be config (e.g. list of (days_before, percentage)).

## State transitions (Booking)

- **Request seat**:
  - If workshop has capacity → create Booking with `state = confirmed`.
  - If workshop full → create Booking with `state = waitlisted`, assign `position` (next in line).
- **Cancel (confirmed)**:
  - Set Booking `state = cancelled`. If waitlist non-empty, promote first waitlisted to `confirmed`, trigger "slot released" notification (backend). If waitlist empty, seat is free for new requests.
- **Cancel (waitlisted)**:
  - Set Booking `state = cancelled`; renumber positions of remaining waitlisted for that workshop.
- **Mark no-show (admin)**:
  - Set Booking `state = no_show`. Do not free seat; do not promote from waitlist.

## Relationships

- Workshop 1 — * N Booking: A workshop has many bookings (confirmed, waitlisted, cancelled, no_show).
- Booking N — 1 Workshop: Each booking belongs to one workshop.
- Bookings for "my bookings": Filter by `email` (and optionally `state` not in [cancelled] or include cancelled for history as needed).

## Concurrency (last seat)

- First request accepted by server wins. Implementation: when processing request-seat, check capacity and confirmed_count in a single logical step (e.g. one function that reads, decides, and writes); no need for distributed lock at demo scale.
