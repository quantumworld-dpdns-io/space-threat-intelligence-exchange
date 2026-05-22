---
name: security-test
description: Write and run OWASP Top 10 security tests using Robot Framework
---

# Security Test Skill

Write OWASP Top 10 security tests for the Space Threat Intelligence Exchange API.

## OWASP Top 10 Test Categories

1. **Broken Access Control** - Test missing auth, privilege escalation, IDOR
2. **Cryptographic Failures** - Test weak crypto, sensitive data exposure
3. **Injection** - Test SQL, NoSQL, XSS, command injection
4. **Insecure Design** - Test rate limiting, account enumeration
5. **Security Misconfiguration** - Test CORS, debug mode, default creds
6. **Vulnerable Components** - Test dependency scanning
7. **Auth Failures** - Test weak passwords, token handling
8. **Integrity Failures** - Test signature verification
9. **Logging Failures** - Test audit logging
10. **SSRF** - Test server-side request forgery

## Running Tests

```bash
# Run all security tests
make test-security

# Run specific OWASP test
robot tests/security/owasp_03_injection.robot

# Run with report
robot --outputdir reports/security tests/security/
```

## Test Convention
- Use Robot Framework with RequestsLibrary
- Each OWASP category has its own test file
- Tests should be idempotent
- Tag tests with `owasp-XX` for traceability

## References
- `tests/security/` - Security test directory
- `tests/robot/` - Robot Framework resources
- OWASP Top 10 - 2021 edition
