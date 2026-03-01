# 📚 NutriMCP — Health Assistant API Documentation

Welcome to the full API reference for the **Health & Complaint Management MCP Server**.

> **Note:** Meal management, macro calculations, BMI, and TDEE tools have moved to the
> [`nutrimcp-agent`](../../nutrimcp-agent/README.md) project.

## Contents

| Document | Description |
|---|---|
| [Authentication](api/authentication.md) | API key setup and Bearer token usage |
| [HTTP Endpoints](api/endpoints.md) | REST endpoints (health check) |
| [MCP Tools](api/tools.md) | All MCP tool definitions with parameters |
| [MCP Resources](api/resources.md) | All MCP resource URIs and response formats |
| [MCP Prompts](api/prompts.md) | Built-in prompt templates |

## Ecosystem

```
nutrimcp-agent/          ← Meal management library (separate project)
    app/services/
        meal_service.py  ← create, get, search, delete meals
        analytics_service.py ← BMI, TDEE, macros

mcp-case-study-practice/ ← This MCP server (health domain)
    Tools: log_complaint · list_appointments
    Resources: health://complaints · health://hospitals · health://appointments
```

## Base URL

```
http://localhost:9000
```

## Quick Start

```bash
# 1. Seed the database (hospitals, complaints, API keys)
uv run python seed.py

# 2. Start the server
uv run python server.py

# 3. Verify it's up
curl -s http://localhost:9000/health

# 4. Docker
docker compose up -d --build
```
