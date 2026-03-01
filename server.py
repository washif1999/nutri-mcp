"""
server.py - Entry point for NutritionAssistant MCP Server.

All application logic is modularized inside the `app/` package:
  app/core/       - Config and database setup
  app/models/     - SQLAlchemy ORM models
  app/schemas/    - Pydantic validation schemas
  app/services/   - Business logic
  app/middleware/ - Authentication middleware
  app/mcp/        - MCP tools, resources, and prompts
  app/utils/      - Startup banner and utilities
"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")

import uvicorn
from app.utils.banner import print_banner, print_startup_info
from app.main import mcp
from app.middleware.auth import APIKeyAuthMiddleware

if __name__ == "__main__":
    print_banner()
    print_startup_info()
    # Wrap the FastMCP ASGI app with auth middleware directly —
    # avoids FastMCP's internal middleware validator (no more WARNING)
    asgi_app = APIKeyAuthMiddleware(mcp.http_app())
    uvicorn.run(asgi_app, host="0.0.0.0", port=9000)
