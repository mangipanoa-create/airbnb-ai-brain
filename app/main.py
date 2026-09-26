from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Guest, Listing, Message, WorkOrder
from app.schemas import (
    BookingCreate,
    BookingRead,
    ContractorCreate,
    ContractorRead,
    GuestCreate,
    GuestRead,
    ListingCreate,
    ListingRead,
    MessageCreate,
    MessageRead,
    TriageMessageRequest,
    TriageMessageResponse,
    WorkOrderCreate,
    WorkOrderRead,
)
from app.services.ai_brain import AirbnbAIBrain

router = APIRouter()
brain = AirbnbAIBrain()


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "airbnb-ai-brain"}


@router.post("/listings", response_model=ListingRead)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    listing = Listing(**payload.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.post("/guests", response_model=GuestRead)
def create_guest(payload: GuestCreate, db: Session = Depends(get_db)):
    guest = Guest(**payload.model_dump())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


@router.post("/bookings", response_model=BookingRead)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.post("/messages", response_model=MessageRead)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    message = Message(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)

    guest = db.get(Guest, payload.guest_id) if payload.guest_id else None
    booking = db.get(Booking, payload.booking_id) if payload.booking_id else None
    listing = db.get(Listing, booking.listing_id) if booking else None

    triage = brain.triage_message(
        message=payload.content,
        guest_name=guest.full_name if guest else None,
        listing_name=listing.title if listing else None,
    )

    message.intent = str(triage["intent"])
    message.urgency = str(triage["urgency"])
    db.commit()
    db.refresh(message)

    if triage["requires_work_order"]:
        work_order_payload = WorkOrderCreate(
            listing_id=(booking.listing_id if booking else ""),
            booking_id=payload.booking_id,
            guest_id=payload.guest_id,
            issue_type=str(triage["intent"]),
            issue_summary=payload.content,
            priority="high" if triage["urgency"] == "high" else "medium",
            status="open",
        )

        if work_order_payload.listing_id:
            work_order = WorkOrder(**work_order_payload.model_dump())
            db.add(work_order)
            db.commit()

    return message


@router.post("/triage", response_model=TriageMessageResponse)
def triage_message(payload: TriageMessageRequest):
    triage = brain.triage_message(payload.message, payload.guest_name, payload.listing_name)
    return TriageMessageResponse(
        intent=str(triage["intent"]),
        urgency=str(triage["urgency"]),
        response=str(triage["response"]),
        requires_work_order=bool(triage["requires_work_order"]),
    )


@router.get("/messages")
def list_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()


@router.get("/work-orders")
def list_work_orders(db: Session = Depends(get_db)):
    return db.query(WorkOrder).all()
