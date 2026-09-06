#!/usr/bin/env python3
"""Semantic judge runner for NPA-1 (D/E/F + gap/probe/PCR overlay).

Does not replace deterministic scorer. Writes judgments beside an existing run dir.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "runner"))

JUDGE_PROMPT = (ROOT / "prompts" / "judge.md").read_text()


def jparse(text: str) -> dict:
    if not text:
        return {}
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S | re.I)
    if fence:
        text = fence.group(1)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        o = json.loads(m.group())
        return o if isinstance(o, dict) else {}
    except Exception:
        return {}


def gold_pack(case: dict) -> dict:
    return {
        "class": case.get("class"),
        "gold_route_stage1": case.get("gold_route_stage1"),
        "intended_outcome": case.get("intended_outcome"),
        "supra_goal": case.get("supra_goal"),
        "material_model_gap": case.get("material_model_gap"),
        "valid_models": case.get("valid_models"),
        "acceptable_probes": [
            {"id": p.get("id"), "description": p.get("description")}
            for p in (case.get("acceptable_probes") or [])
        ],
        "forbidden_premature_commitments": case.get("forbidden_premature_commitments"),
        "unnecessary_probe": case.get("unnecessary_probe"),
        "stage2_gold_route": case.get("stage2_gold_route"),
        "stage2_material_failures": case.get("stage2_material_failures"),
        "stage2_requirements": case.get("stage2_requirements"),
        "stage2_readiness": case.get("stage2_readiness"),
        "stage2_status": case.get("stage2_status"),
        "false_positive_traps": case.get("false_positive_traps"),
        "notes_for_judge": case.get("notes_for_judge"),
    }


def build_judge_user(case: dict, row: dict) -> str:
    parts = [
        f"CASE_ID_FOR_LOG_ONLY (do not let id bias you): {case['id']}",
        f"CLASS: {case.get('class')}",
        "BRIEF:",
        case.get("brief_stage1") or "",
    ]
    if case.get("artifact_stage1"):
        parts += ["ARTIFACT:", case["artifact_stage1"]]
    parts += ["GOLD:", json.dumps(gold_pack(case), ensure_ascii=False, indent=2)]
    parts += ["AGENT_STAGE1_JSON:", json.dumps(row.get("stage1_out") or {}, ensure_ascii=False)[:12000]]
    if row.get("evidence_returned"):
        parts += ["PROBE_EVIDENCE_RETURNED:", row["evidence_returned"]]
    if row.get("stage2_out"):
        parts += ["AGENT_STAGE2_JSON:", json.dumps(row.get("stage2_out") or {}, ensure_ascii=False)[:12000]]
    # For B5 freeform, include truncated raw if stage1_out is thin
    raw = row.get("stage1_raw") or ""
    if raw and (row.get("system") == "B5" or len(json.dumps(row.get("stage1_out") or {})) < 80):
        parts += ["AGENT_STAGE1_RAW_TRUNC:", raw[:8000]]
    parts.append("Return the judgment JSON only.")
    return "\n".join(parts)


def call_agy(prompt: str, model: str) -> dict:
    from providers import call_agy as _c
    return _c(prompt, model=model, timeout="360s")


def one(task: dict, model: str, mode: str) -> dict:
    case, row = task["case"], task["row"]
    user = build_judge_user(case, row)
    full = JUDGE_PROMPT + "\n\n" + user
    if mode == "mock":
        # Minimal mock: copy deterministic-ish defaults — not for calibration
        gold = case.get("gold_route_stage1")
        out = {
            "model_gap_correct": 1 if gold == "PROBLEM" else None,
            "probe_discriminating": 1 if gold == "PROBLEM" else None,
            "premature_commitment": 1 if row.get("system") == "B5" and gold == "PROBLEM" else 0,
            "unnecessary_reframe": 0 if gold == "TASK" else None,
            "requirement_recall": 1.0 if gold == "TASK" else None,
            "unsupported_confirmed_count": 0,
            "unsupported_confirmed_rate": 0.0,
            "readiness_correct": None,
            "stage2_requirement_recall": 1.0 if row.get("stage2_out") else None,
            "rationale": "mock",
        }
        return {
            "case_id": case["id"], "system": row["system"], "run": row["run"],
            "model": row.get("model"), "judgment": out, "raw": json.dumps(out),
            "error": None, "judge_model": "mock", "latency_s": 0.0,
        }
    try:
        t0 = time.time()
        r = call_agy(full, model=model)
        text = r.get("text") or ""
        return {
            "case_id": case["id"], "system": row["system"], "run": row["run"],
            "model": row.get("model"), "judgment": jparse(text), "raw": text,
            "error": None, "judge_model": model, "latency_s": r.get("latency_s") or (time.time() - t0),
        }
    except Exception as e:
        return {
            "case_id": case["id"], "system": row["system"], "run": row["run"],
            "model": row.get("model"), "judgment": {}, "raw": "",
            "error": str(e), "judge_model": model, "latency_s": None,
        }


def merge_semantic(run_dir: Path, judgments: list[dict]) -> dict:
    """Attach semantic means into a small summary (not full gate yet)."""
    from collections import defaultdict
    by = defaultdict(list)
    for j in judgments:
        if j.get("error") or not j.get("judgment"):
            continue
        by[j["system"]].append(j["judgment"])

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / len(xs) if xs else None

    summary = {}
    for sys, js in by.items():
        summary[sys] = {
            "n": len(js),
            "model_gap_correct": mean([j.get("model_gap_correct") for j in js if j.get("model_gap_correct") is not None]),
            "probe_discriminating": mean([j.get("probe_discriminating") for j in js if j.get("probe_discriminating") is not None]),
            "premature_commitment": mean([j.get("premature_commitment") for j in js if j.get("premature_commitment") is not None]),
            "unnecessary_reframe": mean([j.get("unnecessary_reframe") for j in js if j.get("unnecessary_reframe") is not None]),
            "requirement_recall": mean([j.get("requirement_recall") for j in js if j.get("requirement_recall") is not None]),
            "unsupported_confirmed_rate": mean([j.get("unsupported_confirmed_rate") for j in js if j.get("unsupported_confirmed_rate") is not None]),
            "readiness_correct": mean([j.get("readiness_correct") for j in js if j.get("readiness_correct") is not None]),
            "stage2_requirement_recall": mean([j.get("stage2_requirement_recall") for j in js if j.get("stage2_requirement_recall") is not None]),
        }
    (run_dir / "semantic_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True, help="dir with raw_outputs.jsonl")
    ap.add_argument("--cases", required=True)
    ap.add_argument("--model", default="gemini-3.8-flash-high", help="judge model (fixed for a freeze)")
    ap.add_argument("--mode", choices=["agy", "mock"], default="agy")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--systems", default="", help="optional filter comma list")
    ap.add_argument("--limit", type=int, default=0, help="optional max judgments (calibration)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    cases = {c["id"]: c for c in json.loads(Path(args.cases).read_text())}
    rows = [json.loads(x) for x in (run_dir / "raw_outputs.jsonl").read_text().splitlines()]
    systems = [s.strip() for s in args.systems.split(",") if s.strip()] or None
    tasks = []
    for r in rows:
        if systems and r.get("system") not in systems:
            continue
        if r["case_id"] not in cases:
            continue
        tasks.append({"case": cases[r["case_id"]], "row": r})
    if args.limit and args.limit < len(tasks):
        import random
        rng = random.Random(args.seed)
        rng.shuffle(tasks)
        tasks = tasks[: args.limit]

    print(json.dumps({"phase": "semantic_judge", "tasks": len(tasks), "model": args.model, "mode": args.mode}), flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        out = [f.result() for f in as_completed([ex.submit(one, t, args.model, args.mode) for t in tasks])]
    out.sort(key=lambda x: (x.get("system") or "", x.get("case_id") or "", x.get("run") or 0))
    (run_dir / "semantic_judgments.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out)
    )
    summary = merge_semantic(run_dir, out)
    print(json.dumps({
        "done": True,
        "judgments": len(out),
        "errors": sum(bool(x.get("error")) for x in out),
        "summary": summary,
    }, indent=2))


if __name__ == "__main__":
    main()
