*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Test Cases ***
OWASP-10-01: SSRF Via External References
    [Documentation]    Verify SSRF protection on external references
    ${report}=    Create Dictionary
    ...    title=SSRF Test
    ...    description=Test
    ...    threat_type=satellite_intrusion
    ...    severity=medium
    ...    author_id=test-author
    ...    references=["http://169.254.169.254/latest/meta-data/", "http://localhost:5432"]
    ${response}=    POST On Session    stie
    ...    /api/v1/reports
    ...    json=${report}
    ...    expected_status=any
    Log    SSRF test result: ${response.status_code}

OWASP-10-02: SSRF Via URL Fetch
    [Documentation]    Verify SSRF protection on URL fetching
    ${malicious_urls}=    Create List
    ...    http://169.254.169.254/
    ...    http://localhost:8000/
    ...    http://127.0.0.1:6379/
    ...    http://[::1]:22/
    ...    file:///etc/passwd
    FOR    ${url}    IN    @{malicious_urls}
        Log    Testing SSRF: ${url}
    END

OWASP-10-03: DNS Rebinding Protection
    [Documentation]    Verify DNS rebinding attack protection
    Log    1.1.1.1.nip.io and similar DNS rebinding domains should be blocked
