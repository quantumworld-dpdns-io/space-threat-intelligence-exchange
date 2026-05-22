---
name: ci-pipeline
description: Manage GitHub Actions CI/CD pipelines for build, test, security, and deploy
---

# CI/CD Pipeline Skill

Manage continuous integration and deployment pipelines for the Space Threat Intelligence Exchange.

## Pipeline Stages

### CI (`.github/workflows/ci.yml`)
1. Lint & Format (ruff)
2. Type Check (mypy)
3. Unit Tests (pytest)
4. Integration Tests (pytest + PostgreSQL)
5. Robot Framework Tests
6. Security SAST (Bandit, Semgrep)
7. Dependency Scan (Safety)
8. Secret Scan (Gitleaks)
9. Docker Build & Trivy Scan

### CD (`.github/workflows/cd.yml`)
- Deploy to staging on main branch push
- Deploy to production on release

### Security (`.github/workflows/security.yml`)
- Weekly scheduled scans
- Dependency review on PRs
- CodeQL analysis
- Trivy filesystem scan
- OWASP ZAP DAST scan

### Performance (`.github/workflows/performance.yml`)
- Weekly load tests with Locust
- API benchmarks

## Adding a New Pipeline
1. Create `.github/workflows/<name>.yml`
2. Define trigger events
3. Add jobs with appropriate runners
4. Test with `act` locally

## References
- `.github/workflows/` - Pipeline definitions
- `Makefile` - Local CI commands
- Docker Compose for local test environment
