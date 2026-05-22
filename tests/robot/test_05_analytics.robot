*** Settings ***
Resource          resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
Analytics Summary Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/analytics/summary    expected_status=any
    Log    Analytics summary status: ${response.status_code}

Analytics Trends Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/analytics/trends    expected_status=any
    Log    Analytics trends status: ${response.status_code}

Analytics Clusters Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/analytics/clusters    expected_status=any
    Log    Analytics clusters status: ${response.status_code}
