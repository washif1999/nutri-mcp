import datetime
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from .core.config import settings
from .core.database import engine, SessionLocal
from .models.models import AuthKey
from .middleware.auth import APIKeyAuthMiddleware

# Import MCP components to register tools, resources, and prompts
from .mcp import tools
from .mcp import resources  # noqa: registers resources on the mcp instance
from .mcp import prompts    # noqa: registers prompts on the mcp instance

# Re-export mcp for uvicorn to discover: uvicorn app.main:mcp
mcp = tools.mcp



# Create all DB tables on startup
from .core.database import Base
from .models import models as _m  # noqa: ensure models are registered
Base.metadata.create_all(bind=engine)

# Seed default API key from settings
db = SessionLocal()
try:
    if not db.query(AuthKey).filter(AuthKey.api_key == settings.default_auth_token).first():
        db.add(AuthKey(api_key=settings.default_auth_token, client_name="Default Client"))
        db.commit()
finally:
    db.close()

# Add health check endpoint via custom_route
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy",
        "service": "NutritionAssistant MCP",
        "database": settings.database_url,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.http_app(), host="0.0.0.0", port=8000)
