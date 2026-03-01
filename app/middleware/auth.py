"""
app/middleware/auth.py - Pure ASGI auth middleware (no BaseHTTPMiddleware).
Bypasses FastMCP's middleware validator to eliminate the startup warning.
"""
import json
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse
from ..core.database import SessionLocal
from ..models.models import AuthKey


class APIKeyAuthMiddleware:
    """
    Pure ASGI middleware that validates Bearer tokens against the `authkeys` DB table.
    /health and all /mcp* paths are excluded from authentication.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")

        # Only /health is open — everything else (including /mcp) requires auth
        if path == "/health":
            await self.app(scope, receive, send)
            return

        # Check Authorization header
        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode()

        if not auth.startswith("Bearer "):
            response = JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header. Use: Bearer <api_key>"}
            )
            await response(scope, receive, send)
            return

        token = auth.removeprefix("Bearer ").strip()
        db = SessionLocal()
        try:
            key_entry = db.query(AuthKey).filter(AuthKey.api_key == token).first()
            if not key_entry:
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid API Key"}
                )
                await response(scope, receive, send)
                return
            scope["state"] = scope.get("state", {})
            scope["state"]["client"] = key_entry.client_name
        finally:
            db.close()

        await self.app(scope, receive, send)
