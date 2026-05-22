# Agent Context for Space Threat Intelligence Exchange

## Project
Decentralized CTI sharing for satellite intrusions and GNSS spoofing via signed threat reports.

## Quick Start
```bash
make install   # Install dependencies
make dev       # Start dev environment
make test      # Run all tests
```

## Key Files
- `src/stie/` - Python backend source
- `tests/robot/` - Robot Framework acceptance tests
- `tests/security/` - OWASP Top 10 security tests
- `.github/workflows/` - CI/CD pipelines
- `.opencode/skills/` - Agent skills
- `mcp_server/` - MCP server for AI tool integration

## Architecture
- **API**: FastAPI async endpoints
- **DB**: PostgreSQL (primary), Redis (cache), Qdrant (vectors)
- **Analytics**: DuckDB, Apache Arrow, DataFusion, Iceberg, Trino
- **AI**: Ollama/vLLM for LLM, W&B Weave for observability
- **P2P**: libp2p-based decentralized sharing
- **Crypto**: Ed25519 signed reports

## Testing Stack
- pytest: Unit & integration tests
- Robot Framework: API acceptance & OWASP security tests
- Hypothesis: Property-based crypto tests
- Locust: Performance/load testing
- Bandit/Semgrep: SAST scanning
- OWASP ZAP: DAST scanning
- Safety/Trivy: Dependency & container scanning

## CI/CD
- CI: lint, typecheck, unit, integration, robot, security, docker
- CD: staging on main push, production on release
- Security: weekly scheduled scans, dependency review
- Performance: weekly load tests

## Development
- Branch: `dev` (active), `main` (protected)
- Commits: atomic, one feature per commit
- Hooks: pre-commit (ruff, mypy, bandit)
