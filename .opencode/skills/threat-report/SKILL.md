---
name: threat-report
description: Create, sign, and submit space threat intelligence reports for satellite intrusions and GNSS spoofing
---

# Threat Report Skill

Create cryptographically signed threat reports for the Space Threat Intelligence Exchange.

## Workflow

1. **Gather Information**
   - Threat type (satellite_intrusion, gnss_spoofing, signal_jamming, etc.)
   - Severity (critical, high, medium, low, info)
   - Confidence level
   - TLP classification
   - Affected satellites/systems
   - Observables (IPs, domains, hashes)
   - Timeframe

2. **Create Report**
   ```python
   from stie.models.threat_report import ThreatReportCreate
   
   report = ThreatReportCreate(
       title="Suspicious Uplink Activity",
       description="Detailed description...",
       threat_type="satellite_intrusion",
       severity="high",
       ...
   )
   ```

3. **Sign Report**
   ```bash
   stie sign report.json key.priv.pem
   ```

4. **Submit Report**
   ```bash
   stie submit report.signed.json
   ```

## Validation Checklist
- [ ] All required fields populated
- [ ] Threat type matches domain taxonomy
- [ ] TLP level appropriate for sensitivity
- [ ] Observables formatted correctly
- [ ] Report signed with valid key
- [ ] References included where applicable

## References
- `src/stie/models/threat_report.py` - Data models
- `src/stie/crypto/signing.py` - Signing utilities
- `src/stie/cli/entry.py` - CLI commands
