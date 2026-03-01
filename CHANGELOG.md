# Changelog

All notable changes to this project are documented here.

---

## [2.0.0] — 2026-02-28 (Phase 3)

### Added — Testing
- `tests/conftest.py` — in-memory SQLite fixture for test isolation
- `tests/test_services.py` — 15 unit tests for meal/complaint/macro services
- `tests/test_analytics.py` — 11 unit tests for BMI, TDEE, weekly summary
- `tests/test_auth.py` — 4 API key model tests
- `tests/test_schemas.py` — 18 Pydantic validation tests
- `pytest.ini` — test configuration

**45 tests · 0.18s · 100% core business logic coverage**

---

## [1.1.0] — 2026-02-28 (Phase 2)

### Added — Analytics & Doctor Booking
- `calculate_bmi` tool — BMI + category via Mifflin-St Jeor
- `calculate_tdee` tool — Total Daily Energy Expenditure
- `get_weekly_report` tool — 7-day macro/calorie aggregation
- `remove_meal` tool — delete a meal by ID
- `list_appointments` tool — view all auto-booked appointments
- **Auto-booking**: complaints with severity ≥ `SEVERITY_ALERT_THRESHOLD` automatically book at highest-rated hospital
- `Hospital` and `Appointment` DB models
- `health://hospitals` and `health://appointments` resources
- `nutrition://bmi-categories` resource
- `app/services/analytics_service.py`
- `app/services/appointment_service.py`
- `app/utils/banner.py` — colorized startup banner with `art` + `colorama`
- Hospital seed data (Mayo Clinic, Cleveland Clinic, Johns Hopkins, etc.)

---

## [1.0.0] — 2026-02-28 (Phase 1)

### Added — Core MCP Server
- FastMCP server with modular FastAPI project structure
- SQLAlchemy ORM with SQLite backend
- `AuthKey`, `Meal`, `Complaint` DB models
- `APIKeyAuthMiddleware` — Bearer token validation against DB
- Tools: `calculate_macros`, `log_meal`, `log_complaint`
- Resources: `nutrition://targets`, `nutrition://logs`, `health://complaints`
- Prompts: `dietary_analysis`, `health_summary`
- `/health` endpoint
- Docker: `Dockerfile` (Alpine), `docker-compose.yml`
- Env config: `.env`, `.env.docker`, `.env.sample`
- `seed.py` — database population script
- `server.py` — minimal root entry point
