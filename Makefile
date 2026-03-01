.PHONY: run seed test docker-build docker-up docker-down docker-logs docker-shell

# ── Local Development ─────────────────────────────────────────────────────────

## Start the server locally
run:
	uv run python server.py

## Seed the database with sample data
seed:
	uv run python seed.py

## Run the full test suite with coverage
test:
	uv run pytest tests/ -v --cov=app --cov-report=term-missing

## Install all dependencies
install:
	uv sync

# ── Docker ────────────────────────────────────────────────────────────────────

## Build the Docker image
docker-build:
	docker compose build

## Start containers (detached)
docker-up:
	docker compose up -d --build

## Stop containers
docker-down:
	docker compose down

## Tail container logs
docker-logs:
	docker compose logs -f nutri-mcp

## Open a shell inside the running container
docker-shell:
	docker compose exec nutri-mcp sh

## Check container health status
docker-status:
	docker compose ps

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  NutriMCP — Available Commands"
	@echo "  ─────────────────────────────────────────"
	@echo "  make run           Start server locally"
	@echo "  make seed          Seed the database"
	@echo "  make test          Run pytest with coverage"
	@echo "  make install       Install dependencies via uv"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-up     Start container (detached)"
	@echo "  make docker-down   Stop container"
	@echo "  make docker-logs   Tail container logs"
	@echo "  make docker-shell  Shell into container"
	@echo "  make docker-status Show container health"
	@echo ""
