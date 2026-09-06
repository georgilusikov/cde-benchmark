#!/usr/bin/env python3
"""Build a balanced ~36-transcript calibration sample from a run dir."""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-system", type=int, default=12)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    cases = {c["id"]: c for c in json.loads(Path(args.cases).read_text())}
    rows = [json.loads(x) for x in (Path(args.run_dir) / "raw_outputs.jsonl").read_text().splitlines()]
    by_sys_class = defaultdict(list)
    for r in rows:
        c = cases.get(r["case_id"])
        if not c:
            continue
        by_sys_class[(r["system"], c.get("class") or "UNK")].append(r)

    rng = random.Random(args.seed)
    systems = sorted({r["system"] for r in rows})
    classes = sorted({c.get("class") or "UNK" for c in cases.values()})
    selected = []
    for sys in systems:
        need = args.per_system
        # round-robin across classes
        buckets = {cls: list(by_sys_class[(sys, cls)]) for cls in classes}
        for b in buckets.values():
            rng.shuffle(b)
        picked = []
        while len(picked) < need and any(buckets.values()):
            for cls in classes:
                if len(picked) >= need:
                    break
                if buckets[cls]:
                    picked.append(buckets[cls].pop())
        selected.extend(picked[:need])

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    # mini run dir for judge_semantic
    (out / "raw_outputs.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in selected)
    )
    manifest = {
        "source_run": str(args.run_dir),
        "per_system": args.per_system,
        "seed": args.seed,
        "n": len(selected),
        "by_system": {s: sum(1 for r in selected if r["system"] == s) for s in systems},
        "by_class": {},
        "items": [
            {
                "case_id": r["case_id"],
                "system": r["system"],
                "run": r["run"],
                "class": cases[r["case_id"]].get("class"),
            }
            for r in selected
        ],
    }
    for r in selected:
        cls = cases[r["case_id"]].get("class")
        manifest["by_class"][cls] = manifest["by_class"].get(cls, 0) + 1
    (out / "sample_manifest.json").write_text(json.dumps(manifest, indent=2))

    # empty human label template
    labels = []
    for r in selected:
        labels.append({
            "case_id": r["case_id"],
            "system": r["system"],
            "run": r["run"],
            "model_gap_correct": None,
            "probe_discriminating": None,
            "premature_commitment": None,
            "unnecessary_reframe": None,
            "requirement_recall": None,
            "unsupported_confirmed_count": None,
            "unsupported_confirmed_rate": None,
            "readiness_correct": None,
            "stage2_requirement_recall": None,
            "labeler": "",
            "notes": "",
            "_hint_class": cases[r["case_id"]].get("class"),
            "_hint_gold_route": cases[r["case_id"]].get("gold_route_stage1"),
        })
    (out / "human_labels.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in labels)
    )
    # human-readable packets
    packets = out / "packets"
    packets.mkdir(exist_ok=True)
    for i, r in enumerate(selected):
        c = cases[r["case_id"]]
        text = [
            f"# Packet {i:02d} | {r['system']} | {r['case_id']} | run {r['run']}",
            f"class={c.get('class')} gold_route={c.get('gold_route_stage1')}",
            "",
            "## BRIEF",
            c.get("brief_stage1") or "",
            "",
            "## ARTIFACT",
            c.get("artifact_stage1") or "(none)",
            "",
            "## GOLD (for labeler only — hide from naive second rater if testing pure blindness)",
            json.dumps({
                "material_model_gap": c.get("material_model_gap"),
                "valid_models": c.get("valid_models"),
                "acceptable_probes": c.get("acceptable_probes"),
                "forbidden_premature_commitments": c.get("forbidden_premature_commitments"),
                "stage2_requirements": c.get("stage2_requirements"),
                "stage2_material_failures": c.get("stage2_material_failures"),
                "stage2_readiness": c.get("stage2_readiness"),
                "unnecessary_probe": c.get("unnecessary_probe"),
            }, ensure_ascii=False, indent=2),
            "",
            "## AGENT STAGE1",
            json.dumps(r.get("stage1_out") or {}, ensure_ascii=False, indent=2)[:8000],
            "",
            "## EVIDENCE",
            r.get("evidence_returned") or "(none)",
            "",
            "## AGENT STAGE2",
            json.dumps(r.get("stage2_out") or {}, ensure_ascii=False, indent=2)[:8000],
        ]
        (packets / f"{i:02d}_{r['system']}_{r['case_id']}.md").write_text("\n".join(text))

    print(json.dumps({"wrote": str(out), "n": len(selected), "by_system": manifest["by_system"], "by_class": manifest["by_class"]}, indent=2))


if __name__ == "__main__":
    main()
