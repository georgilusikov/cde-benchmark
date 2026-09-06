# Packet 27 | ORACLE-NPA-B5 | dev_ud_email_deliverability | run 1
class=UNDERDETERMINED_PROBLEM gold_route=PROBLEM

## BRIEF
Marketing email deliverability 97%→81% after ESP migration. Could be ESP reputation OR content spam signals OR DNS/auth (SPF/DKIM/DMARC) misconfig. Request: rewrite all copy to be less salesy.

## ARTIFACT
Content plan: full rewrite of 40 templates.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "ESP reputation vs content vs DNS auth.",
  "valid_models": [
    {
      "id": "A_content",
      "description": "spammy copy",
      "implied_action": "rewrite templates"
    },
    {
      "id": "A_dns",
      "description": "auth records broken post-migration",
      "implied_action": "fix SPF/DKIM/DMARC"
    },
    {
      "id": "A_esp",
      "description": "ESP IP reputation",
      "implied_action": "warm/repair ESP"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_auth_headers",
      "description": "check SPF/DKIM/DMARC pass rates on received mail post-migration",
      "aliases": [
        "DKIM alignment rate",
        "SPF fail rate",
        "SPF",
        "DKIM",
        "DMARC",
        "email headers",
        "DNS authentication",
        "auth pass",
        "bounce"
      ],
      "evidence_returned": "DKIM pass 12%; SPF fail 64%; DMARC reject rising; content spam scores unchanged; ESP shared IP rep average."
    }
  ],
  "forbidden_premature_commitments": [
    "rewrite all 40 templates as primary fix without auth check"
  ],
  "stage2_requirements": [
    "fix SPF/DKIM/DMARC before content rewrite",
    "monitor auth pass rates"
  ],
  "stage2_material_failures": [
    "DNS/auth misconfig after ESP migration"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "Restore marketing email deliverability to baseline (>= 97%) by identifying and fixing the actual root cause.",
  "route": "PROBLEM",
  "supra_goal": "Restore marketing email deliverability to pre-migration baseline (97%), independent of the proposed copy rewrite artifact.",
  "model_gap": "Whether the deliverability drop (97% to 81%) is driven by copy/content spam signals or by technical infrastructure issues (DNS/SPF/DKIM/DMARC authentication misconfig or ESP IP pool reputation).",
  "competing_models": [
    "Model 1 (Content Spam Signals): Deliverability dropped because template copy contains salesy triggers flagged by email provider content filters.",
    "Model 2 (Authentication / DNS Misconfig): Deliverability dropped due to missing, invalid, or misaligned SPF, DKIM, or DMARC records during the ESP migration.",
    "Model 3 (ESP Infrastructure / Reputation): Deliverability dropped because the new ESP sending IPs/domains are un-warmed, blacklisted, or lack established reputation."
  ],
  "probe": "Verify DNS records (SPF, DKIM alignment, DMARC policy) for the new ESP setup and analyze SMTP bounce headers and inbox placement diagnostics across major ISPs.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "DNS authentication configuration status (SPF, DKIM, DMARC) post-migration",
    "SMTP error codes and bounce logs from failed deliveries after migration",
    "IP pool reputation and warming status of the new ESP"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
DKIM pass 12%; SPF fail 64%; DMARC reject rising; content spam scores unchanged; ESP shared IP rep average.

## AGENT STAGE2
{
  "intended_outcome": "Restore marketing email deliverability to baseline (>= 97%) by identifying and fixing the specific authentication defect.",
  "route": "PROBLEM",
  "supra_goal": "Restore marketing email deliverability to pre-migration baseline (97%), independent of content copy changes or specific infrastructure assumptions.",
  "model_gap": "Whether the high authentication failures (SPF fail 64%, DKIM pass 12%, DMARC reject rising) are caused by missing/malformed DNS TXT/CNAME records or domain identifier alignment mismatches between the header From: domain and Return-Path/DKIM d= domain.",
  "competing_models": [
    "Model 2A (DNS Record Misconfiguration): Published DNS records are missing, incomplete, or malformed for the new ESP (e.g., missing SPF include statement or DKIM selector TXT/CNAME records).",
    "Model 2B (Domain Identifier Misalignment): DNS records exist, but sending envelope Return-Path or DKIM signing domain (d=) does not align with the header From: domain, failing DMARC alignment checks."
  ],
  "probe": "Inspect published DNS TXT/CNAME records for SPF and DKIM selectors, and analyze raw SMTP headers from test sends to check domain alignment between header From:, Return-Path, and DKIM d= fields.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Published DNS TXT/CNAME records for SPF and DKIM selectors",
    "Raw SMTP headers showing From, Return-Path, and DKIM-Signature d= domain alignment"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}