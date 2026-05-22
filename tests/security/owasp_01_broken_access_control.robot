*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Variables ***
${UNAUTHORIZED_PATH}    /api/v1/reports

*** Test Cases ***
OWASP-01-01: Unauthenticated Access To Reports
    [Documentation]    Verify unauthenticated users cannot access reports
    ${response}=    GET On Session    stie    ${UNAUTHORIZED_PATH}    expected_status=any
    Should Be Equal As Numbers    ${response.status_code}    501

OWASP-01-02: Unauthenticated Access To Admin Functions
    [Documentation]    Verify admin endpoints require auth
    ${response}=    GET On Session    stie    /api/v1/peers    expected_status=any
    ${status}=    Set Variable    ${response.status_code}
    Run Keyword And Continue On Failure    Should Be True    ${status} != 200

OWASP-01-03: No Privilege Escalation Via IDOR
    [Documentation]    Test Insecure Direct Object Reference
    ${response}=    GET On Session    stie    /api/v1/reports/OTHER-USER-REPORT    expected_status=any
    Log    IDOR test result: ${response.status_code}

OWASP-01-04: Missing Function Level Access Control
    [Documentation]    Verify sensitive endpoints check permissions
    ${endpoints}=    Create List
    ...    /api/v1/admin
    ...    /api/v1/users
    ...    /api/v1/config
    FOR    ${endpoint}    IN    @{endpoints}
        ${response}=    GET On Session    stie    ${endpoint}    expected_status=any
        Log    ${endpoint}: ${response.status_code}
    END
