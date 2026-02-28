/**
 * Workshop SlotIn — API client (frontend only calls backend; no 3rd party APIs)
 * Base URL: VITE_API_URL or http://localhost:8000
 */
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function getWorkshops() {
  const res = await fetch(`${API_BASE}/workshops`);
  if (!res.ok) throw new Error(`Workshops: ${res.status}`);
  return res.json();
}

export async function requestSeat(workshopId, email) {
  const res = await fetch(`${API_BASE}/workshops/${workshopId}/request-seat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request seat: ${res.status}`);
  }
  return res.json();
}

export async function getMyBookings(email) {
  const params = new URLSearchParams({ email });
  const res = await fetch(`${API_BASE}/bookings?${params}`);
  if (!res.ok) throw new Error(`My bookings: ${res.status}`);
  return res.json();
}
