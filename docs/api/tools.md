# 🛠️ MCP Tools Reference

All tools are accessible via the MCP protocol at `http://localhost:9000/mcp`.

> **Meal management tools** (`log_meal`, `remove_meal`, `calculate_macros`, `calculate_bmi`,
> `calculate_tdee`, `get_weekly_report`) have moved to the `nutrimcp-agent` project.

---

## `log_complaint`

Log a health complaint. If `severity >= SEVERITY_ALERT_THRESHOLD` (default: 7), a doctor appointment is automatically booked at the highest-rated hospital.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `description` | string | ✅ | Complaint description (non-blank) |
| `severity` | int | ✅ | Severity level **1–10** |

**Response (low severity < 7):**
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

**Validation:**
- `description` cannot be blank
- `severity` must be between **1 and 10** (inclusive)

---

## `list_appointments`

List all auto-booked doctor appointments, most recent first.

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
    "time": "2026-03-01T05:30:00"
  }
]
```

**Appointment Status Values:**

| Status | Meaning |
|---|---|
| `scheduled` | Auto-booked, awaiting confirmation |
| `completed` | Appointment attended |
| `cancelled` | Appointment cancelled |
