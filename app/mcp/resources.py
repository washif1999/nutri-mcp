import json
from ..core.database import SessionLocal
from ..services.nutrition_service import get_meals, get_complaints, get_appointments
from ..models.models import Hospital
from .tools import mcp

@mcp.resource("nutrition://targets")
def get_nutrition_targets() -> str:
    """Daily nutritional benchmarks (calories and macros)."""
    return json.dumps({"calories": 2000, "macros": {"protein_g": 150, "carbs_g": 200, "fat_g": 65}}, indent=2)

@mcp.resource("nutrition://logs")
def get_meal_logs() -> str:
    """Recent meal logs (last 10) from the database."""
    db = SessionLocal()
    try:
        meals = get_meals(db, limit=10)
        return json.dumps(
            [{"id": m.id, "name": m.name, "calories": m.calories, "protein": m.protein, "timestamp": m.timestamp.isoformat()} for m in meals],
            indent=2
        )
    finally:
        db.close()

@mcp.resource("nutrition://bmi-categories")
def get_bmi_categories() -> str:
    """Reference guide for BMI ranges and categories."""
    return json.dumps([
        {"range": "< 18.5",      "category": "Underweight"},
        {"range": "18.5 – 24.9", "category": "Normal weight"},
        {"range": "25.0 – 29.9", "category": "Overweight"},
        {"range": "30.0 – 34.9", "category": "Obese Class I"},
        {"range": "35.0 – 39.9", "category": "Obese Class II"},
        {"range": ">= 40.0",     "category": "Obese Class III"},
    ], indent=2)

@mcp.resource("health://complaints")
def get_health_complaints() -> str:
    """Recent health complaints (last 5) from the database."""
    db = SessionLocal()
    try:
        complaints = get_complaints(db, limit=5)
        return json.dumps(
            [{"id": c.id, "description": c.description, "severity": c.severity, "timestamp": c.timestamp.isoformat()} for c in complaints],
            indent=2
        )
    finally:
        db.close()

@mcp.resource("health://hospitals")
def get_hospitals() -> str:
    """List of all available hospitals for doctor appointments."""
    db = SessionLocal()
    try:
        hospitals = db.query(Hospital).order_by(Hospital.rating.desc()).all()
        return json.dumps(
            [{"id": h.id, "name": h.name, "specialty": h.specialty, "rating": h.rating, "contact": h.contact, "address": h.address} for h in hospitals],
            indent=2
        )
    finally:
        db.close()

@mcp.resource("health://appointments")
def get_all_appointments() -> str:
    """List of all auto-booked doctor appointments."""
    db = SessionLocal()
    try:
        appts = get_appointments(db, limit=20)
        return json.dumps(
            [{"id": a.id, "complaint_id": a.complaint_id, "hospital_id": a.hospital_id, "status": a.status, "timestamp": a.timestamp.isoformat()} for a in appts],
            indent=2
        )
    finally:
        db.close()
