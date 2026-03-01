"""
test_schemas.py - Unit tests for Pydantic schema validation.
"""
import pytest
from pydantic import ValidationError
from app.schemas.schemas import (
    MealCreate, ComplaintCreate, MacroInput, BMIInput, TDEEInput
)


class TestMealCreate:
    def test_valid_meal(self):
        meal = MealCreate(name="Chicken", protein=30, carbs=10, fat=5)
        assert meal.name == "Chicken"

    def test_name_cannot_be_blank(self):
        with pytest.raises(ValidationError):
            MealCreate(name="   ", protein=30, carbs=10, fat=5)

    def test_negative_protein_rejected(self):
        with pytest.raises(ValidationError):
            MealCreate(name="Test", protein=-1, carbs=10, fat=5)

    def test_negative_carbs_rejected(self):
        with pytest.raises(ValidationError):
            MealCreate(name="Test", protein=10, carbs=-5, fat=5)

    def test_negative_fat_rejected(self):
        with pytest.raises(ValidationError):
            MealCreate(name="Test", protein=10, carbs=5, fat=-2)

    def test_zero_macros_allowed(self):
        meal = MealCreate(name="Water", protein=0, carbs=0, fat=0)
        assert meal.protein == 0


class TestComplaintCreate:
    def test_valid_complaint(self):
        c = ComplaintCreate(description="Headache", severity=5)
        assert c.severity == 5

    def test_severity_zero_rejected(self):
        with pytest.raises(ValidationError):
            ComplaintCreate(description="Test", severity=0)

    def test_severity_eleven_rejected(self):
        with pytest.raises(ValidationError):
            ComplaintCreate(description="Test", severity=11)

    def test_blank_description_rejected(self):
        with pytest.raises(ValidationError):
            ComplaintCreate(description="  ", severity=5)

    def test_severity_boundaries(self):
        assert ComplaintCreate(description="Min", severity=1).severity == 1
        assert ComplaintCreate(description="Max", severity=10).severity == 10


class TestBMIInput:
    def test_valid_bmi_input(self):
        b = BMIInput(weight_kg=70, height_cm=175)
        assert b.weight_kg == 70

    def test_zero_weight_rejected(self):
        with pytest.raises(ValidationError):
            BMIInput(weight_kg=0, height_cm=175)

    def test_zero_height_rejected(self):
        with pytest.raises(ValidationError):
            BMIInput(weight_kg=70, height_cm=0)


class TestTDEEInput:
    def test_valid_tdee_input(self):
        t = TDEEInput(weight_kg=70, height_cm=175, age=30, gender="male", activity_level="moderate")
        assert t.gender == "male"

    def test_invalid_gender_rejected(self):
        with pytest.raises(ValidationError):
            TDEEInput(weight_kg=70, height_cm=175, age=30, gender="other", activity_level="moderate")

    def test_invalid_activity_level_rejected(self):
        with pytest.raises(ValidationError):
            TDEEInput(weight_kg=70, height_cm=175, age=30, gender="male", activity_level="extreme")

    def test_age_boundary(self):
        with pytest.raises(ValidationError):
            TDEEInput(weight_kg=70, height_cm=175, age=0, gender="female", activity_level="light")
