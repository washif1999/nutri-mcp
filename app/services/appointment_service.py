"""
appointment_service.py - Severity-triggered doctor appointment booking.

When a complaint severity >= SEVERITY_ALERT_THRESHOLD, the best available
hospital is selected and an Appointment record is created automatically.
"""
from sqlalchemy.orm import Session
from ..models.models import Hospital, Appointment
from ..core.config import settings

def find_best_hospital(db: Session) -> Hospital | None:
    """Return the highest-rated hospital in the database."""
    return db.query(Hospital).order_by(Hospital.rating.desc()).first()

def book_appointment(db: Session, complaint_id: int) -> dict | None:
    """
    Book a doctor appointment for a given complaint.
    Returns appointment details dict or None if no hospitals are available.
    """
    hospital = find_best_hospital(db)
    if not hospital:
        return None

    notes = f"Auto-booked due to high severity complaint (ID: {complaint_id})."
    appointment = Appointment(
        complaint_id=complaint_id,
        hospital_id=hospital.id,
        status="scheduled",
        notes=notes,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "appointment_id": appointment.id,
        "status": appointment.status,
        "hospital": hospital.name,
        "contact": hospital.contact,
        "address": hospital.address,
        "rating": hospital.rating,
        "notes": notes,
    }

def should_book(severity: int) -> bool:
    """Returns True if the severity meets or exceeds the alert threshold."""
    return severity >= settings.severity_alert_threshold
