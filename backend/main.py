# Workshop SlotIn — FastAPI app and routes (specs/001-workshop-waitlist)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import get_bookings_by_workshop, load_workshops

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
