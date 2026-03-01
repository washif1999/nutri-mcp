"""
nutrition_service.py - Business logic for meals and complaints.
Includes severity-based appointment trigger for Phase 2.
"""
from sqlalchemy.orm import Session
from ..models.models import Meal, Complaint, Appointment
from ..schemas.schemas import MealCreate, ComplaintCreate
from . import appointment_service

def create_meal(db: Session, meal: MealCreate) -> Meal:
    calories = (meal.protein * 4) + (meal.carbs * 4) + (meal.fat * 9)
    db_meal = Meal(
        name=meal.name,
        protein=meal.protein,
        carbs=meal.carbs,
        fat=meal.fat,
        calories=round(calories, 2)
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_meals(db: Session, limit: int = 10) -> list[Meal]:
    return db.query(Meal).order_by(Meal.timestamp.desc()).limit(limit).all()

def delete_meal(db: Session, meal_id: int) -> bool:
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        return False
    db.delete(meal)
    db.commit()
    return True

def create_complaint(db: Session, complaint: ComplaintCreate) -> tuple[Complaint, dict | None]:
    """
    Create a complaint. If severity >= threshold, auto-book a doctor appointment.
    Returns (complaint, appointment_details or None).
    """
    db_complaint = Complaint(
        description=complaint.description,
        severity=complaint.severity
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    appointment_details = None
    if appointment_service.should_book(complaint.severity):
        appointment_details = appointment_service.book_appointment(db, db_complaint.id)

    return db_complaint, appointment_details

def get_complaints(db: Session, limit: int = 5) -> list[Complaint]:
    return db.query(Complaint).order_by(Complaint.timestamp.desc()).limit(limit).all()

def get_appointments(db: Session, limit: int = 10) -> list[Appointment]:
    return db.query(Appointment).order_by(Appointment.timestamp.desc()).limit(limit).all()

def compute_macros(protein: float, carbs: float, fat: float) -> dict:
    calories = (protein * 4) + (carbs * 4) + (fat * 9)
    total = protein + carbs + fat
    return {
        "calories": round(calories, 2),
        "split": {
            "protein_pct": round((protein / total) * 100, 1) if total > 0 else 0,
            "carbs_pct": round((carbs / total) * 100, 1) if total > 0 else 0,
            "fat_pct": round((fat / total) * 100, 1) if total > 0 else 0
        }
    }
