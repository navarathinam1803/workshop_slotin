# Workshop SlotIn — Workshop, booking, waitlist, refund logic (specs/001-workshop-waitlist)
import json
import os
from pathlib import Path

# Configurable path for workshops JSON (default: same dir as this file, workshops.json)
WORKSHOPS_JSON = os.environ.get("WORKSHOPS_JSON", str(Path(__file__).resolve().parent / "workshops.json"))


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
