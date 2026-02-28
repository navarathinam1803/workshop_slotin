# Feature Specification: Workshop SlotIn — Waitlist & Slot-Release

**Feature Branch**: `001-workshop-waitlist`  
**Created**: 2026-03-01  
**Status**: Draft  
**Input**: User description: "Workshop SlotIn is a workshop sign-up app with waitlist and slot-release behavior. Workshop catalog; sign-up & waitlist; slot released; cancellation & refund; no-show; notifications backend only. Constraints: No Redux, no auth, in-memory or JSON, frontend API only."

## Clarifications

### Session 2026-03-01

- Q: How should the app identify a participant without authentication (for "my bookings" and waitlist position)? → A: Email (no password). User enters email to request a seat; backend links bookings to that email. No login, but we store contact info for notifications.
- Q: When two users request the last available seat at the same time, how should the system decide who gets the seat? → A: First request accepted by server wins. Whichever request the backend processes first gets the seat; the other is added to the waitlist.
- Q: When a user cancels within the refund window, should the refund be full or partial? → A: Pro-rata by time. Refund amount depends on how far in advance they cancel (e.g. 7 days = full refund, 3 days = 50%).
- Q: How should the system distinguish an admin for the no-show action without authentication? → A: Same app, admin route/link only (e.g. /admin or "Admin" link). No login; anyone who opens the admin entry can mark no-show (demo trust).
- Q: Should workshop and booking data survive a backend server restart? → A: Hybrid. Workshops are persisted (e.g. local JSON/file); bookings can be in-memory only.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse Workshops & See Availability (Priority: P1)

A user opens the app and sees a list of workshops. Each workshop shows title, date/time, capacity, and current counts of confirmed participants and waitlisted users. The user can assess availability at a glance.

**Why this priority**: Without a visible catalog and capacity, no sign-up or waitlist flow is possible.

**Independent Test**: Can be fully tested by loading the app and verifying workshop list with correct capacity and counts; delivers the foundation for all other flows.

**Acceptance Scenarios**:

1. **Given** the app is loaded, **When** the user views the workshop list, **Then** each workshop displays title, date/time, capacity, number of confirmed participants, and number of waitlisted users.
2. **Given** a workshop exists with a defined capacity, **When** the user views it, **Then** the system displays counts that never exceed capacity (confirmed ≤ capacity).

---

### User Story 2 - Request a Seat (Confirm or Join Waitlist) (Priority: P2)

A user selects a workshop and requests a seat. If capacity is available, the booking is confirmed. If the workshop is full, the user is added to the waitlist and sees their position. While on the waitlist, the user can see their position and workshop details.

**Why this priority**: Core value of the product—converting interest into either a confirmed seat or a waitlist place.

**Independent Test**: Can be tested by requesting a seat when capacity exists (expect confirmed) and when full (expect waitlist with position); verifies sign-up and waitlist behavior in isolation.

**Acceptance Scenarios**:

1. **Given** a workshop has available capacity, **When** the user requests a seat, **Then** the user is confirmed and the confirmed count increases by one.
2. **Given** a workshop is at capacity, **When** the user requests a seat, **Then** the user is added to the waitlist and sees their waitlist position and workshop details.
3. **Given** the user is on the waitlist, **When** they view their bookings, **Then** the system shows their position and the workshop details.

---

### User Story 3 - Slot Released (Cancel → Promote Waitlist & Notify) (Priority: P3)

When a confirmed participant cancels, if the waitlist is non-empty the first waitlisted user is promoted to confirmed and receives a "slot released" notification (sent by the backend). If the waitlist is empty, the seat is freed for new sign-ups.

**Why this priority**: Fulfills the promise of the waitlist and keeps the system fair and transparent.

**Independent Test**: Can be tested by cancelling a confirmed booking when waitlist has one or more users (expect first promoted and notification triggered via backend) and when waitlist is empty (expect seat available for new requests).

**Acceptance Scenarios**:

1. **Given** a confirmed participant cancels and the waitlist is non-empty, **When** the cancellation is processed, **Then** the first waitlisted user is promoted to confirmed and the backend triggers a "slot released" notification.
2. **Given** a confirmed participant cancels and the waitlist is empty, **When** the cancellation is processed, **Then** the seat is freed and available for new sign-ups.
3. **Given** a user was first on the waitlist, **When** they are promoted after a cancellation, **Then** they see their status as confirmed and (per backend) receive the notification.

---

### User Story 4 - Cancellation & Refund Rules (Priority: P4)

A user may cancel a confirmed booking. If they cancel within the refund window (e.g. ≥24 hours before workshop start), the system processes a refund per policy. If they cancel after the refund window (last-minute), no refund is granted—only the cancellation is recorded.

**Why this priority**: Clarifies business rules and sets user expectations; can be implemented after core booking and waitlist work.

**Independent Test**: Can be tested by cancelling inside the refund window (expect refund path) and inside the last-minute window (expect no refund, cancellation recorded).

**Acceptance Scenarios**:

1. **Given** the user cancels at least 24 hours before workshop start, **When** cancellation is submitted, **Then** the system processes the refund per policy and records the cancellation.
2. **Given** the user cancels less than 24 hours before workshop start, **When** cancellation is submitted, **Then** the system records the cancellation and does not grant a refund.
3. **Given** the refund window is defined in the spec (e.g. 24h before start), **When** the system evaluates a cancellation, **Then** it uses this definition consistently.

