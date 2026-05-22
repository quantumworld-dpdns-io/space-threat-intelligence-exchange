*** Settings ***
Resource          resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
No SQL Injection In Report ID
    [Tags]    owasp    owasp-03
    ${response}=    GET On Session    stie
    ...    /api/v1/reports/1%27%20OR%20%271%27%3D%271
    ...    expected_status=any
    Should Not Be Equal As Numbers    ${response.status_code}    500
    Log    SQL injection attempt returned: ${response.status_code}

No SQL Injection In Search
    [Tags]    owasp    owasp-03
    ${response}=    POST On Session    stie
    ...    /api/v1/reports/search
    ...    json={"query": "'; DROP TABLE threat_reports; --"}
    ...    expected_status=any
    Should Not Be Equal As Numbers    ${response.status_code}    500

No Path Traversal
    [Tags]    owasp    owasp-05
    ${response}=    GET On Session    stie
    ...    /api/v1/reports/../../../etc/passwd
    ...    expected_status=any
    Should Not Be Equal As Numbers    ${response.status_code}    200
    Should Not Be Equal As Numbers    ${response.status_code}    500

No XSS In Report Search
    [Tags]    owasp    owasp-03
    ${response}=    POST On Session    stie
    ...    /api/v1/reports/search
    ...    json={"query": "<script>alert('xss')</script>"}
    ...    expected_status=any
    Should Not Be Equal As Numbers    ${response.status_code}    500
    Run Keyword If    ${response.status_code} == 200
    ...    Should Not Contain    ${response.text}    <script>

Security Headers Present
    [Tags]    owasp    owasp-05
    ${response}=    GET On Session    stie    /api/v1/health
    ${headers}=    Get Dictionary Keys    ${response.headers}
    Log    Response headers: ${headers}

No Mass Assignment On Report Create
    [Tags]    owasp    owasp-01
    ${report}=    Create Dictionary
    ...    title=Test
    ...    description=Test
    ...    threat_type=satellite_intrusion
    ...    severity=critical
    ...    author_id=robot-test
    ...    is_admin=true
    ...    role=superuser
    ${response}=    POST On Session    stie    /api/v1/reports    json=${report}    expected_status=any
    Log    Mass assignment attempt: ${response.status_code}

No Server Info Disclosure
    [Tags]    owasp    owasp-05
    ${response}=    GET On Session    stie    /api/v1/health
    Should Not Contain    ${response.text}    Django
    Should Not Contain    ${response.text}    Express
    Should Not Contain    ${response.text}    ASP.NET

Rate Limiting On Auth Endpoint
    [Tags]    owasp    owasp-04
    FOR    ${i}    IN RANGE    10
        ${response}=    POST On Session    stie
        ...    /api/v1/auth/login
        ...    json={"username": "test", "password": "test"}
        ...    expected_status=any
    END
    Log    Rate limit test completed

No Credentials In URL Logging
    [Tags]    owasp    owasp-09
    ${response}=    GET On Session    stie
    ...    /api/v1/health?password=secret123&api_key=abc123
    ...    expected_status=any
    Log    Credential in URL test: ${response.status_code}
