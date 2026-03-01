# 🛠️ MCP Tools Reference

All tools are accessible via the MCP protocol at `http://localhost:9000/mcp`.

---

## Phase 1 Tools

### `calculate_macros`
Calculate total calories and macro percentage split.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `protein` | float | ✅ | Protein in grams |
| `carbs` | float | ✅ | Carbohydrates in grams |
| `fat` | float | ✅ | Fat in grams |

**Response:**
```json
{
  "protein_g": 30,
  "carbs_g": 50,
  "fat_g": 10,
  "calories": 410,
  "split": {
    "protein_pct": 29.3,
    "carbs_pct": 48.8,
    "fat_pct": 21.9
  }
}
```

---

### `log_meal`
Save a meal to the database.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Meal name |
| `protein` | float | ✅ | Protein in grams (≥ 0) |
| `carbs` | float | ✅ | Carbs in grams (≥ 0) |
| `fat` | float | ✅ | Fat in grams (≥ 0) |

**Response:**
```json
{
  "message": "Meal logged successfully.",
  "meal_id": 1,
  "name": "Grilled Chicken",
  "calories": 229.0
}
```

---

### `log_complaint`
Log a health complaint. If `severity >= SEVERITY_ALERT_THRESHOLD` (default: 7), a doctor appointment is automatically booked at the highest-rated hospital.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `description` | string | ✅ | Complaint description |
| `severity` | int | ✅ | Severity level **1–10** |

**Response (low severity):**
```json
{
  "message": "Complaint logged successfully.",
  "complaint_id": 3,
  "severity": 4
}
```

**Response (high severity ≥ 7):**
```json
{
  "message": "Complaint logged successfully.",
  "complaint_id": 4,
  "severity": 9,
  "alert": "⚠️ High severity detected! Doctor appointment automatically booked.",
  "appointment": {
    "appointment_id": 1,
    "status": "scheduled",
    "hospital": "Mayo Clinic",
    "contact": "+1-507-284-2511",
    "address": "200 First St SW, Rochester, MN",
    "rating": 4.9
  }
}
```

---

## Phase 2 Tools

### `calculate_bmi`
Calculate Body Mass Index and health category.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `weight_kg` | float | ✅ | Weight in kilograms (> 0) |
| `height_cm` | float | ✅ | Height in centimetres (> 0) |

**Response:**
```json
{
  "weight_kg": 70,
  "height_cm": 175,
  "bmi": 22.86,
  "category": "Normal weight"
}
```

**BMI Categories:**

| BMI Range | Category |
|---|---|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal weight |
| 25.0 – 29.9 | Overweight |
| 30.0 – 34.9 | Obese Class I |
| 35.0 – 39.9 | Obese Class II |
| ≥ 40.0 | Obese Class III |

---

### `calculate_tdee`
Calculate Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor formula.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `weight_kg` | float | ✅ | Weight in kg |
| `height_cm` | float | ✅ | Height in cm |
| `age` | int | ✅ | Age in years (> 0) |
| `gender` | string | ✅ | `"male"` or `"female"` |
| `activity_level` | string | ✅ | See table below |

**Activity Levels:**

| Value | Multiplier | Description |
|---|---|---|
| `sedentary` | 1.2 | Little or no exercise |
| `light` | 1.375 | Light exercise 1–3 days/week |
| `moderate` | 1.55 | Moderate exercise 3–5 days/week |
| `active` | 1.725 | Hard exercise 6–7 days/week |
| `very_active` | 1.9 | Very hard exercise + physical job |

**Response:**
```json
{
  "bmr": 1698.8,
  "tdee": 2633.1,
  "activity_level": "moderate"
}
```

---

### `get_weekly_report`
Get a 7-day summary of logged meals grouped by day.

*No parameters required.*

**Response:**
```json
[
  {
    "date": "2026-03-01",
    "meals": 3,
    "calories": 1820.5,
    "protein_g": 145.0,
    "carbs_g": 180.0,
    "fat_g": 55.0
  }
]
```

---

### `remove_meal`
Delete a meal from the database by ID.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `meal_id` | int | ✅ | ID of the meal to delete |

**Response:**
```json
{"message": "Meal 5 removed successfully."}
```

**Error:**
```json
{"error": "Meal with ID 99 not found."}
```

---

### `list_appointments`
List all auto-booked doctor appointments.

*No parameters required.*

**Response:**
```json
[
  {
    "id": 1,
    "complaint_id": 4,
    "hospital_id": 1,
    "status": "scheduled",
    "notes": "Auto-booked due to high severity complaint (ID: 4).",
    "timestamp": "2026-03-01T05:30:00"
  }
]
```
