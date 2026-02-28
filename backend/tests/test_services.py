# Workshop SlotIn — Unit tests for capacity, waitlist, refund logic (specs/001-workshop-waitlist)
# Full tests in Phase 8 (T029). This is the test layout placeholder.
import pytest

from services import load_workshops, add_booking, get_bookings_by_email


def test_load_workshops_returns_list():
    """Placeholder: load_workshops returns a list (empty or from file)."""
    result = load_workshops()
    assert isinstance(result, list)


def test_add_booking_and_get_by_email():
    """Placeholder: add_booking creates a booking; get_bookings_by_email returns it."""
    # Use a unique email to avoid affecting other tests
    email = "test-placeholder@example.com"
    b = add_booking("ws-001", email, "confirmed", position=None)
    assert b["id"]
    assert b["email"] == email
    assert b["state"] == "confirmed"
    found = get_bookings_by_email(email)
    assert any(x["id"] == b["id"] for x in found)
