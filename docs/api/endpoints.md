# 🌐 HTTP Endpoints

## GET /health

Health check endpoint. No authentication required.

**URL:** `http://localhost:9000/health`

**Request:**
```bash
curl -s http://localhost:9000/health
```

**Response `200 OK`:**
```json
{
  "status": "healthy",
  "service": "NutritionAssistant MCP",
  "database": "sqlite:///./db/nutrition.db",
  "timestamp": "2026-03-01T05:30:00.000000"
}
```

---

## POST /mcp  *(MCP Protocol)*

Main MCP protocol endpoint — handles all tool calls, resource reads, and prompt requests via StreamableHTTP transport.

**URL:** `http://localhost:9000/mcp`  
**Auth:** `Authorization: Bearer <api_key>` required  
**Transport:** StreamableHTTP (MCP SDK)

> Use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) or any MCP-compatible LLM client to interact with this endpoint. Do not call it directly with plain HTTP unless you implement the MCP protocol.

**MCP Inspector connection:**
```
URL:       http://localhost:9000/mcp
Transport: streamable-http
Header:    Authorization: Bearer <api_key>
```
