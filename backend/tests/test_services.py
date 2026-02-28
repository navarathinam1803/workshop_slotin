# Workshop SlotIn — Unit tests for capacity, waitlist promotion, refund logic (specs/001-workshop-waitlist)
import pytest
from datetime import datetime, timedelta

import services
from services import (
    add_booking,
    cancel_booking,
    compute_refund,
    get_bookings_by_email,
    get_bookings_by_workshop,
    load_workshops,
    request_seat,
    update_booking_state,
)


def _clear_bookings():
    """Reset in-memory bookings for test isolation."""
    services._bookings.clear()


# --- Existing placeholders (kept) ---


def test_load_workshops_returns_list():
    """load_workshops returns a list (empty or from file)."""
    result = load_workshops()
    assert isinstance(result, list)


def test_add_booking_and_get_by_email():
    """add_booking creates a booking; get_bookings_by_email returns it."""
    _clear_bookings()
    email = "test-placeholder@example.com"
    b = add_booking("ws-001", email, "confirmed", position=None)
    assert b["id"]
    assert b["email"] == email
    assert b["state"] == "confirmed"
    found = get_bookings_by_email(email)
    assert any(x["id"] == b["id"] for x in found)


# --- T029: Workshop capacity ---


def test_request_seat_confirmed_when_capacity_available(monkeypatch):
    """When confirmed_count < capacity, request_seat returns confirmed."""
    _clear_bookings()
    workshops = [
        {"id": "ws-cap", "title": "Cap", "date_time": "2026-06-01T10:00:00", "capacity": 2},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    booking, outcome = request_seat("ws-cap", "a@test.com")
    assert outcome == "confirmed"
    assert booking["state"] == "confirmed"
    assert booking["email"] == "a@test.com"


def test_request_seat_waitlisted_when_at_capacity(monkeypatch):
    """When confirmed_count >= capacity, request_seat returns waitlisted with position."""
    _clear_bookings()
    workshops = [
        {"id": "ws-full", "title": "Full", "date_time": "2026-06-01T10:00:00", "capacity": 2},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    add_booking("ws-full", "first@test.com", "confirmed", None)
    add_booking("ws-full", "second@test.com", "confirmed", None)
    booking, outcome = request_seat("ws-full", "third@test.com")
    assert outcome == "waitlisted"
    assert booking["state"] == "waitlisted"
    assert booking["position"] == 1


def test_request_seat_not_found_when_workshop_missing(monkeypatch):
    """When workshop id does not exist, request_seat returns not_found."""
    _clear_bookings()
    monkeypatch.setattr(services, "load_workshops", lambda: [])
    booking, outcome = request_seat("nonexistent", "a@test.com")
    assert outcome == "not_found"
    assert booking is None


def test_request_seat_already_booked_when_same_email_has_booking(monkeypatch):
    """When email already has confirmed/waitlisted for workshop, request_seat returns already_booked."""
    _clear_bookings()
    workshops = [
        {"id": "ws-1", "title": "One", "date_time": "2026-06-01T10:00:00", "capacity": 5},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    add_booking("ws-1", "same@test.com", "confirmed", None)
    booking, outcome = request_seat("ws-1", "same@test.com")
    assert outcome == "already_booked"
    assert booking is None


# --- T029: Waitlist promotion (cancel) ---


def test_cancel_booking_promotes_first_waitlisted(monkeypatch):
    """When confirmed is cancelled and waitlist non-empty, first waitlisted becomes confirmed."""
    _clear_bookings()
    workshops = [
        {"id": "ws-promo", "title": "Promo", "date_time": "2026-06-01T10:00:00", "capacity": 1},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    conf = add_booking("ws-promo", "confirmed@test.com", "confirmed", None)
    wl = add_booking("ws-promo", "waitlisted@test.com", "waitlisted", 1)
    cancelled, outcome, promoted = cancel_booking(conf["id"])
    assert outcome == "cancelled"
    assert promoted is not None
    assert promoted["id"] == wl["id"]
    assert promoted["state"] == "confirmed"
    # State in store is updated via update_booking_state
    wl_after = next(b for b in get_bookings_by_workshop("ws-promo") if b["id"] == wl["id"])
    assert wl_after["state"] == "confirmed"


def test_cancel_booking_no_promotion_when_waitlist_empty(monkeypatch):
    """When confirmed is cancelled and waitlist empty, no promoted booking."""
    _clear_bookings()
    conf = add_booking("ws-any", "only@test.com", "confirmed", None)
    cancelled, outcome, promoted = cancel_booking(conf["id"])
    assert outcome == "cancelled"
    assert promoted is None


def test_cancel_booking_not_found():
    """Cancel returns not_found for unknown booking id."""
    _clear_bookings()
    cancelled, outcome, promoted = cancel_booking("nonexistent-id")
    assert outcome == "not_found"
    assert cancelled is None


# --- T029: Refund window ---


def test_compute_refund_zero_when_less_than_24h_before_start(monkeypatch):
    """When <24h before workshop start, refund_percentage is 0."""
    now = datetime(2026, 6, 1, 8, 0, 0)  # 8:00
    start = datetime(2026, 6, 1, 20, 0, 0)  # 20:00 same day -> 12h later
    workshops = [
        {"id": "ws-norefund", "title": "NoRefund", "date_time": start.isoformat(), "capacity": 5},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    result = compute_refund("ws-norefund", now=now)
    assert result is not None
    assert result["refund_percentage"] == 0


def test_compute_refund_pro_rata_when_4_days_before(monkeypatch):
    """When ~4 days before start (between 3 and 7), refund is between 50 and 100%."""
    now = datetime(2026, 6, 1, 12, 0, 0)
    start = now + timedelta(days=4)
    workshops = [
        {"id": "ws-prorata", "title": "ProRata", "date_time": start.isoformat(), "capacity": 5},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    result = compute_refund("ws-prorata", now=now)
    assert result is not None
    assert 50 <= result["refund_percentage"] <= 100


def test_compute_refund_full_when_7_or_more_days_before(monkeypatch):
    """When >=7 days before start, refund is 100%."""
    now = datetime(2026, 6, 1, 12, 0, 0)
    start = now + timedelta(days=8)
    workshops = [
        {"id": "ws-fullrefund", "title": "Full", "date_time": start.isoformat(), "capacity": 5},
    ]
    monkeypatch.setattr(services, "load_workshops", lambda: workshops)
    result = compute_refund("ws-fullrefund", now=now)
    assert result is not None
    assert result["refund_percentage"] == 100


def test_compute_refund_none_when_workshop_not_found(monkeypatch):
    """When workshop id not in list, compute_refund returns None."""
    monkeypatch.setattr(services, "load_workshops", lambda: [])
    result = compute_refund("missing")
    assert result is None
