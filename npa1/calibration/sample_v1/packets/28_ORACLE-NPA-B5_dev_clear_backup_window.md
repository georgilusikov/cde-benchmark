# Packet 28 | ORACLE-NPA-B5 | dev_clear_backup_window | run 1
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
  "intended_outcome": "Finish 80GB full backup within the 2-hour window (01:00-03:00).",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "Full 80GB dataset is backed up every night starting at 01:00 and completes on or before 03:00.",
  "parts": [
    {
      "component": "Backup Time Window",
      "local_contribution": "Provides a fixed 2-hour window (01:00 to 03:00) for backup execution."
    },
    {
      "component": "Reserved Network Link",
      "local_contribution": "Transfers data at a dedicated rate of 20 GB/h during the execution window."
    },
    {
      "component": "Backup Source Dataset",
      "local_contribution": "Provides 80 GB of data requiring complete nightly backup."
    }
  ],
  "material_failures": [
    "Throughput/Window Capacity Deficit: Transferring 80 GB over a 20 GB/h link requires 4 hours (completing at 05:00), but the available window is only 2 hours, resulting in a 40 GB deficit and incomplete backup by 03:00."
  ],
  "requirements": [
    "Network link throughput must be at least 40 GB/h to transfer 80 GB within a 2-hour window.",
    "Backup window duration must be at least 4 hours (e.g., 01:00-05:00) to transfer 80 GB at 20 GB/h."
  ],
  "tests": [
    "Window Capacity Test: Verify whether reserved_rate * window_duration (20 GB/h * 2 h = 40 GB) >= dataset_size (80 GB).",
    "Completion Schedule Test: Verify whether start_time + (dataset_size / reserved_rate) (01:00 + 4 h = 05:00) <= window_end_time (03:00)."
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
(none)

## AGENT STAGE2
{}