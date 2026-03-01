"""
test_services.py - Unit tests for the nutrition service layer.
"""
import pytest
from app.schemas.schemas import MealCreate, ComplaintCreate
from app.services.nutrition_service import (
    create_meal, get_meals, delete_meal,
    create_complaint, get_complaints, compute_macros,
)
from app.models.models import AuthKey, Hospital


# ── Meal Tests ────────────────────────────────────────────────────────────────

class TestCreateMeal:
    def test_creates_meal_with_correct_calories(self, db):
        meal = create_meal(db, MealCreate(name="Chicken", protein=30, carbs=10, fat=5))
        assert meal.id is not None
        assert meal.calories == (30 * 4) + (10 * 4) + (5 * 9)

    def test_creates_meal_stored_in_db(self, db):
        create_meal(db, MealCreate(name="Rice", protein=5, carbs=45, fat=2))
        meals = get_meals(db, limit=10)
        assert len(meals) == 1
        assert meals[0].name == "Rice"

    def test_get_meals_respects_limit(self, db):
        for i in range(5):
            create_meal(db, MealCreate(name=f"Meal {i}", protein=10, carbs=10, fat=5))
        assert len(get_meals(db, limit=3)) == 3

    def test_delete_meal_removes_record(self, db):
        meal = create_meal(db, MealCreate(name="Salad", protein=5, carbs=10, fat=3))
        assert delete_meal(db, meal.id) is True
        assert len(get_meals(db, limit=10)) == 0

    def test_delete_nonexistent_meal_returns_false(self, db):
        assert delete_meal(db, 9999) is False


# ── Complaint Tests ────────────────────────────────────────────────────────────

class TestCreateComplaint:
    def test_low_severity_no_appointment(self, db):
        complaint, appt = create_complaint(db, ComplaintCreate(description="Mild headache", severity=3))
        assert complaint.id is not None
        assert appt is None  # threshold is 7; no hospital seeded anyway

    def test_high_severity_with_hospital_books_appointment(self, db):
        # Seed a hospital first
        db.add(Hospital(name="Test Hospital", specialty="General", rating=4.5, contact="000", address="Test City"))
        db.commit()

        complaint, appt = create_complaint(db, ComplaintCreate(description="Severe chest pain", severity=9))
        assert complaint.severity == 9
        assert appt is not None
        assert appt["hospital"] == "Test Hospital"
        assert appt["status"] == "scheduled"

    def test_high_severity_no_hospital_returns_none(self, db):
        # No hospitals in DB
        complaint, appt = create_complaint(db, ComplaintCreate(description="Severe pain", severity=8))
        assert appt is None

    def test_get_complaints_returns_most_recent(self, db):
        create_complaint(db, ComplaintCreate(description="First",  severity=2))
        create_complaint(db, ComplaintCreate(description="Second", severity=3))
        results = get_complaints(db, limit=5)
        assert results[0].description == "Second"  # most recent first


# ── Macro Calculation Tests ────────────────────────────────────────────────────

class TestComputeMacros:
    def test_calorie_formula(self):
        result = compute_macros(30, 50, 10)
        assert result["calories"] == (30 * 4) + (50 * 4) + (10 * 9)

    def test_zero_macros(self):
        result = compute_macros(0, 0, 0)
        assert result["calories"] == 0
        assert result["split"]["protein_pct"] == 0

    def test_percentage_sums_to_100(self):
        result = compute_macros(25, 50, 25)
        total = result["split"]["protein_pct"] + result["split"]["carbs_pct"] + result["split"]["fat_pct"]
        assert abs(total - 100.0) < 0.5  # allow minor rounding
