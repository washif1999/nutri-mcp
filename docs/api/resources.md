# 📦 MCP Resources Reference

Resources are read-only data exposed via the MCP protocol. Access them using any MCP-compatible client.

---

## `nutrition://targets`

Daily macro and calorie benchmark targets.

**Response:**
```json
{
  "daily_targets": {
    "calories": 2000,
    "protein_g": 150,
    "carbs_g": 225,
    "fat_g": 65
  },
  "note": "These are general targets. Adjust based on your TDEE calculation."
}
```

---

## `nutrition://logs`

Last 10 logged meals.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Grilled Chicken Breast (200g)",
    "protein": 46.0,
    "carbs": 0.0,
    "fat": 5.0,
    "calories": 229.0,
    "timestamp": "2026-03-01T05:30:00"
  }
]
```

---

## `nutrition://bmi-categories`

BMI classification reference guide.

**Response:**
```json
[
  {"range": "< 18.5",     "category": "Underweight",    "risk": "Increased risk of malnutrition"},
  {"range": "18.5–24.9",  "category": "Normal weight",  "risk": "Lowest health risk"},
  {"range": "25.0–29.9",  "category": "Overweight",     "risk": "Increased risk of chronic disease"},
  {"range": "30.0–34.9",  "category": "Obese Class I",  "risk": "High risk"},
  {"range": "35.0–39.9",  "category": "Obese Class II", "risk": "Very high risk"},
  {"range": "≥ 40.0",     "category": "Obese Class III","risk": "Extremely high risk"}
]
```

---

## `health://complaints`

Last 5 logged health complaints, most recent first.

**Response:**
```json
[
  {
    "id": 4,
    "description": "Severe chest tightness and shortness of breath",
    "severity": 9,
    "timestamp": "2026-03-01T05:30:00"
  }
]
```

---

## `health://hospitals`

All hospitals ordered by rating (descending).

**Response:**
```json
[
  {
    "id": 1,
    "name": "Mayo Clinic",
    "specialty": "General & Cardiology",
    "rating": 4.9,
    "contact": "+1-507-284-2511",
    "address": "200 First St SW, Rochester, MN"
  }
]
```

---

## `health://appointments`

All auto-booked doctor appointments.

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

**Appointment Status Values:**

| Status | Meaning |
|---|---|
| `scheduled` | Auto-booked, awaiting confirmation |
| `completed` | Appointment attended |
| `cancelled` | Appointment cancelled |
