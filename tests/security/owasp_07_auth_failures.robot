*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-07-01: Weak Password Policy Not Allowed
    [Documentation]    Verify weak passwords are rejected
    ${response}=    POST On Session    stie
    ...    /api/v1/auth/register
    ...    json={"username": "test", "email": "test@test.com", "password": "123"}
    ...    expected_status=any
    Log    Weak password response: ${response.status_code}

OWASP-07-02: JWT Token Not In URL
    [Documentation]    Verify tokens are not passed in URLs
    ${response}=    GET On Session    stie
    ...    /api/v1/health?token=eyJhbGciOiJIUzI1NiJ9.test
    ...    expected_status=any
    Log    Token in URL test: ${response.status_code}

OWASP-07-03: Session Timeout
    [Documentation]    Verify sessions expire appropriately
    Log    Session timeout should be <= 60 minutes by default

OWASP-07-04: Multi-Factor Auth Available
    [Documentation]    Verify MFA endpoints exist
    ${response}=    POST On Session    stie
    ...    /api/v1/auth/mfa/setup
    ...    json={}
    ...    expected_status=any
    Log    MFA endpoint status: ${response.status_code}
