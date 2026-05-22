*** Settings ***
Library           RequestsLibrary
Library           Collections
Variables         ../config.py

*** Keywords ***
Create API Session
    [Arguments]    ${base_url}=${API_BASE_URL}
    Create Session    stie    ${base_url}    verify=True
    Log    Created API session to ${base_url}

Health Check Should Succeed
    ${response}=    GET On Session    stie    /api/v1/health
    Should Be Equal As Numbers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[status]    ok
    RETURN    ${response.json()}

Report Should Exist
    [Arguments]    ${report_id}
    ${response}=    GET On Session    stie    /api/v1/reports/${report_id}    expected_status=any
    RETURN    ${response.status_code}

Generate Random ID
    ${uuid}=    Generate Random String    12    [LOWER]
    RETURN    STIE-TEST-${uuid}

Validate Report Schema
    [Arguments]    ${report}
    Dictionary Should Contain Key    ${report}    id
    Dictionary Should Contain Key    ${report}    title
    Dictionary Should Contain Key    ${report}    threat_type
    Dictionary Should Contain Key    ${report}    severity
    Dictionary Should Contain Key    ${report}    author_id
    Dictionary Should Contain Key    ${report}    created_at

Wait For Service
    [Arguments]    ${timeout}=30    ${interval}=2
    ${elapsed}=    Set Variable    0
    FOR    ${i}    IN RANGE    ${timeout}
        ${status}=    Run Keyword And Return Status    Health Check Should Succeed
        Return From Keyword If    ${status}
        Sleep    ${interval}
    END
    Fail    Service did not become healthy within ${timeout} seconds
