.PHONY: help install lint format typecheck test test-unit test-integration test-robot test-security clean build run dev docker-up docker-down migrate seed cli

help:
	@echo "Available commands:"
	@echo "  install       Install project dependencies"
	@echo "  lint          Run linter (ruff)"
	@echo "  format        Format code (ruff)"
	@echo "  typecheck     Run type checker (mypy)"
	@echo "  test          Run all tests"
	@echo "  test-unit     Run unit tests"
	@echo "  test-integration Run integration tests"
	@echo "  test-robot    Run Robot Framework tests"
	@echo "  test-security Run security tests"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build Docker images"
	@echo "  run           Run API server locally"
	@echo "  dev           Run dev environment (docker-compose)"
	@echo "  docker-up     Start all Docker services"
	@echo "  docker-down   Stop all Docker services"
	@echo "  migrate       Run database migrations"
	@echo "  seed          Seed sample data"
	@echo "  cli           Run CLI tool"

install:
	poetry install

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/

test:
	pytest tests/unit tests/integration -v --cov=src --cov-report=term --cov-report=html

test-unit:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

test-robot:
	robot --outputdir reports/robot tests/robot/

test-security:
	robot --outputdir reports/security tests/security/ && \
	bandit -r src/ -f json -o reports/bandit.json && \
	safety check -r <(poetry export -f requirements.txt) --json > reports/safety.json

clean:
	rm -rf dist/ build/ __pycache__/ .pytest_cache/ .mypy_cache/ .ruff_cache/ reports/ htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:
	docker compose build

run:
	uvicorn stie.api.app:create_app --host 0.0.0.0 --port 8000 --factory --reload

dev:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build -d

docker-up:
	docker compose up -d

docker-down:
	docker compose down

migrate:
	alembic upgrade head

seed:
	python scripts/seed_data.py

cli:
	python -m stie.cli.entry

.PHONY: agent-setup
agent-setup:
	@echo "Setting up agent configuration..."
	@mkdir -p .opencode
	@echo "Agent configuration ready"
