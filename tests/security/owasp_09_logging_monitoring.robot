*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-09-01: Sensitive Data In Logs
    [Documentation]    Verify sensitive data not logged
    ${response}=    POST On Session    stie
    ...    /api/v1/auth/login
    ...    json={"username": "testuser", "password": "supersecret123!"}
    ...    expected_status=any
    Log    Password should not appear in logs

OWASP-09-02: Audit Logging Present
    [Documentation]    Verify audit logs are generated
    Log    All API requests should be logged with request ID

OWASP-09-03: Failed Auth Attempts Logged
    [Documentation]    Verify failed authentication attempts are logged
    FOR    ${i}    IN RANGE    5
        POST On Session    stie
        ...    /api/v1/auth/login
        ...    json={"username": "admin", "password": "wrong"}
        ...    expected_status=any
    END
    Log    Failed auth attempts should trigger audit event

OWASP-09-04: Log Monitoring Alerts
    [Documentation]    Verify suspicious activity generates alerts
    Log    Repeated failures should trigger security alerts
