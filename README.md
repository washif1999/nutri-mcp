# 🥗 Smart Macro & Nutrition Assistant MCP Server

> A production-ready **Model Context Protocol (MCP)** server for health and nutrition tracking — built with FastMCP, SQLAlchemy, and Pydantic.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [MCP Tools](#mcp-tools)
- [MCP Resources](#mcp-resources)
- [MCP Prompts](#mcp-prompts)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Seeding Data](#seeding-data)
- [Running Tests](#running-tests)
- [Docker](#docker)

---

## Overview

This MCP server provides intelligent nutrition and health tracking capabilities to any LLM client that supports the MCP protocol (Claude Desktop, Supergateway, etc.). It features:

- **Macro & calorie tracking** with Pydantic-validated tools
- **BMI & TDEE analytics** using Mifflin-St Jeor formula
- **Health complaint logging** with automatic doctor appointment booking for severe cases (severity ≥ 7)
- **DB-backed API key authentication** via Bearer tokens
- **Colorized startup banner** with full URL and config display

---

## Project Structure

```
mcp-case-study-practice/
├── server.py                     # 🚀 Entry point — run this
├── seed.py                       # 🌱 Populate database with sample data
├── pytest.ini                    # 🧪 Test configuration
│
├── app/
│   ├── main.py                   # FastMCP app wiring
│   ├── core/
│   │   ├── config.py             # Settings from .env (pydantic-settings)
│   │   └── database.py           # SQLAlchemy engine & session
│   ├── models/
│   │   └── models.py             # ORM: AuthKey, Meal, Complaint, Hospital, Appointment
│   ├── schemas/
│   │   └── schemas.py            # Pydantic V2 validation schemas
│   ├── services/
│   │   ├── nutrition_service.py  # Meal/complaint CRUD + macro logic
│   │   ├── analytics_service.py  # BMI, TDEE, weekly reports
│   │   └── appointment_service.py# Severity-triggered booking
│   ├── middleware/
│   │   └── auth.py               # APIKeyAuthMiddleware
│   ├── mcp/
│   │   ├── tools.py              # MCP Tool definitions
│   │   ├── resources.py          # MCP Resource definitions
│   │   └── prompts.py            # MCP Prompt definitions
│   └── utils/
│       └── banner.py             # Colorized startup display
│
├── tests/
│   ├── conftest.py               # Fixtures (in-memory SQLite)
│   ├── test_services.py          # Meal, complaint, macro tests
│   ├── test_analytics.py         # BMI, TDEE, weekly summary tests
│   ├── test_auth.py              # API key model tests
│   └── test_schemas.py           # Pydantic validation tests
│
├── Dockerfile                    # Alpine Linux container
├── docker-compose.yml            # Docker Compose setup
├── pyproject.toml                # Dependencies (uv)
├── .env                          # Local environment config
├── .env.docker                   # Docker environment config
└── .env.sample                   # Template for env setup
```

---

## Features

### Phase 1 — Core MCP Server
- ✅ FastMCP server with SQLAlchemy + SQLite
- ✅ DB-backed Bearer token authentication middleware
- ✅ `calculate_macros`, `log_meal`, `log_complaint` tools
- ✅ `nutrition://targets`, `nutrition://logs`, `health://complaints` resources
- ✅ `dietary_analysis`, `health_summary` prompts
- ✅ `/health` endpoint

### Phase 2 — Analytics & Doctor Booking
- ✅ `calculate_bmi`, `calculate_tdee` tools
- ✅ `get_weekly_report`, `remove_meal`, `list_appointments` tools
- ✅ Auto-book doctor at **best-rated hospital** when complaint severity ≥ 7
- ✅ `health://hospitals`, `health://appointments`, `nutrition://bmi-categories` resources
- ✅ Configurable severity threshold via `SEVERITY_ALERT_THRESHOLD`

### Phase 3 — Testing
- ✅ 45 unit tests across 4 test files
- ✅ 100% coverage on schemas, models, analytics, appointment services
- ✅ In-memory SQLite fixtures for test isolation

---

## Getting Started

### Prerequisites
- Python ≥ 3.11
- [`uv`](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd mcp-case-study-practice

# Install dependencies
uv sync

# Setup environment
cp .env.sample .env

# Seed the database
uv run python seed.py

# Start the server
uv run python server.py
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./nutrition.db` | SQLite database path |
| `DEBUG` | `True` | Debug mode flag |
| `DEFAULT_AUTH_TOKEN` | `secret-key-nutrition-123` | Default API key seeded on startup |
| `SEVERITY_ALERT_THRESHOLD` | `7` | Complaint severity that triggers auto-booking |

---

## MCP Tools

### Phase 1 Tools

| Tool | Parameters | Description |
|---|---|---|
| `calculate_macros` | `protein`, `carbs`, `fat` (float) | Returns calories + % split |
| `log_meal` | `name`, `protein`, `carbs`, `fat` | Saves meal to DB |
| `log_complaint` | `description`, `severity` (1-10) | Logs complaint; auto-books if severity ≥ threshold |

### Phase 2 Tools

| Tool | Parameters | Description |
|---|---|---|
| `calculate_bmi` | `weight_kg`, `height_cm` | Returns BMI + category |
| `calculate_tdee` | `weight_kg`, `height_cm`, `age`, `gender`, `activity_level` | Returns BMR + TDEE |
| `get_weekly_report` | — | 7-day calorie/macro summary |
| `remove_meal` | `meal_id` | Deletes a meal from the DB |
| `list_appointments` | — | Lists all auto-booked appointments |

**Activity levels:** `sedentary` · `light` · `moderate` · `active` · `very_active`

---

## MCP Resources

| URI | Description |
|---|---|
| `nutrition://targets` | Daily macro benchmarks (calories, protein, carbs, fat) |
| `nutrition://logs` | Last 10 logged meals |
| `nutrition://bmi-categories` | BMI range reference guide |
| `health://complaints` | Last 5 health complaints |
| `health://hospitals` | All hospitals (sorted by rating) |
| `health://appointments` | All auto-booked appointments |

---

## MCP Prompts

| Prompt | Description |
|---|---|
| `dietary_analysis` | Guides LLM to compare intake vs. daily targets |
| `health_summary` | Prepares a complaint summary for medical consultation |

---

## API Endpoints

| Method | URL | Auth | Description |
|---|---|---|---|
| `GET` | `http://localhost:8000/health` | ❌ None | Health check |
| `*` | `http://localhost:8000/mcp/` | ✅ Bearer | MCP protocol |
| `GET` | `http://localhost:8000/mcp/sse` | ✅ Bearer | SSE stream (Supergateway) |

```bash
# Health check
curl -s http://localhost:8000/health

# MCP (with auth)
curl -H "Authorization: Bearer secret-key-nutrition-123" http://localhost:8000/mcp/
```

---

## Authentication

All `/mcp/*` routes require a Bearer token:

```
Authorization: Bearer <api_key>
```

API keys are stored in the `authkeys` database table. Default keys seeded by `seed.py`:

| API Key | Client |
|---|---|
| `secret-key-nutrition-123` | Default Client |
| `secret-key-dev-1234` | Dev Client |
| `secret-key-prod-5678` | Prod Client |

---

## Seeding Data

```bash
uv run python seed.py
```

Seeds: API keys, 5 hospitals (Mayo Clinic, Cleveland Clinic, etc.), 8 sample meals, 7 health complaints (2 with high severity to demo auto-booking).

---

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# With coverage report
uv run pytest tests/ -v --cov=app --cov-report=term-missing
```

**Results:** 45 tests · 0.18s · 56% overall coverage (100% on core business logic)

---

## Docker

```bash
# Build and run
docker compose up

# Or build manually
docker build -t team-mcp-service .
docker run -p 8000:8000 --env-file .env.docker team-mcp-service
```

Docker uses `.env.docker` and mounts a `data/` volume for SQLite persistence.

---

## Supergateway Integration

```bash
npx supergateway --port 8080 \
  --url http://localhost:8000/mcp/sse \
  --header "Authorization: Bearer secret-key-nutrition-123"
```
