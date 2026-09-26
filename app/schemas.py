from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    check_in_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    bookings: Mapped[list["Booking"]] = relationship(back_populates="listing")
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="listing")


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    bookings: Mapped[list["Booking"]] = relationship(back_populates="guest")
    messages: Mapped[list["Message"]] = relationship(back_populates="guest")
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="guest")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    guest_id: Mapped[str] = mapped_column(ForeignKey("guests.id"), nullable=False)
    listing_id: Mapped[str] = mapped_column(ForeignKey("listings.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="confirmed")
    check_in: Mapped[Date] = mapped_column(Date, nullable=False)
    check_out: Mapped[Date] = mapped_column(Date, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), default="paid")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    guest: Mapped[Guest] = relationship(back_populates="bookings")
    listing: Mapped[Listing] = relationship(back_populates="bookings")
    messages: Mapped[list["Message"]] = relationship(back_populates="booking")
    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="booking")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    guest_id: Mapped[str | None] = mapped_column(ForeignKey("guests.id"), nullable=True)
    booking_id: Mapped[str | None] = mapped_column(ForeignKey("bookings.id"), nullable=True)
    sender_type: Mapped[str] = mapped_column(String(50), default="guest")
    channel: Mapped[str] = mapped_column(String(50), default="sms")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    urgency: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    guest: Mapped[Guest | None] = relationship(back_populates="messages")
    booking: Mapped[Booking | None] = relationship(back_populates="messages")


class Contractor(Base):
    __tablename__ = "contractors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="available")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    work_orders: Mapped[list["WorkOrder"]] = relationship(back_populates="contractor")


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    listing_id: Mapped[str] = mapped_column(ForeignKey("listings.id"), nullable=False)
    booking_id: Mapped[str | None] = mapped_column(ForeignKey("bookings.id"), nullable=True)
    guest_id: Mapped[str | None] = mapped_column(ForeignKey("guests.id"), nullable=True)
    contractor_id: Mapped[str | None] = mapped_column(ForeignKey("contractors.id"), nullable=True)
    issue_type: Mapped[str] = mapped_column(String(100), nullable=False)
    issue_summary: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), default="medium")
    status: Mapped[str] = mapped_column(String(50), default="open")
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    listing: Mapped[Listing] = relationship(back_populates="work_orders")
    booking: Mapped[Booking | None] = relationship(back_populates="work_orders")
    guest: Mapped[Guest | None] = relationship(back_populates="work_orders")
    contractor: Mapped[Contractor | None] = relationship(back_populates="work_orders")