---

### User Story 5 - No-Show Handling (Priority: P5)

An admin can mark a confirmed participant as no-show via a separate admin entry in the same app (e.g. `/admin` or "Admin" link). No login; access is implicit trust for the demo. The system records the no-show and does not free the seat for waitlist promotion (the slot was consumed). Optional: admin action triggers internal reporting via backend.

**Why this priority**: Operational clarity and reporting; does not block core sign-up or waitlist flows.

**Independent Test**: Can be tested by marking a confirmed participant as no-show and verifying the record exists and no waitlist promotion occurs.

**Acceptance Scenarios**:

1. **Given** a confirmed participant did not attend, **When** a user opens the admin entry (e.g. /admin) and marks them as no-show, **Then** the system records the no-show and does not promote from the waitlist or free the seat for new sign-ups.
2. **Given** a no-show is recorded, **When** reporting or analytics are requested, **Then** the backend may include this in internal reporting (optional).

---

### Edge Cases

- What happens when two users request the last available seat at the same time? (First request accepted by the server wins; that user is confirmed and the other is added to the waitlist.)
- What happens when the only confirmed user cancels and the waitlist has multiple users? (First waitlisted is promoted; others remain in order.)
- How does the system handle cancellation exactly at the refund-window boundary (e.g. exactly 24h before)? (Define as inclusive: ≥24h qualifies for refund.)
- What if a promoted waitlist user’s notification fails? (Backend handles retry/error; user still has confirmed status in the system.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system SHALL list workshops with title, date/time, capacity, current confirmed count, and current waitlisted count.
- **FR-002**: The system SHALL enforce a maximum capacity per workshop (confirmed participants shall not exceed capacity).
- **FR-003**: WHEN a user requests a seat (supplying a valid email) and capacity is available, THE system SHALL confirm the booking, associate it with that email, and increment the confirmed count.
- **FR-004**: WHEN a user requests a seat (supplying a valid email) and the workshop is full, THE system SHALL add the user to the waitlist keyed by that email and return their position and workshop details.
- **FR-005**: WHILE a user is on the waitlist, THE system SHALL display their position and workshop details when they view their bookings.
- **FR-006**: WHEN a confirmed participant cancels and the waitlist is non-empty, THE system SHALL promote the first waitlisted user to confirmed and trigger a "slot released" notification via the backend only.
- **FR-007**: WHEN a confirmed participant cancels and the waitlist is empty, THE system SHALL free the seat so it is available for new sign-ups.
- **FR-008**: IF a user cancels within the refund window (at least 24 hours before workshop start), THE system SHALL process a refund on a pro-rata-by-time basis (e.g. 7 days before = full refund, 3 days before = 50%) and record the cancellation.
- **FR-009**: IF a user cancels less than 24 hours before the workshop start time (last-minute), THE system SHALL record the cancellation and SHALL NOT grant a refund.
- **FR-010**: IF a confirmed participant is marked no-show (via the in-app admin entry, e.g. /admin, no login), THE system SHALL record the no-show and SHALL NOT free the seat for waitlist promotion.
- **FR-011**: All email, calendar, or other notifications SHALL be sent by the backend only; the frontend SHALL NOT call external notification APIs.
- **FR-012**: The frontend SHALL only read and update data via the backend API (list workshops, request seat with email, cancel, view my bookings by email and waitlist position).

### Key Entities

- **Workshop**: Represents a single workshop event; attributes include title, date/time, capacity, and derived counts (confirmed, waitlisted). Identified by a stable ID. Persisted to disk (e.g. local JSON); survives server restart.
- **Booking (registration)**: A user’s request for a seat; keyed by participant email (no password/login). Can be in state confirmed, waitlisted, cancelled, or no-show. For waitlisted, position is stored. Backend uses email to link bookings and to send notifications. May be in-memory only (data lost on server restart).
- **Refund window**: At least 24 hours before workshop start. Cancellations within this window receive a pro-rata refund (e.g. 7 days before = full, 3 days before = 50%). Cancellations inside the last 24 hours (last-minute) receive no refund.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can see all workshops and their availability (capacity and counts) in one view.
- **SC-002**: Users can request a seat and receive either a confirmation or a waitlist position with clear visibility of that position.
- **SC-003**: When a slot is freed by cancellation, the first waitlisted user is promoted and notified (via backend) without manual intervention.
- **SC-004**: Cancellation and refund behavior are consistent with the defined refund window (e.g. 24h) and last-minute rule.
- **SC-005**: No-show is recorded without incorrectly freeing the seat or promoting from the waitlist.

## Assumptions

- **Refund window** is 24 hours before the workshop’s scheduled start time. Refunds within the window are pro-rata by time (e.g. 7 days before = full, 3 days before = 50%); exact tiers are configurable.
- **Participant identity**: participants are identified by email only (no password or login). User enters email when requesting a seat; backend links all bookings and notifications to that email; "my bookings" is retrieved by supplying the same email.
- **Single promoter per cancellation**: when one seat frees, exactly one waitlisted user is promoted (first in order).
- Notifications are "triggered" by the backend; actual delivery mechanism (email, etc.) is out of scope for MVP but must not be implemented in the frontend.
- **Persistence (hybrid)**: Workshop data is persisted to disk (e.g. local JSON or file) and survives server restart. Booking data may be in-memory only and is lost on restart.
