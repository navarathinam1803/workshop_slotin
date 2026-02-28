# Workshop SlotIn

Workshop sign-up app with waitlist and slot-release: browse workshops, request a seat (confirmed or waitlisted), view my bookings, cancel with refund rules, and admin no-show handling.

**Branch**: `001-workshop-waitlist`

## Tech stack

- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn. Workshops in JSON; bookings in-memory.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React. No Redux; identity by email only.
- **Tests**: pytest (backend unit tests for capacity, waitlist promotion, refund logic).

## Prerequisites

- Python 3.10+
- Node 18+ and npm (or pnpm/yarn)

## Quick start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

API: **http://localhost:8000** (health: http://localhost:8000/health)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: **http://localhost:5173**. Set `VITE_API_URL=http://localhost:8000` if the backend runs elsewhere.

### Optional

- Copy `backend/.env.example` to `backend/.env` for overrides (e.g. `WORKSHOPS_JSON`). See [backend/.env.example](backend/.env.example).

## Running tests

From `backend/`:

```bash
pytest tests/ -v
```

## Project structure

```
workshop_slotin/
├── backend/
│   ├── main.py          # FastAPI app, routes
│   ├── services.py      # Workshops, bookings, request-seat, cancel, refund, no-show
│   ├── models.py        # Pydantic models
│   ├── workshops.json   # Workshop data (persisted)
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/
│       └── test_services.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx     # Router: /, /admin
│   │   ├── components/  # WorkshopList, RequestSeatForm, MyBookings
│   │   ├── pages/       # Admin.jsx
│   │   └── services/    # api.js
│   └── package.json
├── specs/001-workshop-waitlist/
│   ├── spec.md
│   ├── quickstart.md    # Detailed run + manual test scenarios
│   ├── tasks.md
│   ├── contracts/
│   └── checklists/      # Phase validation checklists
└── README.md
```

## Features

- **Catalog**: Workshop list with title, date/time, capacity, confirmed and waitlisted counts.
- **Request seat**: Confirm when capacity available; waitlist with position when full. First-request-wins for the last seat.
- **My bookings**: Enter email to see bookings with state and (if waitlisted) position.
- **Cancel**: Cancel confirmed or waitlisted; if confirmed and waitlist non-empty, first waitlisted is promoted; “slot released” notification stub.
- **Refund**: Cancel ≥24h before start → pro-rata refund (e.g. 7 days = 100%, 3 days = 50%); &lt;24h → no refund.
- **Admin**: `/admin` — list confirmed bookings, mark no-show (no seat freed, no promotion).

## Specs and docs

- [Feature spec & user stories](specs/001-workshop-waitlist/spec.md)
- [Quickstart & manual test scenarios](specs/001-workshop-waitlist/quickstart.md)
- [Backend API contract](specs/001-workshop-waitlist/contracts/backend-api.md)
