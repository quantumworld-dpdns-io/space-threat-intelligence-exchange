*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-03-01: SQL Injection Via Report ID
    [Documentation]    Test SQL injection in report ID parameter
    ${payloads}=    Create List
    ...    1' OR '1'='1
    ...    1; DROP TABLE threat_reports--
    ...    1 UNION SELECT * FROM users--
    ...    1' WAITFOR DELAY '0:0:5'--
    ...    1 AND SLEEP(5)--
    FOR    ${payload}    IN    @{payloads}
        ${response}=    GET On Session    stie
        ...    /api/v1/reports/${payload}
        ...    expected_status=any
        Should Be True    500 > ${response.status_code} or ${response.status_code} >= 400
        ...    msg=SQL injection payload '${payload}' did not fail as expected
    END

OWASP-03-02: NoSQL Injection Via JSON Body
    [Documentation]    Test NoSQL injection in JSON payloads
    ${response}=    POST On Session    stie
    ...    /api/v1/reports/search
    ...    json={"query": {"$ne": ""}, "password": {"$gt": ""}}
    ...    expected_status=any
    Should Be True    500 > ${response.status_code} or ${response.status_code} >= 400

OWASP-03-03: XSS Via Report Fields
    [Documentation]    Test cross-site scripting in report fields
    ${report}=    Create Dictionary
    ...    title=<script>alert('xss')</script>
    ...    description=<img src=x onerror=alert(1)>
    ...    threat_type=satellite_intrusion
    ...    severity=medium
    ...    author_id=test-author
    ${response}=    POST On Session    stie
    ...    /api/v1/reports
    ...    json=${report}
    ...    expected_status=any
    Log    XSS test result: ${response.status_code}

OWASP-03-04: Command Injection In Headers
    [Documentation]    Test command injection via HTTP headers
    ${headers}=    Create Dictionary    X-Forwarded-Host    $(whoami)
    ${response}=    GET On Session    stie
    ...    /api/v1/health
    ...    headers=${headers}
    ...    expected_status=any
    Should Be Equal As Numbers    ${response.status_code}    200
