#!/usr/bin/env python3
"""Compare human labels vs semantic judge; report agreement."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BINARY = [
    "model_gap_correct",
    "probe_discriminating",
    "premature_commitment",
    "unnecessary_reframe",
    "readiness_correct",
]
CONTINUOUS = [
    "requirement_recall",
    "unsupported_confirmed_rate",
    "stage2_requirement_recall",
]


def key(r):
    return (r["case_id"], r["system"], r.get("run", 1))


def load_jsonl(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def norm_bin(v):
    if v is None:
        return None
    if v is True or v == 1 or v == "1":
        return 1
    if v is False or v == 0 or v == "0":
        return 0
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", required=True)
    ap.add_argument("--judge", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    human = {key(r): r for r in load_jsonl(args.human)}
    judge_rows = load_jsonl(args.judge)
    judge = {}
    for r in judge_rows:
        j = r.get("judgment") or {}
        judge[key(r)] = {**r, **j}

    binary_stats = {}
    disagreements = []
    for field in BINARY:
        agree = disagree = skipped = 0
        for k, h in human.items():
            hv = norm_bin(h.get(field))
            j = judge.get(k)
            if not j:
                skipped += 1
                continue
            jv = norm_bin(j.get(field))
            if hv is None and jv is None:
                skipped += 1
                continue
            if hv is None or jv is None:
                # one null one not — count disagree
                disagree += 1
                disagreements.append({"key": list(k), "field": field, "human": hv, "judge": jv})
                continue
            if hv == jv:
                agree += 1
            else:
                disagree += 1
                disagreements.append({"key": list(k), "field": field, "human": hv, "judge": jv})
        total = agree + disagree
        binary_stats[field] = {
            "agree": agree,
            "disagree": disagree,
            "skipped_null": skipped,
            "agreement": (agree / total) if total else None,
        }

    cont_stats = {}
    for field in CONTINUOUS:
        abs_err = []
        within = n = 0
        for k, h in human.items():
            hv = h.get(field)
            j = judge.get(k)
            if j is None or hv is None or j.get(field) is None:
                continue
            try:
                hv = float(hv)
                jv = float(j.get(field))
            except (TypeError, ValueError):
                continue
            abs_err.append(abs(hv - jv))
            n += 1
            if abs(hv - jv) <= 0.25:
                within += 1
        cont_stats[field] = {
            "n": n,
            "mae": (sum(abs_err) / len(abs_err)) if abs_err else None,
            "within_0_25": (within / n) if n else None,
        }

    bin_agreements = [v["agreement"] for v in binary_stats.values() if v["agreement"] is not None]
    overall = sum(bin_agreements) / len(bin_agreements) if bin_agreements else None
    # micro-average
    a = sum(v["agree"] for v in binary_stats.values())
    d = sum(v["disagree"] for v in binary_stats.values())
    micro = a / (a + d) if (a + d) else None

    report = {
        "binary_per_field": binary_stats,
        "binary_macro_agreement": overall,
        "binary_micro_agreement": micro,
        "binary_gate_pass": (micro is not None and micro >= 0.90),
        "continuous": cont_stats,
        "disagreements": disagreements,
        "n_human": len(human),
        "n_judge": len(judge),
    }
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(json.dumps({
        "binary_micro_agreement": micro,
        "binary_gate_pass": report["binary_gate_pass"],
        "per_field": {k: v["agreement"] for k, v in binary_stats.items()},
        "n_disagreements": len(disagreements),
        "out": args.out,
    }, indent=2))


if __name__ == "__main__":
    main()
