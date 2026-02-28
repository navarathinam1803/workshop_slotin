# Workshop SlotIn — Workshop, booking, waitlist, refund logic (specs/001-workshop-waitlist)
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Refund window: ≥24h before start = pro-rata; <24h = no refund. Pro-rata: 7 days = 100%, 3 days = 50%, 1 day = 0%.
REFUND_WINDOW_HOURS = 24
REFUND_FULL_DAYS = 7
REFUND_HALF_DAYS = 3

# Configurable path for workshops JSON (default: same dir as this file, workshops.json)
WORKSHOPS_JSON = os.environ.get("WORKSHOPS_JSON", str(Path(__file__).resolve().parent / "workshops.json"))

# In-memory bookings store (lost on server restart per spec)
_bookings: list[dict] = []


def add_booking(workshop_id: str, email: str, state: str, position: int | None = None) -> dict:
    """Append a booking to the in-memory store. Returns the created booking dict with id and created_at."""
    now = datetime.utcnow()
    booking = {
        "id": str(uuid.uuid4()),
        "workshop_id": workshop_id,
        "email": email,
        "state": state,
        "position": position,
        "created_at": now.isoformat(),
    }
    _bookings.append(booking)
    return booking


def get_booking_by_id(booking_id: str) -> dict | None:
    """Return booking by id or None."""
    for b in _bookings:
        if b["id"] == booking_id:
            return b
    return None


def get_bookings_by_email(email: str) -> list[dict]:
    """Return all bookings for the given email (any state)."""
    return [b for b in _bookings if b["email"] == email]


def get_bookings_by_workshop(workshop_id: str) -> list[dict]:
    """Return all bookings for the workshop (confirmed, waitlisted, cancelled, no_show)."""
    return [b for b in _bookings if b["workshop_id"] == workshop_id]


def update_booking_state(booking_id: str, state: str, position: int | None = None) -> dict | None:
    """Update a booking's state (and optional position). Returns updated booking or None."""
    for b in _bookings:
        if b["id"] == booking_id:
            b["state"] = state
            if position is not None:
                b["position"] = position
            return b
    return None


def request_seat(workshop_id: str, email: str) -> tuple[dict | None, str]:
    """
    Request a seat for the given workshop and email.
    First-request-wins: capacity checked in one logical step.
    Returns (booking_dict, outcome) where outcome is:
      "confirmed" | "waitlisted" | "not_found" | "already_booked"
    """
    workshops = load_workshops()
    workshop = next((w for w in workshops if w.get("id") == workshop_id), None)
    if not workshop:
        return None, "not_found"

    bookings = get_bookings_by_workshop(workshop_id)
    confirmed_count = sum(1 for b in bookings if b.get("state") == "confirmed")
    waitlisted = [b for b in bookings if b.get("state") == "waitlisted"]
    waitlisted.sort(key=lambda b: b.get("position") or 0)

    if any(b.get("email") == email and b.get("state") in ("confirmed", "waitlisted") for b in bookings):
        return None, "already_booked"

    capacity = workshop.get("capacity", 0)
    if confirmed_count < capacity:
        booking = add_booking(workshop_id, email, "confirmed", None)
        return booking, "confirmed"
    position = len(waitlisted) + 1
    booking = add_booking(workshop_id, email, "waitlisted", position)
    return booking, "waitlisted"


def trigger_slot_released_notification(workshop_id: str, promoted_booking: dict) -> None:
    """Stub: slot released after promoting first waitlisted. Backend-only; delivery out of scope."""
    # In a real system: send email, push, etc. For now no-op or log.
    pass


def cancel_booking(booking_id: str) -> tuple[dict | None, str, dict | None]:
    """
    Cancel a booking by id. If it was confirmed and the workshop has waitlisted users,
    promote the first waitlisted and trigger slot-released notification.
    Returns (cancelled_booking, outcome, promoted_booking_or_none).
    Outcome: "cancelled" | "not_found" | "invalid_state"
    """
    booking = get_booking_by_id(booking_id)
    if not booking:
        return None, "not_found", None
    if booking.get("state") not in ("confirmed", "waitlisted"):
        return None, "invalid_state", None

    workshop_id = booking["workshop_id"]
    was_confirmed = booking.get("state") == "confirmed"
    update_booking_state(booking_id, "cancelled", None)
    promoted = None

    if was_confirmed:
        waitlisted = [b for b in get_bookings_by_workshop(workshop_id) if b.get("state") == "waitlisted"]
        waitlisted.sort(key=lambda b: b.get("position") or 0)
        if waitlisted:
            first = waitlisted[0]
            update_booking_state(first["id"], "confirmed", None)
            promoted = first
            trigger_slot_released_notification(workshop_id, first)

    return booking, "cancelled", promoted


def mark_no_show(booking_id: str) -> tuple[dict | None, str]:
    """
    Mark a confirmed booking as no-show. No seat freed; no waitlist promotion.
    Returns (booking, outcome) where outcome is "ok" | "not_found" | "invalid_state".
    """
    booking = get_booking_by_id(booking_id)
    if not booking:
        return None, "not_found"
    if booking.get("state") != "confirmed":
        return None, "invalid_state"
    update_booking_state(booking_id, "no_show", None)
    return booking, "ok"


def load_workshops() -> list[dict]:
    """Load workshops from JSON file. Returns list of dicts (id, title, date_time, capacity)."""
    path = Path(WORKSHOPS_JSON)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_workshops(workshops: list[dict]) -> None:
    """Persist workshops to JSON file."""
    path = Path(WORKSHOPS_JSON)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(workshops, f, indent=2, default=str)


def _parse_workshop_start(date_time: str | None) -> datetime | None:
    """Parse workshop date_time (ISO string) to naive UTC datetime. Returns None if missing/invalid."""
    if not date_time:
        return None
    try:
        if isinstance(date_time, datetime):
            dt = date_time
        else:
            dt = datetime.fromisoformat(str(date_time).replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except (TypeError, ValueError):
        return None


def compute_refund(workshop_id: str) -> dict | None:
    """
    Compute refund for a cancellation now. ≥24h before start = pro-rata (e.g. 7 days = 100%, 3 days = 50%);
    <24h = no refund. Returns {"refund_percentage": int} or None when workshop not found / no date.
    """
    workshops = load_workshops()
    workshop = next((w for w in workshops if w.get("id") == workshop_id), None)
    if not workshop:
        return None
    start = _parse_workshop_start(workshop.get("date_time"))
    if not start:
        return None
    now = datetime.utcnow()
    hours_until = (start - now).total_seconds() / 3600
    if hours_until < REFUND_WINDOW_HOURS:
        return {"refund_percentage": 0}
    days_until = hours_until / 24
    if days_until >= REFUND_FULL_DAYS:
        return {"refund_percentage": 100}
    if days_until >= REFUND_HALF_DAYS:
        pct = 50 + (days_until - REFUND_HALF_DAYS) / (REFUND_FULL_DAYS - REFUND_HALF_DAYS) * 50
        return {"refund_percentage": round(min(100, max(0, pct)))}
    if days_until >= 1:
        pct = (days_until - 1) / (REFUND_HALF_DAYS - 1) * 50
        return {"refund_percentage": round(min(50, max(0, pct)))}
    return {"refund_percentage": 0}
