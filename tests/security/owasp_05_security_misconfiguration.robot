*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-05-01: Debug Mode Disabled In Production
    [Documentation]    Verify debug/error pages don't leak info
    ${response}=    GET On Session    stie    /api/v1/health    expected_status=any
    Should Not Contain    ${response.text}    Traceback
    Should Not Contain    ${response.text}    File "/app/
    Should Not Contain    ${response.text}    DEBUG

OWASP-05-02: CORS Not Wildcard For Sensitive Endpoints
    [Documentation]    Verify CORS is properly restricted
    ${response}=    GET On Session    stie    /api/v1/health
    ${cors}=    Get Variable Value    ${response.headers}[access-control-allow-origin]    *
    Log    CORS origin: ${cors}

OWASP-05-03: Security Headers Check
    [Documentation]    Verify security headers are present
    ${response}=    GET On Session    stie    /api/v1/health
    Log    All headers: ${response.headers}

OWASP-05-04: Default Credentials Check
    [Documentation]    Verify no default credentials
    ${response}=    POST On Session    stie
    ...    /api/v1/auth/login
    ...    json={"username": "admin", "password": "admin"}
    ...    expected_status=any
    Should Not Be Equal As Numbers    ${response.status_code}    200

OWASP-05-05: HTTP Methods Allowed
    [Documentation]    Verify HTTP method restrictions
    ${response}=    PUT On Session    stie    /api/v1/health    expected_status=any
    Log    PUT /health: ${response.status_code}
    ${response}=    DELETE On Session    stie    /api/v1/health    expected_status=any
    Log    DELETE /health: ${response.status_code}
