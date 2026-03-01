"""
test_analytics.py - Unit tests for BMI, TDEE, and weekly summary analytics.
"""
import pytest
from app.services.analytics_service import compute_bmi, compute_tdee, get_weekly_summary
from app.schemas.schemas import MealCreate
from app.services.nutrition_service import create_meal


class TestComputeBMI:
    def test_normal_weight(self):
        result = compute_bmi(70, 175)
        assert result["bmi"] == pytest.approx(22.86, abs=0.1)
        assert result["category"] == "Normal weight"

    def test_underweight(self):
        result = compute_bmi(45, 175)
        assert result["category"] == "Underweight"

    def test_overweight(self):
        result = compute_bmi(90, 175)
        assert result["category"] == "Overweight"

    def test_obese_class1(self):
        result = compute_bmi(100, 175)
        assert "Obese" in result["category"]

    def test_bmi_formula(self):
        # BMI = weight / (height_m)^2
        result = compute_bmi(80, 180)
        expected = round(80 / (1.80 ** 2), 2)
        assert result["bmi"] == expected


class TestComputeTDEE:
    def test_male_moderate(self):
        result = compute_tdee(75, 175, 30, "male", "moderate")
        assert result["bmr"] == pytest.approx(1698.8, abs=1)
        assert result["tdee"] == pytest.approx(2633.1, abs=5)

    def test_female_sedentary(self):
        result = compute_tdee(60, 163, 25, "female", "sedentary")
        assert "bmr" in result
        assert result["tdee"] < result["bmr"] * 1.5  # sedentary multiplier = 1.2

    def test_activity_levels_increase_tdee(self):
        base = compute_tdee(70, 170, 28, "male", "sedentary")["tdee"]
        active = compute_tdee(70, 170, 28, "male", "very_active")["tdee"]
        assert active > base

    def test_returns_correct_keys(self):
        result = compute_tdee(70, 170, 28, "male", "light")
        assert set(result.keys()) == {"bmr", "tdee", "activity_level"}


class TestWeeklySummary:
    def test_empty_db_returns_empty_list(self, db):
        summary = get_weekly_summary(db)
        assert summary == []

    def test_returns_aggregated_calories(self, db):
        create_meal(db, MealCreate(name="Meal 1", protein=30, carbs=50, fat=10))
        create_meal(db, MealCreate(name="Meal 2", protein=20, carbs=30, fat=5))
        summary = get_weekly_summary(db)
        assert len(summary) == 1  # same day
        assert summary[0]["meals"] == 2
        assert summary[0]["calories"] > 0
