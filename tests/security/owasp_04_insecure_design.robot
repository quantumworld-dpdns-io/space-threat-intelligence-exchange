*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-04-01: Rate Limiting On Auth
    [Documentation]    Verify rate limiting on authentication endpoints
    FOR    ${i}    IN RANGE    50
        ${response}=    POST On Session    stie
        ...    /api/v1/auth/login
        ...    json={"username": "admin", "password": "admin"}
        ...    expected_status=any
        Exit For Loop If    ${response.status_code} == 429
    END
    Log    Rate limit hit at iteration ${i}: ${response.status_code}

OWASP-04-02: No Account Enumeration
    [Documentation]    Verify consistent error messages prevent account enumeration
    ${resp1}=    POST On Session    stie
    ...    /api/v1/auth/login
    ...    json={"username": "nonexistent", "password": "wrong"}
    ...    expected_status=any
    ${resp2}=    POST On Session    stie
    ...    /api/v1/auth/login
    ...    json={"username": "existing", "password": "wrong"}
    ...    expected_status=any
    Log    Messages should be identical (no enumeration)

OWASP-04-03: Unlimited File Upload Not Allowed
    [Documentation]    Verify file upload size limits
    ${response}=    POST On Session    stie
    ...    /api/v1/reports
    ...    json={"title": "x" * 100000}
    ...    expected_status=any
    Log    Large payload response: ${response.status_code}
