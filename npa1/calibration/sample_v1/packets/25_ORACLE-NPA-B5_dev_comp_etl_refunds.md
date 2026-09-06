# Packet 25 | ORACLE-NPA-B5 | dev_comp_etl_refunds | run 1
class=COMPOSITE_TASK gold_route=TASK

## BRIEF
Extract: all 2024 order rows; PAID positive, REFUND negative. Load: sum per customer; keep net>=1000.

## ARTIFACT
Extract only status='PAID' 2024. Load sums extracted with HAVING >=1000.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "extract includes REFUND",
    "load sees both"
  ],
  "stage2_material_failures": [
    "extract drops REFUND rows required by load net"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Correct net customer totals including refunds.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Net customer totals for 2024 are accurately calculated by aggregating positive PAID amounts and negative REFUND amounts per customer, retaining only those with a net total >= 1000.",
  "parts": [
    {
      "component": "Extraction Stage",
      "local_contribution": "Extract all 2024 order records including both PAID (positive) and REFUND (negative) statuses."
    },
    {
      "component": "Extraction-to-Aggregation Interface",
      "local_contribution": "Handoff complete set of order status rows and signed amounts to the aggregation component."
    },
    {
      "component": "Aggregation and Load Stage",
      "local_contribution": "Aggregate signed amounts per customer and filter for net totals >= 1000."
    }
  ],
  "material_failures": [
    "Artifact Extraction stage filters status='PAID' only, excluding status='REFUND' records from extraction.",
    "Interface handoff passes gross paid amounts instead of signed net amounts.",
    "Aggregation stage applies HAVING >= 1000 to gross paid amounts rather than net amounts, incorrectly including customers whose net total after refunds is below 1000."
  ],
  "requirements": [
    "Extraction query must extract all 2024 order rows with status in ('PAID', 'REFUND').",
    "Order amounts for REFUND status must be treated as negative values in customer net sum calculations.",
    "Aggregation stage must compute sum of (PAID - REFUND) per customer.",
    "HAVING filter must enforce net total >= 1000 per customer prior to loading."
  ],
  "tests": [
    "Verify extraction filter does not restrict order status to 'PAID' only.",
    "Verify refund order amounts are subtracted from paid order amounts during aggregation.",
    "Verify loaded customer records have net total (PAID - REFUND) >= 1000."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}