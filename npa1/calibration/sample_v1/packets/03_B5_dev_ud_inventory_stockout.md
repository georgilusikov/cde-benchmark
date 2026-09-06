# Packet 03 | B5 | dev_ud_inventory_stockout | run 1
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
  "SUCCESS": "Stockout rate on SKU-17 is reduced to baseline/zero by diagnosing and resolving the true operational constraint (whether demand spike, supply delay, or warehouse location mis-slot) without incurring unnecessary expedite costs.",
  "CONFIRMED MATERIAL FAILURES": "None confirmed within the artifact text itself ('PO: expedite air freight SKU-17'). The artifact accurately generates an expedite PO as requested in the brief. The lack of empirical proof confirming supply delay as the active bottleneck is an evidence gap rather than an intrinsic defect of the PO document.",
  "EVIDENCE GAPS / ASSUMPTIONS": "1. EVIDENCE GAP: Warehouse physical inventory audit / cycle count data for SKU-17 is missing (cannot rule out location mis-slotting).\n2. EVIDENCE GAP: Supplier lead-time logs and carrier tracking data for recent shipments are missing (cannot confirm supply delay).\n3. EVIDENCE GAP: Recent point-of-sale and sales order velocity data for SKU-17 are missing (cannot rule out demand spike).\n4. ASSUMPTION: The artifact assumes supply delay is the true constraint driving stockouts, bypassing verification of alternative candidate causes.",
  "REQUIREMENTS + TESTS": "COMPONENT 1: Constraint Diagnosis & Root-Cause Identification\n- Local Contribution: Isolate the true constraint driving stockouts prior to committing capital to remediation.\n- Requirement 1.1: Perform physical cycle count and WMS bin audit across pick, reserve, and receiving locations for SKU-17.\n- Test 1.1: Compare total physical count against system inventory to check for mis-slotted stock.\n- Requirement 1.2: Audit trailing 14-day sales velocity against forecast baseline.\n- Test 1.2: Flag demand spike if order volume exceeds baseline by >20%.\n- Requirement 1.3: Audit vendor dispatch timestamps and carrier transit logs.\n- Test 1.3: Calculate actual vs. contracted supplier lead time to verify supply delay.\n\nCOMPONENT 2: Procurement Execution (Air Freight PO)\n- Local Contribution: Rapidly replenish stock from supplier when supply delay is the validated constraint.\n- Requirement 2.1: PO authorization must require an attached diagnostic sign-off validating supply delay.\n- Test 2.1: Verify PO release rule blocks issuance if diagnostic sign-off is absent.\n\nCOMPONENT 3: Warehouse Inventory Management\n- Local Contribution: Ensure stock is physically available in pickable locations for order fulfillment.\n- Requirement 3.1: All incoming or existing SKU-17 inventory must be mapped to active pick bins in WMS.\n- Test 3.1: Perform mock order pick test for SKU-17 to confirm zero WMS pick rejections.\n\nINTERFACE A: [Constraint Diagnosis -> Procurement Execution]\n- Handoff Contract: Diagnostic root-cause determination passed to Procurement to select correct mitigation action.\n- Interface Failure Mode: Diagnosis identifies warehouse mis-slotting or unverified cause, but Procurement receives an un-gated trigger and issues air freight PO anyway (locally correct PO execution on broken handoff).\n- Requirement A.1: Procurement workflow must gate air freight PO creation on verified diagnostic payload indicating supply delay.\n- Test A.1: Negative test: Submit air freight request with 'mis-slot' or 'unverified' diagnostic tag; confirm system rejects PO creation.\n\nINTERFACE B: [Procurement Execution -> Warehouse Receiving]\n- Handoff Contract: Expedited shipping manifest passed to Warehouse to ensure priority receiving and active bin slotting.\n- Interface Failure Mode: Procurement successfully delivers air freighted stock on time, but Warehouse receiving places stock into unmapped overflow bins without WMS location updates (locally correct delivery, broken handoff).\n- Requirement B.1: Air freight receiving scan must immediately auto-assign active pick location in WMS within 60 minutes of arrival.\n- Test B.1: Track air freight delivery scan to active pick-location status update in WMS.",
  "NON-BLOCKING IMPROVEMENTS": "1. Implement automated WMS alerts when pick rejections occur despite positive system stock for SKU-17.\n2. Establish pre-negotiated SLA rates for air freight expediting to minimize unit cost if supply delay is verified.\n3. Implement dynamic safety stock calculation triggers for high-volatility SKUs.",
  "WHAT NOT TO SPEND TIME ON": "1. Negotiating air freight carrier contracts or expediting shipping before confirming that supply delay is the true constraint.\n2. Redesigning long-term demand forecasting models or SKU-17 packaging during active stockout emergency investigation.\n3. Decomposing warehouse operations into sub-tasks (e.g. forklift routing vs label scanning) that do not alter the material failure modes or tests.",
  "DEFECT STATUS": "PASS",
  "DECISION READINESS": "NEEDS_EVIDENCE",
  "route": "TASK",
  "requirements": [
    "(freeform B5 solution output)"
  ],
  "material_failures": [
    "(see raw)"
  ]
}

## EVIDENCE
(none)

## AGENT STAGE2
{}