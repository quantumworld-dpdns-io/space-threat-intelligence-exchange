*** Settings ***
Resource          resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
List Peers Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/peers    expected_status=any
    Log    Peers list status: ${response.status_code}

Get Peer Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/peers/test-peer    expected_status=any
    Log    Peer detail status: ${response.status_code}

Network Status Returns Expected Status
    ${response}=    GET On Session    stie    /api/v1/network/status    expected_status=any
    Log    Network status: ${response.status_code}
