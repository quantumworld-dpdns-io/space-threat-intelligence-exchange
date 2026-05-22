*** Settings ***
Resource          resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
API Health Check Should Return OK
    ${response}=    GET On Session    stie    /api/v1/health
    Status Should Be    200
    Should Be Equal    ${response.json()}[status]    ok
    Should Contain    ${response.json()}    version
    Should Contain    ${response.json()}    timestamp

API Health Check Returns Version
    ${response}=    GET On Session    stie    /api/v1/health
    Should Match Regexp    ${response.json()}[version]    ^\\d+\\.\\d+\\.\\d+$

API Health Check Returns Valid Timestamp
    ${response}=    GET On Session    stie    /api/v1/health
    Should Contain    ${response.json()}[timestamp]    T

Unauthenticated Request Returns Appropriate Status
    ${response}=    GET On Session    stie    /api/v1/reports    expected_status=any
    Log    Status: ${response.status_code}

API Root Should Return 404
    ${response}=    GET On Session    stie    /    expected_status=any
    Should Be Equal As Numbers    ${response.status_code}    404

Rate Limiting Headers Present
    ${response}=    GET On Session    stie    /api/v1/health
    Should Contain    ${response.headers}    x-request-id
