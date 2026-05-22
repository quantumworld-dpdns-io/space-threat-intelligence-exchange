from __future__ import annotations

from typing import Any

from stie.ai.client import llm_client


ENRICHMENT_SYSTEM_PROMPT = """You are a space threat intelligence analyst. Given a threat report, provide enrichment including:
1. Potential threat actor attribution
2. Related tactics and techniques (MITRE ATT&CK for Space)
3. Severity justification
4. Recommended detection and mitigation actions
5. Links to known vulnerabilities or campaigns

Provide your analysis in a structured JSON format."""


async def enrich_threat_report(report_text: str) -> dict[str, Any]:
    prompt = f"Analyze and enrich the following space threat intelligence report:\n\n{report_text}"
    response = await llm_client.complete(prompt, system_prompt=ENRICHMENT_SYSTEM_PROMPT)
    return {"raw_enrichment": response, "model": llm_client.model}


async def summarize_threat_report(report_text: str) -> str:
    prompt = f"Provide a concise 3-sentence summary of this space threat report:\n\n{report_text}"
    return await llm_client.complete(prompt)


CLASSIFICATION_PROMPT = """Classify the following space threat report. Return a JSON object with:
- threat_type: one of [satellite_intrusion, gnss_spoofing, signal_jamming, command_hijack, telemetry_tampering, dos_attack, supply_chain, physical_attack, other]
- severity: one of [critical, high, medium, low, info]
- confidence: one of [high, medium, low, unknown]
- tlp_level: one of [red, amber, green, clear]"""


async def classify_threat(report_text: str) -> dict[str, str]:
    prompt = f"{CLASSIFICATION_PROMPT}\n\nReport:\n{report_text}"
    response = await llm_client.complete(prompt)
    return {"classification": response}
