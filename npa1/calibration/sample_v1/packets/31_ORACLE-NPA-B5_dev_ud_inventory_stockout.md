# Packet 31 | ORACLE-NPA-B5 | dev_ud_inventory_stockout | run 1
class=UNDERDETERMINED_PROBLEM gold_route=PROBLEM

## BRIEF
Stockout rate doubled on SKU-17. Could be demand spike OR supply delay OR warehouse location mis-slot. Request: expedite air freight from supplier.

## ARTIFACT
PO: expedite air freight SKU-17.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Demand vs inbound supply vs internal slotting loss.",
  "valid_models": [
    {
      "id": "A_demand",
      "description": "true demand spike",
      "implied_action": "more inbound"
    },
    {
      "id": "A_supply",
      "description": "supplier late",
      "implied_action": "expedite freight"
    },
    {
      "id": "A_slot",
      "description": "units exist but mis-slotted/unfindable",
      "implied_action": "cycle count/reslot not freight"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_onhand_inbound",
      "description": "on-hand by location + inbound ASN ETA vs sales velocity",
      "aliases": [
        "cycle count SKU-17",
        "ASN status vs demand"
      ],
      "evidence_returned": "System on-hand 0 but cycle count finds 420 units in wrong aisle; inbound ASN on time; demand +8% only."
    }
  ],
  "forbidden_premature_commitments": [
    "expedite air freight as committed primary fix without on-hand check"
  ],
  "stage2_requirements": [
    "reslot/cycle-count process",
    "do not expedite freight as primary"
  ],
  "stage2_material_failures": [
    "mis-slot hides available units"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "End stockouts for SKU-17 by identifying and addressing the true constraint.",
  "route": "PROBLEM",
  "supra_goal": "Maintain inventory availability and eliminate stockouts for SKU-17.",
  "model_gap": "Uncertainty regarding the true root cause of the doubled stockout rate (demand surge vs. supplier delay vs. warehouse mis-slotting), rendering the expedited air freight request unvalidated.",
  "competing_models": [
    "Model 1 (Demand Spike): Outbound customer demand unexpectedly surged beyond forecasted capacity.",
    "Model 2 (Supply Delay): Supplier lead times or transit times increased, delaying inbound fulfillment.",
    "Model 3 (Warehouse Mis-slot): Physical stock exists in the facility but is misplaced or incorrectly recorded in the WMS."
  ],
  "probe": "Perform an immediate physical bin audit/WMS count reconciliation for SKU-17 in parallel with reviewing recent sales velocity and supplier lead-time logs.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Physical inventory reconciliation data for SKU-17",
    "Recent outbound demand velocity trends for SKU-17",
    "Supplier dispatch and transit lead-time logs"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
System on-hand 0 but cycle count finds 420 units in wrong aisle; inbound ASN on time; demand +8% only.

## AGENT STAGE2
{
  "intended_outcome": "End stockouts for SKU-17 by resolving inventory mis-location and WMS system discrepancies.",
  "route": "PROBLEM",
  "supra_goal": "Maintain inventory availability and eliminate stockouts for SKU-17.",
  "model_gap": "Uncertainty regarding the operational root cause of the misplaced 420 units (human putaway scanning omission vs. WMS location mapping/sync bug), preventing verified systemic corrective action.",
  "competing_models": [
    "Model 1 (Putaway Execution Failure): Warehouse staff physically moved stock to an unassigned aisle without completing the location scan in the WMS.",
    "Model 2 (WMS System Error): Location scan was performed, but a system sync failure or mapping error prevented available on-hand inventory from updating."
  ],
  "probe": "Audit RF putaway transaction logs and operator task execution history for the 420-unit batch of SKU-17.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "RF scan transaction history for receiving/putaway of SKU-17",
    "WMS task execution logs and bin transfer records"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}