# Packet 04 | B5 | dev_clear_backup_window | run 1
class=CLEAR_TASK gold_route=TASK

## BRIEF
Nightly backup must finish 01:00-03:00. Dataset 80GB. Only link: 20GB/h reserved for backup in window.

## ARTIFACT
Plan: full 80GB backup every night from 01:00 on the 20GB/h link.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": null,
  "valid_models": [],
  "acceptable_probes": [],
  "forbidden_premature_commitments": [],
  "stage2_requirements": [
    "bytes/throughput must fit <=2h or increase window/throughput",
    "do not schedule full 80GB on 20GB/h in 2h"
  ],
  "stage2_material_failures": [
    "80GB at 20GB/h needs 4h; window is 2h"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": true
}

## AGENT STAGE1
{
  "intended_outcome": "Finish backup inside the 2-hour window.",
  "route": "TASK",
  "probe": null,
  "requirements": [],
  "material_failures": [],
  "tests": [],
  "decision_readiness": "READY",
  "_raw": true
}

## EVIDENCE
(none)

## AGENT STAGE2
{}