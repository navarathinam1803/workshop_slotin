# Workshop SlotIn — Pydantic models (specs/001-workshop-waitlist)
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class BookingState(str, Enum):
    CONFIRMED = "confirmed"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


# --- Workshop (persisted to JSON) ---
class WorkshopBase(BaseModel):
    title: str
    date_time: datetime
    capacity: int = Field(..., gt=0, description="Max confirmed participants")


class WorkshopCreate(WorkshopBase):
    pass


class WorkshopIn(WorkshopBase):
    id: str


class WorkshopOut(WorkshopBase):
    id: str
    confirmed_count: int = 0
    waitlisted_count: int = 0

    class Config:
        from_attributes = True


# --- Booking (in-memory) ---
class BookingBase(BaseModel):
    workshop_id: str
    email: EmailStr
    state: BookingState
    position: Optional[int] = None  # 1-based when state is waitlisted


class BookingCreate(BaseModel):
    workshop_id: str
    email: EmailStr


class BookingOut(BookingBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Request/response DTOs for API ---
class RequestSeatRequest(BaseModel):
    email: EmailStr


class RequestSeatResponse(BaseModel):
    booking_id: str
    state: BookingState
    workshop_id: str
    email: str
    position: Optional[int] = None
