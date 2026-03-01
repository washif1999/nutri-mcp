# ──────────────────────────────────────────────
# Stage 1: Builder — install dependencies
# ──────────────────────────────────────────────
FROM python:3.11-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# ──────────────────────────────────────────────
# Stage 2: Runtime — lean production image
# ──────────────────────────────────────────────
FROM python:3.11-alpine AS runtime

LABEL name="nutri-mcp" \
      version="2.0.0" \
      description="Smart Macro & Nutrition Assistant MCP Server"

WORKDIR /app

# Copy only the venv from builder (no build tools in final image)
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY app/ ./app/
COPY server.py seed.py ./

# Ensure db directory exists for SQLite persistence
RUN mkdir -p /app/db

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONWARNINGS="ignore::DeprecationWarning"

EXPOSE 9000

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
