# Space Threat Intelligence Exchange - Agent Instructions

## Project Overview
Decentralized CTI sharing platform for satellite intrusions and GNSS spoofing.
Reports are cryptographically signed (Ed25519) and shared via P2P network.

## Technology Stack
- **Backend**: Python 3.11+ / FastAPI / SQLAlchemy / asyncpg
- **Frontend**: TypeScript / React / Vite / TailwindCSS
- **Databases**: PostgreSQL, Redis, Qdrant, DuckDB, Apache Iceberg
- **Data**: Apache Arrow, Apache DataFusion, Trino
- **AI**: Ollama, vLLM, W&B Weave
- **P2P**: libp2p protocol implementation
- **Security**: Ed25519 crypto, OWASP Top 10 tested
- **Testing**: Pytest, Robot Framework
- **CI/CD**: GitHub Actions

## Development Workflow
1. Always work on the `dev` branch
2. Run `make lint` before committing
3. Run `make typecheck` to verify types
4. Run `make test-unit` for unit tests
5. Run `make test-robot` for Robot Framework tests
6. Run `make test-security` for OWASP security tests
7. Each commit should represent one atomic change

## Code Conventions
- Python: Follow ruff/flake8 rules, use type hints
- Imports: Use `from __future__ import annotations`
- Models: Use Pydantic v2 for validation
- API: FastAPI with async endpoints
- DB: SQLAlchemy 2.0 async with Alembic migrations
- Tests: Write both pytest unit tests and Robot Framework acceptance tests

## Testing Requirements
- Unit tests for all domain models (pytest)
- Unit tests for all crypto operations (pytest + hypothesis)
- Integration tests for API endpoints (pytest + httpx)
- Robot Framework tests for API acceptance
- OWASP Top 10 security tests (Robot Framework)
- SAST scanning (Bandit, Semgrep)
- DAST scanning (OWASP ZAP)
- Dependency scanning (Safety, Trivy)
- Secret scanning (Gitleaks)

## Key Directories
- `src/stie/` - Main source code
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/robot/` - Robot Framework tests
- `tests/security/` - OWASP security tests
- `.github/workflows/` - CI/CD pipelines
- `docs/` - Documentation
- `helm/` - Kubernetes Helm chart
- `k8s/` - Kubernetes manifests
