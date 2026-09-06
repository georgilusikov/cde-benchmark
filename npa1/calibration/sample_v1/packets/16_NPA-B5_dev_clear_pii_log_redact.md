# Packet 16 | NPA-B5 | dev_clear_pii_log_redact | run 1
class=CLEAR_TASK gold_route=TASK

## BRIEF
Logging standard: never write raw PAN/SSN to logs. Artifact log line includes ssn=123-45-6789 and pan=4111111111111111 in plaintext.

## ARTIFACT
INFO payment user=42 ssn=123-45-6789 pan=4111111111111111 status=ok

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "redact/tokenize SSN and PAN",
    "reject log sinks that emit raw PII"
  ],
  "stage2_material_failures": [
    "raw SSN and PAN present in log"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Logs comply with PII redaction standard by ensuring raw SSN and PAN plaintext values are never written to log outputs.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": null,
  "probe": null,
  "success": "All log output emitted by the system contains zero raw SSN or PAN plaintext values, strictly complying with the PII redaction logging standard.",
  "parts": [
    {
      "name": "Log Event Formatter",
      "local_contribution": "Captures event attributes (user ID, SSN, PAN, status) and constructs structured log payloads for processing."
    },
    {
      "name": "PII Redaction Filter",
      "local_contribution": "Scans log payloads to detect and replace raw SSN and PAN plaintext patterns with redacted placeholders."
    },
    {
      "name": "Log Writer / Output Sink",
      "local_contribution": "Persists or streams sanitized log messages to the target destination without leaking unredacted data."
    }
  ],
  "material_failures": [
    "Redaction Filter failure: Pattern matching fails to identify raw SSN ('123-45-6789') or raw PAN ('4111111111111111'), leaving plaintext PII in emitted logs.",
    "Pipeline routing failure: Log Formatter bypasses the Redaction Filter and sends unredacted payload directly to Log Writer.",
    "Interface handoff failure: Log Formatter encodes payload in a format that obscures PII structure from the Redaction Filter, causing the filter to pass raw PII through to the Log Writer."
  ],
  "requirements": [
    "The Redaction Filter must inspect all log payloads and sanitize raw SSN (e.g., matching '\\d{3}-\\d{2}-\\d{4}') and raw PAN (e.g., matching '\\d{13,19}') into masked or redacted forms before emission.",
    "The logging framework must enforce that 100% of log entries route through the Redaction Filter prior to reaching the Log Writer.",
    "The logging pipeline must fail safe (suppress log or redact entire entry) if redaction processing throws an exception or fails."
  ],
  "tests": [
    "Unit Test (Redaction Filter): Verify that passing 'INFO payment user=42 ssn=123-45-6789 pan=4111111111111111 status=ok' outputs text with '123-45-6789' and '4111111111111111' replaced by redacted tokens.",
    "Integration Test (Pipeline Routing): Verify that log emission calls across all log severity levels route payload through the Redaction Filter before output sink write.",
    "Negative Test (Fail-Safe Handoff): Verify that if the Redaction Filter encounters invalid encoding or execution errors, raw PII is suppressed and not written to output."
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}