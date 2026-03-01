# 📚 NutriMCP API Documentation

Welcome to the full API reference for the **Smart Macro & Nutrition Assistant MCP Server**.

## Contents

| Document | Description |
|---|---|
| [Authentication](api/authentication.md) | API key setup and Bearer token usage |
| [HTTP Endpoints](api/endpoints.md) | REST endpoints (health check) |
| [MCP Tools](api/tools.md) | All MCP tool definitions with parameters |
| [MCP Resources](api/resources.md) | All MCP resource URIs and response formats |
| [MCP Prompts](api/prompts.md) | Built-in prompt templates |

## Base URL

```
http://localhost:9000
```

## Quick Start

```bash
# 1. Seed the database
uv run python seed.py

# 2. Start the server
uv run python server.py

# 3. Verify it's up
curl -s http://localhost:9000/health
```
