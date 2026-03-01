# 🔑 Authentication

All `/mcp` routes require a valid API key passed as a Bearer token.

## Header Format

```
Authorization: Bearer <api_key>
```

## Default API Keys (seeded by `seed.py`)

| Client | API Key |
|---|---|
| Default | `default-key-aCW5eV_VAL20k9MToEUOoFHQ2_DIXu80GxJYIkPSAIc` |
| Dev | `dev-key-iMq39muMWJ2AHRoDNncztH4BhIGhyPwUn0JZZZCLbgc` |
| Prod | `prod-key-32ZQf_8o0kh1D5xnflhCZjz5vTxp6XZTmUfnS0nWM1A` |

> Keys are stored in the `authkeys` table. Format: `{env}-key-{secrets.token_urlsafe(32)}`

## Example

```bash
curl -X POST http://localhost:9000/mcp \
  -H "Authorization: Bearer default-key-aCW5eV_VAL20k9MToEUOoFHQ2_DIXu80GxJYIkPSAIc" \
  -H "Content-Type: application/json"
```

## Error Responses

| Status | Reason |
|---|---|
| `401` | Missing `Authorization` header |
| `401` | Token not found in database |

```json
{"detail": "Missing or invalid Authorization header. Use: Bearer <api_key>"}
{"detail": "Invalid API Key"}
```

## Open Paths (no auth required)

| Path | Reason |
|---|---|
| `/health` | Health check |
