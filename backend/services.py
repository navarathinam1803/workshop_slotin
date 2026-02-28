# Workshop SlotIn — Workshop, booking, waitlist, refund logic (specs/001-workshop-waitlist)
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

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
