# Workshop SlotIn — FastAPI app and routes (specs/001-workshop-waitlist)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import RequestSeatRequest
from services import get_bookings_by_workshop, load_workshops, request_seat

app = FastAPI(
    title="Workshop SlotIn API",
    description="Workshop sign-up with waitlist and slot-release",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health check for deployment and load balancers."""
    return {"status": "ok"}


@app.get("/workshops")
def list_workshops():
    """Return all workshops with confirmed_count and waitlisted_count derived from bookings."""
    workshops = load_workshops()
    result = []
    for ws in workshops:
        wid = ws.get("id", "")
        bookings = get_bookings_by_workshop(wid)
        confirmed_count = sum(1 for b in bookings if b.get("state") == "confirmed")
        waitlisted_count = sum(1 for b in bookings if b.get("state") == "waitlisted")
        result.append({
            "id": wid,
            "title": ws.get("title", ""),
            "date_time": ws.get("date_time"),
            "capacity": ws.get("capacity", 0),
            "confirmed_count": confirmed_count,
            "waitlisted_count": waitlisted_count,
        })
    return result


@app.post("/workshops/{workshop_id}/request-seat")
def request_seat_endpoint(workshop_id: str, body: RequestSeatRequest):
    """Request a seat: 201 confirmed, 202 waitlisted; 404 workshop not found, 409 already booked."""
    booking, outcome = request_seat(workshop_id, body.email)
    if outcome == "not_found":
        raise HTTPException(status_code=404, detail="Workshop not found")
    if outcome == "already_booked":
        raise HTTPException(status_code=409, detail="Already have a booking for this workshop")
    status = 201 if outcome == "confirmed" else 202
    content = {
        "booking_id": booking["id"],
        "state": booking["state"],
        "workshop_id": booking["workshop_id"],
        "email": booking["email"],
        "position": booking.get("position"),
    }
    return JSONResponse(content=content, status_code=status)
