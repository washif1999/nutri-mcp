"""
analytics_service.py - BMI, TDEE, and weekly meal summary calculations.
"""
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.models import Meal

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

BMI_CATEGORIES = [
    (0,   18.5, "Underweight"),
    (18.5, 25,  "Normal weight"),
    (25,   30,  "Overweight"),
    (30,   35,  "Obese (Class I)"),
    (35,   40,  "Obese (Class II)"),
    (40,  999,  "Obese (Class III)"),
]

def compute_bmi(weight_kg: float, height_cm: float) -> dict:
    """Calculate BMI and return value with category."""
    bmi = weight_kg / ((height_cm / 100) ** 2)
    category = next(c for lo, hi, c in BMI_CATEGORIES if lo <= bmi < hi)
    return {"bmi": round(bmi, 2), "category": category}

def compute_tdee(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str) -> dict:
    """
    Calculate TDEE using the Mifflin-St Jeor equation.
    gender: 'male' or 'female'
    activity_level: sedentary | light | moderate | active | very_active
    """
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
    tdee = bmr * multiplier
    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "activity_level": activity_level
    }

def get_weekly_summary(db: Session) -> list[dict]:
    """Aggregate total calories and macros by day for the past 7 days."""
    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    meals = db.query(Meal).filter(Meal.timestamp >= seven_days_ago).all()

    summary: dict[str, dict] = {}
    for m in meals:
        day = m.timestamp.date().isoformat()
        if day not in summary:
            summary[day] = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0, "meals": 0}
        summary[day]["calories"] += m.calories
        summary[day]["protein"] += m.protein
        summary[day]["carbs"] += m.carbs
        summary[day]["fat"] += m.fat
        summary[day]["meals"] += 1

    return [{"date": k, **{k2: round(v2, 1) for k2, v2 in v.items()}} for k, v in sorted(summary.items())]
