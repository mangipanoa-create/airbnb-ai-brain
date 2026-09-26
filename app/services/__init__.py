from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ListingCreate(BaseModel):
    title: str
    address: str
    check_in_instructions: Optional[str] = None
    emergency_contact: Optional[str] = None


class ListingRead(ListingCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GuestCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None


class GuestRead(GuestCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    guest_id: str
    listing_id: str
    check_in: date
    check_out: date
    status: str = "confirmed"
    payment_status: str = "paid"
    notes: Optional[str] = None


class BookingRead(BookingCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    guest_id: Optional[str] = None
    booking_id: Optional[str] = None
    sender_type: str = "guest"
    channel: str = "sms"
    content: str


class MessageRead(MessageCreate):
    id: str
    intent: Optional[str] = None
    urgency: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContractorCreate(BaseModel):
    name: str
    service_type: str
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    status: str = "available"


class ContractorRead(ContractorCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkOrderCreate(BaseModel):
    listing_id: str
    booking_id: Optional[str] = None
    guest_id: Optional[str] = None
    contractor_id: Optional[str] = None
    issue_type: str
    issue_summary: str
    priority: str = "medium"
    status: str = "open"
    scheduled_at: Optional[datetime] = None


class WorkOrderRead(WorkOrderCreate):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TriageMessageRequest(BaseModel):
    guest_name: Optional[str] = None
    listing_name: Optional[str] = None
    message: str


class TriageMessageResponse(BaseModel):
    intent: str
    urgency: str
    response: str
    requires_work_order: bool
