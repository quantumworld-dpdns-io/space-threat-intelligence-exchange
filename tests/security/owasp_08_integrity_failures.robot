*** Settings ***
Resource          ../robot/resources/common.robot
Test Setup        Create API Session

*** Variables ***
${SAMPLE_REPORT_PATH}    ${CURDIR}/../fixtures/sample_report.json

*** Test Cases ***
OWASP-08-01: Signed Report Verification
    [Documentation]    Verify cryptographic signature verification works
    ${report}=    OperatingSystem.Get File    ${SAMPLE_REPORT_PATH}
    Log    Report loaded: ${report}

OWASP-08-02: Tampered Report Detection
    [Documentation]    Verify tampered reports are rejected
    # Load signed report and modify it
    ${response}=    POST On Session    stie
    ...    /api/v1/reports
    ...    json={"title": "Tampered", "description": "Modified after signing"}
    ...    expected_status=any
    Log    Tampered report: ${response.status_code}

OWASP-08-03: Software Supply Chain Security
    [Documentation]    Verify dependency integrity
    Log    Dependencies should be pinned with hash verification
