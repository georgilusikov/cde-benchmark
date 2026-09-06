# Packet 24 | ORACLE-NPA-B5 | dev_clear_pii_log_redact | run 1
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
  "intended_outcome": "Logs comply with PII redaction standard.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": [
    "Log entries contain no raw PAN or SSN plaintext strings.",
    "Non-sensitive operational log metadata (e.g., user ID, transaction status) is preserved."
  ],
  "parts": [
    {
      "name": "Payment Log Emitter",
      "local_contribution": "Constructs and dispatches payment operation log events."
    },
    {
      "name": "PII Sanitization Filter",
      "local_contribution": "Scans and redacts sensitive data (PAN, SSN) from log messages prior to output."
    },
    {
      "name": "Log Output Sink",
      "local_contribution": "Persists and outputs the finalized log records."
    }
  ],
  "material_failures": [
    {
      "component": "PII Sanitization Filter",
      "description": "Log artifact contains plaintext SSN ('ssn=123-45-6789') violating non-exposure rule."
    },
    {
      "component": "PII Sanitization Filter",
      "description": "Log artifact contains plaintext PAN ('pan=4111111111111111') violating non-exposure rule."
    },
    {
      "interface": "Payment Log Emitter -> PII Sanitization Filter",
      "description": "Raw PII passed into logging stream without pre-formatting mask or active sanitization interceptor."
    }
  ],
  "requirements": [
    {
      "id": "REQ-PII-01",
      "component": "PII Sanitization Filter",
      "description": "Must detect and redact Social Security Number patterns (e.g., XXX-XX-XXXX) before writing log records."
    },
    {
      "id": "REQ-PII-02",
      "component": "PII Sanitization Filter",
      "description": "Must detect and redact Primary Account Number patterns (e.g., 16-digit card numbers) before writing log records."
    },
    {
      "id": "REQ-PII-03",
      "component": "Payment Log Emitter",
      "description": "Must sanitize or pass structured parameters through redaction middleware prior to log line emission."
    }
  ],
  "tests": [
    {
      "id": "TEST-PII-01",
      "target_requirement": "REQ-PII-01",
      "description": "Assert that logging an input string containing 'ssn=123-45-6789' outputs 'ssn=[REDACTED]' or equivalent masked string."
    },
    {
      "id": "TEST-PII-02",
      "target_requirement": "REQ-PII-02",
      "description": "Assert that logging an input string containing 'pan=4111111111111111' outputs 'pan=[REDACTED]' or equivalent masked string."
    }
  ],
  "evidence_gaps": [],
  "decision_readiness": "READY"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}