from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models import Booking, Contractor, Guest, Listing, Message, WorkOrder


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> dict:
        today = date.today()

        total_listings = db.query(Listing).count()
        total_guests = db.query(Guest).count()
        total_bookings = db.query(Booking).count()
        open_work_orders = db.query(WorkOrder).filter(WorkOrder.status != "resolved").count()
        urgent_work_orders = db.query(WorkOrder).filter(WorkOrder.priority == "high").count()
        upcoming_check_ins = db.query(Booking).filter(Booking.check_in >= today).count()

        recent_messages = db.query(Message).order_by(Message.created_at.desc()).limit(5).all()
        active_contractors = db.query(Contractor).filter(Contractor.status == "available").count()

        open_orders = db.query(WorkOrder).order_by(WorkOrder.created_at.desc()).limit(8).all()
        contractor_rows = db.query(Contractor).order_by(Contractor.created_at.desc()).limit(6).all()
        recent_bookings = db.query(Booking).order_by(Booking.created_at.desc()).limit(6).all()

        return {
            "stats": {
                "listings": total_listings,
                "guests": total_guests,
                "bookings": total_bookings,
                "open_work_orders": open_work_orders,
                "urgent_work_orders": urgent_work_orders,
                "upcoming_check_ins": upcoming_check_ins,
                "active_contractors": active_contractors,
            },
            "recent_messages": [
                {
                    "id": m.id,
                    "sender_type": m.sender_type,
                    "content": m.content,
                    "intent": m.intent,
                    "urgency": m.urgency,
                    "created_at": m.created_at.isoformat(),
                }
                for m in recent_messages
            ],
            "work_orders": [
                {
                    "id": w.id,
                    "issue_type": w.issue_type,
                    "issue_summary": w.issue_summary,
                    "priority": w.priority,
                    "status": w.status,
                    "created_at": w.created_at.isoformat(),
                }
                for w in open_orders
            ],
            "contractors": [
                {
                    "id": c.id,
                    "name": c.name,
                    "service_type": c.service_type,
                    "city": c.city,
                    "status": c.status,
                }
                for c in contractor_rows
            ],
            "bookings": [
                {
                    "id": b.id,
                    "check_in": b.check_in.isoformat(),
                    "check_out": b.check_out.isoformat(),
                    "status": b.status,
                    "payment_status": b.payment_status,
                }
                for b in recent_bookings
            ],
        }
