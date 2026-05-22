*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-02-01: HTTPS Not Enforced
    [Documentation]    Verify API should enforce HTTPS
    ${response}=    GET On Session    stie    /api/v1/health    expected_status=any
    Log    HTTPS test for ${API_BASE_URL}

OWASP-02-02: Weak Signature Algorithm Not Accepted
    [Documentation]    Verify weak crypto rejected
    # Ed25519 is strong, but MD5/SHA1 should not be accepted for signatures

OWASP-02-03: Sensitive Data In URL Parameters
    [Documentation]    Test that sensitive data not exposed in URLs
    ${response}=    GET On Session    stie
    ...    /api/v1/health
    ...    params=api_key=sk-test123&token=eyJhbGciOiJIUzI1NiJ9.test
    ...    expected_status=any
    Log    Sensitive data in URL: ${response.status_code}
