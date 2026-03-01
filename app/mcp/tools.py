import json
from ..core.database import SessionLocal
from ..schemas.schemas import MacroInput, MealCreate, ComplaintCreate, BMIInput, TDEEInput
from ..services.nutrition_service import create_meal, get_meals, create_complaint, get_complaints, delete_meal, get_appointments, compute_macros
from ..services.analytics_service import compute_bmi, compute_tdee, get_weekly_summary
from fastmcp import FastMCP

mcp = FastMCP("NutritionAssistant")

# ── Phase 1 Tools ─────────────────────────────────────────────────────────────

@mcp.tool()
async def calculate_macros(protein: float, carbs: float, fat: float) -> dict:
    """Calculate total calories and macro percentage split. All values must be >= 0."""
    MacroInput(protein=protein, carbs=carbs, fat=fat)
    return compute_macros(protein, carbs, fat)

@mcp.tool()
async def log_meal(name: str, protein: float, carbs: float, fat: float) -> str:
    """Log a meal to the database. Name must be non-empty, macros must be >= 0."""
    meal_data = MealCreate(name=name, protein=protein, carbs=carbs, fat=fat)
    db = SessionLocal()
    try:
        meal = create_meal(db, meal_data)
        return f"Logged meal '{meal.name}' - {meal.calories:.1f} kcal"
    finally:
        db.close()

@mcp.tool()
async def log_complaint(description: str, severity: int) -> dict:
    """
    Log a health complaint. Severity must be 1-10.
    If severity >= 7, a doctor appointment is automatically booked at the best hospital.
    """
    complaint_data = ComplaintCreate(description=description, severity=severity)
    db = SessionLocal()
    try:
        complaint, appointment = create_complaint(db, complaint_data)
        result = {
            "message": "Complaint logged successfully.",
            "complaint_id": complaint.id,
            "severity": complaint.severity,
        }
        if appointment:
            result["alert"] = "⚠️ High severity detected! Doctor appointment automatically booked."
            result["appointment"] = appointment
        return result
    finally:
        db.close()

# ── Phase 2 Tools ─────────────────────────────────────────────────────────────

@mcp.tool()
async def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """Calculate BMI and return the value with health category. Weight in kg, height in cm."""
    BMIInput(weight_kg=weight_kg, height_cm=height_cm)
    return compute_bmi(weight_kg, height_cm)

@mcp.tool()
async def calculate_tdee(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str) -> dict:
    """
    Calculate Total Daily Energy Expenditure (Mifflin-St Jeor).
    gender: 'male' or 'female'
    activity_level: sedentary | light | moderate | active | very_active
    """
    TDEEInput(weight_kg=weight_kg, height_cm=height_cm, age=age, gender=gender, activity_level=activity_level)
    return compute_tdee(weight_kg, height_cm, age, gender, activity_level)

@mcp.tool()
async def get_weekly_report() -> str:
    """Get a 7-day macro and calorie summary from logged meals."""
    db = SessionLocal()
    try:
        summary = get_weekly_summary(db)
        return json.dumps(summary, indent=2)
    finally:
        db.close()

@mcp.tool()
async def remove_meal(meal_id: int) -> str:
    """Delete a meal from the database by its ID."""
    if meal_id <= 0:
        raise ValueError("meal_id must be a positive integer.")
    db = SessionLocal()
    try:
        if delete_meal(db, meal_id):
            return f"Meal ID {meal_id} deleted successfully."
        return f"Meal ID {meal_id} not found."
    finally:
        db.close()

@mcp.tool()
async def list_appointments() -> str:
    """List all auto-booked doctor appointments."""
    db = SessionLocal()
    try:
        appts = get_appointments(db)
        return json.dumps(
            [{"id": a.id, "complaint_id": a.complaint_id, "hospital_id": a.hospital_id,
              "status": a.status, "notes": a.notes, "time": a.timestamp.isoformat()} for a in appts],
            indent=2
        )
    finally:
        db.close()
