# Backend API Contract: Workshop SlotIn

**Branch**: `001-workshop-waitlist` | **Date**: 2026-03-01

The frontend SHALL only communicate with the backend via these endpoints. All request/response bodies are JSON. Pydantic used for validation on backend.

**Base URL**: e.g. `http://localhost:8000` (configurable; frontend uses env or config).

---

## Endpoints

### 1. List workshops

- **Method**: `GET`
- **Path**: `/workshops` (or `/api/workshops`)
- **Response**: `200 OK`
- **Body**: Array of workshop objects.

```json
[
  {
    "id": "string",
    "title": "string",
    "date_time": "ISO8601",
    "capacity": "integer",
    "confirmed_count": "integer",
    "waitlisted_count": "integer"
  }
]
```

- **Rules**: `confirmed_count` ≤ `capacity`; counts are derived from current bookings.

---

### 2. Request a seat

- **Method**: `POST`
- **Path**: `/workshops/{workshop_id}/request-seat` (or `/api/workshops/{workshop_id}/request-seat`)
- **Request body**:

```json
{
  "email": "user@example.com"
}
```

- **Validation**: `email` required, valid format.
- **Response**:
  - **201 Created** — Seat confirmed. Body e.g. `{ "booking_id": "...", "state": "confirmed", "workshop_id": "...", "email": "..." }`.
  - **202 Accepted** — Added to waitlist. Body e.g. `{ "booking_id": "...", "state": "waitlisted", "position": 1, "workshop_id": "...", "email": "..." }`.
- **Error**: **400** (e.g. invalid email), **404** (workshop not found), **409** (e.g. already has a booking for this workshop — optional business rule).

- **Concurrency**: First request accepted by server wins when contesting the last seat; other returns 202 with waitlist position.

---

### 3. Cancel booking

- **Method**: `POST` or `DELETE`
- **Path**: `/bookings/{booking_id}/cancel` (or `/api/bookings/{booking_id}/cancel`). Alternatively cancel by workshop + email: e.g. `POST /workshops/{workshop_id}/cancel` with body `{ "email": "..." }`.
- **Request body** (if required): `{ "email": "..." }` when cancel is keyed by workshop + email.
- **Response**: **200 OK** — Cancellation recorded. Body may include refund info when within refund window (e.g. `{ "refund_percentage": 100 }` or pro-rata value).
- **Side effect**: If was confirmed and waitlist non-empty, backend promotes first waitlisted and triggers "slot released" notification (backend-only).

---

### 4. My bookings

- **Method**: `GET`
- **Path**: `/bookings?email=user@example.com` (or `/api/bookings?email=...`)
- **Query**: `email` (required) — participant email.
- **Response**: `200 OK` — Array of booking objects for that email.

```json
[
  {
    "id": "string",
    "workshop_id": "string",
    "email": "string",
    "state": "confirmed" | "waitlisted" | "cancelled" | "no_show",
    "position": "integer | null",
    "workshop_title": "string",
    "workshop_date_time": "ISO8601"
  }
]
```

- **Rules**: Only bookings for the given email; include workshop summary for display.

---

### 5. Mark no-show (admin)

- **Method**: `POST`
- **Path**: `/admin/bookings/{booking_id}/no-show` (or `/api/admin/bookings/{booking_id}/no-show`)
- **Request body**: Optional `{}` or empty.
- **Response**: **200 OK** — No-show recorded. No seat freed; no waitlist promotion.
- **Note**: No auth; demo trust. Frontend admin page at `/admin` calls this endpoint.

---

### 6. (Optional) Get workshop by ID

- **Method**: `GET`
- **Path**: `/workshops/{workshop_id}`
- **Response**: `200 OK` — Single workshop object (same shape as list item); **404** if not found.

---

## Error responses

- **400 Bad Request**: Validation error (e.g. invalid email). Body: `{ "detail": "..." }` or Pydantic-style errors.
- **404 Not Found**: Workshop or booking not found.
- **409 Conflict**: Optional; e.g. duplicate request for same workshop + email when already confirmed/waitlisted.

---

## Notification (backend-only)

- "Slot released" notification is triggered by the backend when a confirmed booking is cancelled and the waitlist is non-empty (after promoting the first waitlisted). Contract for the notification delivery (email, etc.) is out of scope for this API; the backend SHALL NOT expose notification APIs to the frontend.
