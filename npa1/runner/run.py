#!/usr/bin/env python3
"""NPA-1 runner: B5 / NPA-B5 / ORACLE-NPA-B5 with optional stage-2 probe evidence.

Usage:
  python runner/run.py --cases smoke/cases.json --systems NPA-B5,B5 --runs 1 --mode mock
  python runner/run.py --cases smoke/cases.json --systems NPA-B5,B5,ORACLE-NPA-B5 --runs 1 --mode agy --model gemini-3.6-flash-high
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scorer"))
sys.path.insert(0, str(ROOT.parent / "runner"))
from score import (  # noqa: E402
    aggregate,
    check_gates,
    has_downstream_commit,
    jparse,
    match_probe,
    score_stage1,
    score_stage2,
)

PROMPTS = {
    "B5": ROOT / "prompts" / "b5.md",
    "NPA-B5": ROOT / "prompts" / "npa_b5.md",
    "ORACLE-NPA-B5": ROOT / "prompts" / "oracle_npa_b5.md",
}


def load_prompt(system: str, case: dict) -> str:
    text = PROMPTS[system].read_text()
    if system == "ORACLE-NPA-B5":
        text = text.replace("{{ROUTE}}", case["gold_route_stage1"])
    return text


def build_user_stage1(case: dict) -> str:
    parts = [f"INTENDED OUTCOME (hint may be incomplete): {case['intended_outcome']}", "BRIEF:", case["brief_stage1"]]
    if case.get("artifact_stage1"):
        parts += ["ARTIFACT:", case["artifact_stage1"]]
    parts.append("Respond with the required JSON only.")
    return "\n".join(parts)


def build_user_stage2(case: dict, stage1_out: dict, evidence: str) -> str:
    return "\n".join([
        "FOLLOW-UP EVIDENCE from the discriminating probe:",
        evidence,
        "",
        "Your previous JSON:",
        json.dumps(stage1_out, ensure_ascii=False),
        "",
        "Update the model, reclassify TASK vs PROBLEM, and if TASK run B5 fields.",
        "Respond with the required JSON only.",
    ])


def call_mock(system: str, case: dict, stage: str, stage1_out: dict | None = None) -> dict:
    """Deterministic mock agent for harness smoke — not evidence."""
    t0 = time.time()
    if stage == "stage1":
        if system == "B5":
            # Always "solves" as TASK with generic requirements — baseline pathology on PROBLEM
            out = {
                "intended_outcome": case["intended_outcome"],
                "route": "TASK",
                "supra_goal": None,
                "model_gap": None,
                "competing_models": [],
                "probe": None,
                "success": case["intended_outcome"],
                "parts": ["part_a", "part_b"],
                "material_failures": case.get("stage2_material_failures") or ["unspecified"],
                "requirements": (
                    case.get("forbidden_premature_commitments")[:1]
                    or case.get("stage2_requirements")[:2]
                    or ["implement requested solution"]
                ),
                "tests": case.get("stage2_tests")[:1] or ["check outcome"],
                "evidence_gaps": [],
                "decision_readiness": case.get("stage2_readiness") or "READY",
            }
        elif system in ("NPA-B5", "ORACLE-NPA-B5"):
            if case["gold_route_stage1"] == "TASK":
                out = {
                    "intended_outcome": case["intended_outcome"],
                    "route": "TASK",
                    "supra_goal": None,
                    "model_gap": None,
                    "competing_models": [],
                    "probe": None,
                    "success": case["intended_outcome"],
                    "parts": ["component_1", "interface_1"],
                    "material_failures": case.get("stage2_material_failures") or [],
                    "requirements": case.get("stage2_requirements") or ["satisfy stated constraints"],
                    "tests": case.get("stage2_tests") or ["verify constraints"],
                    "evidence_gaps": [],
                    "decision_readiness": case.get("stage2_readiness") or "READY",
                }
            else:
                probes = case.get("acceptable_probes") or []
                p = probes[0] if probes else {"description": "gather discriminating metric"}
                out = {
                    "intended_outcome": case["intended_outcome"],
                    "route": "PROBLEM",
                    "supra_goal": case.get("supra_goal"),
                    "model_gap": case.get("material_model_gap"),
                    "competing_models": [m.get("id") for m in case.get("valid_models") or []],
                    "probe": p.get("description"),
                    "success": "",
                    "parts": [],
                    "material_failures": [],
                    "requirements": [],
                    "tests": [],
                    "evidence_gaps": ["model not resolved"],
                    "decision_readiness": "NEEDS_EVIDENCE",
                }
        else:
            raise ValueError(system)
    else:  # stage2
        out = {
            "intended_outcome": case["intended_outcome"],
            "route": case.get("stage2_gold_route") or "TASK",
            "supra_goal": case.get("supra_goal"),
            "model_gap": None,
            "competing_models": [],
            "probe": None,
            "success": case["intended_outcome"],
            "parts": ["updated_model", "execution"],
            "material_failures": case.get("stage2_material_failures") or [],
            "requirements": case.get("stage2_requirements") or [],
            "tests": case.get("stage2_tests") or [],
            "evidence_gaps": [],
            "decision_readiness": case.get("stage2_readiness") or "BLOCKED",
        }
    return {"text": json.dumps(out, ensure_ascii=False), "latency_s": time.time() - t0, "error": None}


def call_agy(prompt: str, model: str, timeout: str = "360s") -> dict:
    from providers import call_agy as _call
    return _call(prompt, model=model, timeout=timeout)


def run_one(job: dict, mode: str, model: str) -> dict:
    case, system, run = job["case"], job["system"], job["run"]
    sys_prompt = load_prompt(system, case)
    user1 = build_user_stage1(case)
    full1 = sys_prompt + "\n\n" + user1

    if mode == "mock":
        r1 = call_mock(system, case, "stage1")
    else:
        try:
            r1 = call_agy(full1, model=model)
            r1 = {"text": r1["text"], "latency_s": r1.get("latency_s"), "error": None}
        except Exception as e:
            r1 = {"text": "", "latency_s": None, "error": str(e)}

    out1 = jparse(r1.get("text") or "")
    # B5 freeform: map common section labels into scorer fields when route-less
    if system == "B5":
        text = r1.get("text") or ""
        if not out1:
            out1 = {
                "intended_outcome": case["intended_outcome"],
                "route": "TASK",
                "probe": None,
                "requirements": [],
                "material_failures": [],
                "tests": [],
                "decision_readiness": "READY",
                "_raw": True,
            }
        if route_missing(out1):
            out1["route"] = "TASK"
        # Pull FAIL/READY markers
        m = re.findall(r"DECISION READINESS\s*[:*]*\s*(READY|NEEDS_EVIDENCE|BLOCKED)", text, re.I)
        if m:
            out1["decision_readiness"] = m[-1].upper()
        # If freeform has substantial body, treat as downstream commit content
        if len(text) >= 200 and not has_downstream_commit(out1):
            out1.setdefault("requirements", [])
            if isinstance(out1.get("requirements"), list) and not out1["requirements"]:
                out1["requirements"] = ["(freeform B5 solution output)"]
            out1.setdefault("material_failures", [])
            if isinstance(out1.get("material_failures"), list) and not out1["material_failures"]:
                # keep a short raw anchor for phrase scans via meta raw_text
                out1["material_failures"] = ["(see raw)"]


    row = {
        "case_id": case["id"],
        "system": system,
        "run": run,
        "model": model if mode != "mock" else "mock",
        "stage1_raw": r1.get("text"),
        "stage1_out": out1,
        "stage1_latency_s": r1.get("latency_s"),
        "stage1_error": r1.get("error"),
        "stage1_chars": len(r1.get("text") or ""),
        "stage2_raw": None,
        "stage2_out": None,
        "stage2_latency_s": None,
        "stage2_error": None,
        "stage2_chars": None,
        "evidence_returned": None,
        "probe_matched_id": None,
    }

    # Multi-turn only when gold PROBLEM and agent route PROBLEM (or oracle/mock path)
    if case.get("gold_route_stage1") == "PROBLEM" and case.get("stage2_gold_route"):
        matched = match_probe(case, out1)
        # For B5 always-TASK, still optionally skip stage2 (no probe)
        if matched or (mode == "mock" and system != "B5"):
            if not matched and case.get("acceptable_probes"):
                matched = case["acceptable_probes"][0]
            if matched:
                evidence = matched["evidence_returned"]
                row["evidence_returned"] = evidence
                row["probe_matched_id"] = matched.get("id")
                user2 = build_user_stage2(case, out1, evidence)
                full2 = sys_prompt + "\n\n" + user2
                if mode == "mock":
                    r2 = call_mock(system, case, "stage2", out1)
                else:
                    try:
                        r2 = call_agy(full2, model=model)
                        r2 = {"text": r2["text"], "latency_s": r2.get("latency_s"), "error": None}
                    except Exception as e:
                        r2 = {"text": "", "latency_s": None, "error": str(e)}
                out2 = jparse(r2.get("text") or "")
                if system == "B5" and not out2:
                    out2 = {
                        "intended_outcome": case["intended_outcome"],
                        "route": "TASK",
                        "requirements": ["(freeform)"],
                        "decision_readiness": "READY",
                    }
                row["stage2_raw"] = r2.get("text")
                row["stage2_out"] = out2
                row["stage2_latency_s"] = r2.get("latency_s")
                row["stage2_error"] = r2.get("error")
                row["stage2_chars"] = len(r2.get("text") or "")
    return row


def route_missing(out: dict) -> bool:
    r = out.get("route")
    return not (isinstance(r, str) and r.strip().upper() in ("TASK", "PROBLEM"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(ROOT / "smoke" / "cases.json"))
    ap.add_argument("--systems", default="B5,NPA-B5")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--mode", choices=["mock", "agy"], default="mock")
    ap.add_argument("--model", default="gemini-3.6-flash-high")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=str(ROOT / "results" / "smoke"))
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    cases = json.loads(Path(args.cases).read_text())
    systems = [s.strip() for s in args.systems.split(",") if s.strip()]
    for s in systems:
        if s not in PROMPTS:
            raise SystemExit(f"unknown system {s}")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    jobs = []
    for c in cases:
        for run in range(1, args.runs + 1):
            order = systems[:]
            rng.shuffle(order)
            for s in order:
                jobs.append({"case": c, "system": s, "run": run})

    t0 = time.time()
    print(json.dumps({"phase": "eval", "jobs": len(jobs), "mode": args.mode, "systems": systems}), flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = [f.result() for f in as_completed([ex.submit(run_one, j, args.mode, args.model) for j in jobs])]
    rows.sort(key=lambda r: (r["case_id"], r["run"], r["system"]))
    (out_dir / "raw_outputs.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    )

    # score
    by_id = {c["id"]: c for c in cases}
    s1, s2 = [], []
    for r in rows:
        c = by_id[r["case_id"]]
        s1.append(score_stage1(c, r["stage1_out"] or {}, {
            "latency_s": r["stage1_latency_s"],
            "chars": r["stage1_chars"],
            "system": r["system"],
            "model": r["model"],
            "run": r["run"],
            "raw_text": r.get("stage1_raw") or "",
        }))
        if r.get("stage2_out"):
            s2.append(score_stage2(c, r["stage2_out"], {
                "latency_s": r["stage2_latency_s"],
                "chars": r["stage2_chars"],
                "system": r["system"],
                "model": r["model"],
                "run": r["run"],
            }))

    agg = aggregate(s1, cases)
    gates = check_gates(agg) if set(systems) >= {"B5", "NPA-B5"} else None
    report = {
        "manifest": {
            "cases": args.cases,
            "n_cases": len(cases),
            "systems": systems,
            "runs": args.runs,
            "mode": args.mode,
            "model": args.model if args.mode != "mock" else "mock",
            "jobs": len(rows),
            "seconds": round(time.time() - t0, 2),
            "stage1_errors": sum(bool(r.get("stage1_error")) for r in rows),
            "stage2_errors": sum(bool(r.get("stage2_error")) for r in rows),
            "gold_hidden_from_evaluator": True,
        },
        "stage1_scores": s1,
        "stage2_scores": s2,
        "aggregate": agg,
        "gates": gates,
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))
    # short md
    lines = [
        f"# NPA-1 run ({args.mode})",
        "",
        f"cases={len(cases)} systems={systems} runs={args.runs} jobs={len(rows)}",
        "",
        "| system | route_acc | PROBLEM recall | TASK spec | PCR | URR | probe | lat med |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for sys, a in agg["systems"].items():
        lines.append(
            f"| {sys} | {a['route_accuracy']} | {a['problem_route_recall']} | {a['task_route_specificity']} | "
            f"{a['premature_commitment_rate']} | {a['unnecessary_reframe_rate']} | {a['probe_match_rate']} | "
            f"{a['latency_median_s']} |"
        )
    if gates:
        lines += ["", "## Gates (deterministic core)", ""]
        for k, v in gates["gates"].items():
            lines.append(f"- {k}: {'PASS' if v['pass'] else 'FAIL/PENDING'} — {v['detail']}")
        lines.append(f"- deterministic_core_pass: {gates['deterministic_core_pass']}")
    (out_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({
        "done": True,
        "out": str(out_dir),
        "aggregate": agg["systems"],
        "deterministic_core_pass": (gates or {}).get("deterministic_core_pass"),
        "errors": report["manifest"]["stage1_errors"],
    }, indent=2), flush=True)
    print((out_dir / "REPORT.md").read_text())


if __name__ == "__main__":
    main()
