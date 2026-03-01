# 📦 MCP Resources Reference

Resources are read-only data exposed via the MCP protocol.

> **Nutrition resources** (`nutrition://logs`, `nutrition://targets`, `nutrition://bmi-categories`)
> have moved to the `nutrimcp-agent` project.

---

## `health://complaints`

Recent health complaints (last 5), most recent first.

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
