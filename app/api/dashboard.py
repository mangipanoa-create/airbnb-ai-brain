from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Contractor, Guest, Listing, Message, WorkOrder
from app.services.dashboard import DashboardService

router = APIRouter()


def build_dashboard_context(db: Session) -> dict:
    summary = DashboardService.get_summary(db)
    return {
        "stats": summary["stats"],
        "recent_messages": summary["recent_messages"],
        "work_orders": summary["work_orders"],
        "contractors": summary["contractors"],
        "bookings": summary["bookings"],
    }


@router.get("/dashboard-data")
def dashboard_data(db: Session = Depends(get_db)):
    return DashboardService.get_summary(db)


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "airbnb-ai-brain"}


@router.get("/listings", response_model=list[dict])
def list_listings(db: Session = Depends(get_db)):
    listings = db.query(Listing).all()
    return [
        {
            "id": item.id,
            "title": item.title,
            "address": item.address,
            "status": "active",
        }
        for item in listings
    ]


@router.get("/guests", response_model=list[dict])
def list_guests(db: Session = Depends(get_db)):
    guests = db.query(Guest).all()
    return [
        {
            "id": g.id,
            "full_name": g.full_name,
            "email": g.email,
            "phone": g.phone,
        }
        for g in guests
    ]


@router.get("/bookings", response_model=list[dict])
def list_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return [
        {
            "id": b.id,
            "status": b.status,
            "check_in": b.check_in.isoformat(),
            "check_out": b.check_out.isoformat(),
            "payment_status": b.payment_status,
        }
        for b in bookings
    ]


@router.get("/messages", response_model=list[dict])
def list_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.created_at.desc()).all()
    return [
        {
            "id": m.id,
            "sender_type": m.sender_type,
            "content": m.content,
            "intent": m.intent,
            "urgency": m.urgency,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]


@router.get("/work-orders", response_model=list[dict])
def list_work_orders(db: Session = Depends(get_db)):
    work_orders = db.query(WorkOrder).order_by(WorkOrder.created_at.desc()).all()
    return [
        {
            "id": w.id,
            "issue_type": w.issue_type,
            "issue_summary": w.issue_summary,
            "priority": w.priority,
            "status": w.status,
            "created_at": w.created_at.isoformat(),
        }
        for w in work_orders
    ]


@router.get("/contractors", response_model=list[dict])
def list_contractors(db: Session = Depends(get_db)):
    contractors = db.query(Contractor).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "service_type": c.service_type,
            "city": c.city,
            "status": c.status,
        }
        for c in contractors
    ]
