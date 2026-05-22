*** Settings ***
Documentation     OWASP-06: Vulnerable and Outdated Components
Library           OperatingSystem
Library           Process

*** Test Cases ***
OWASP-06-01: Dependency Scan With Safety
    [Documentation]    Scan Python dependencies for known vulnerabilities
    ${result}=    Run Process    safety    check    --json    cwd=${CURDIR}/../..
    Log    Safety scan output: ${result.stdout}
    Should Be Equal As Numbers    ${result.returncode}    0
    ...    msg=Dependency vulnerabilities found

OWASP-06-02: SAST Scan With Bandit
    [Documentation]    Scan source code for security issues
    ${result}=    Run Process    bandit    -r    ${CURDIR}/../../src    -f    json
    Log    Bandit scan output: ${result.stdout}
    Should Be Equal As Numbers    ${result.returncode}    0
    ...    msg=Security issues found in source code

OWASP-06-03: Secret Scan With Gitleaks
    [Documentation]    Scan repository for secrets
    ${result}=    Run Process    gitleaks    detect    --no-git    -v    cwd=${CURDIR}/../..
    Log    Gitleaks output: ${result.stdout}
    Should Be Equal As Numbers    ${result.returncode}    0
    ...    msg=Potential secrets found in repository
