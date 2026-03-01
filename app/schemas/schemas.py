import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

# ── Existing schemas ──────────────────────────────────────────────────────────

class MacroInput(BaseModel):
    protein: float = Field(ge=0)
    carbs: float = Field(ge=0)
    fat: float = Field(ge=0)

class MealCreate(BaseModel):
    name: str = Field(min_length=1)
    protein: float = Field(ge=0)
    carbs: float = Field(ge=0)
    fat: float = Field(ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Meal name cannot be blank")
        return v.strip()

class MealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    protein: float
    carbs: float
    fat: float
    calories: float
    timestamp: datetime.datetime

class ComplaintCreate(BaseModel):
    description: str = Field(min_length=1)
    severity: int = Field(ge=1, le=10)

    @field_validator("description")
    @classmethod
    def description_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Description cannot be blank")
        return v.strip()

class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    severity: int
    timestamp: datetime.datetime

# ── Phase 2 schemas ───────────────────────────────────────────────────────────

class BMIInput(BaseModel):
    weight_kg: float = Field(gt=0, description="Weight in kilograms")
    height_cm: float = Field(gt=0, description="Height in centimetres")

class TDEEInput(BaseModel):
    weight_kg: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    age: int = Field(gt=0, le=120)
    gender: str = Field(pattern="^(male|female)$")
    activity_level: str = Field(
        pattern="^(sedentary|light|moderate|active|very_active)$"
    )

class HospitalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    specialty: str
    rating: float
    contact: str
    address: str

class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    complaint_id: int
    hospital_id: int
    status: str
    notes: str | None
    timestamp: datetime.datetime
