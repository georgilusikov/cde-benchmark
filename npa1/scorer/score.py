#!/usr/bin/env python3
"""NPA-1 deterministic scorer (primary reliability layer).

Semantic judge fields are optional overlays; this module never requires them
for route/stop/PCR-proxy/URR-proxy/cost metrics.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def jparse(text: str) -> dict:
    if not text:
        return {}
    text = text.strip()
    # strip markdown fences
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S | re.I)
    if fence:
        text = fence.group(1)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        obj = json.loads(m.group())
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _as_list(v: Any) -> list:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.strip():
        return [v]
    return []


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def _text_blob(out: dict) -> str:
    parts = []
    for k in (
        "intended_outcome", "route", "supra_goal", "model_gap", "probe",
        "success", "material_failures", "requirements", "tests", "evidence_gaps",
        "competing_models", "parts", "decision_readiness",
    ):
        v = out.get(k)
        if v is None:
            continue
        if isinstance(v, (list, dict)):
            parts.append(json.dumps(v, ensure_ascii=False))
        else:
            parts.append(str(v))
    return _norm(" ".join(parts))


def has_downstream_commit(out: dict) -> bool:
    """True if agent manufactured solution-ish content (requirements/failures/tests)."""
    reqs = _as_list(out.get("requirements"))
    fails = _as_list(out.get("material_failures"))
    tests = _as_list(out.get("tests"))
    parts = _as_list(out.get("parts"))
    # nonempty structured solution content
    if any(_norm(str(x)) for x in reqs + fails + tests):
        return True
    if len(parts) >= 2:
        return True
    return False


def route_of(out: dict) -> str | None:
    r = out.get("route")
    if isinstance(r, str):
        r = r.strip().upper()
        if r in ("TASK", "PROBLEM"):
            return r
    return None


def match_probe(case: dict, out: dict) -> dict | None:
    """Return matched acceptable_probe or None."""
    probe = out.get("probe")
    if probe is None:
        return None
    if isinstance(probe, dict):
        blob = _norm(json.dumps(probe, ensure_ascii=False))
    else:
        blob = _norm(str(probe))
    if not blob:
        return None
    best = None
    best_score = 0.0
    for p in case.get("acceptable_probes") or []:
        keys = [_norm(p.get("description", ""))] + [_norm(a) for a in p.get("aliases") or []]
        keys = [k for k in keys if k]
        score = 0.0
        for k in keys:
            if len(k) >= 8 and (k in blob or blob in k):
                score = max(score, 1.0)
            kw = set(re.findall(r"[a-z0-9%]{4,}", k))
            bw = set(re.findall(r"[a-z0-9%]{4,}", blob))
            if kw:
                score = max(score, len(kw & bw) / len(kw))
            # also score against significant content words only
            stop = {"with", "from", "that", "this", "have", "been", "were", "their", "about", "into", "over", "under", "after", "before", "versus", "vs"}
            kw2 = {w for w in kw if w not in stop}
            bw2 = {w for w in bw if w not in stop}
            if kw2:
                score = max(score, len(kw2 & bw2) / len(kw2))
        if score > best_score:
            best_score = score
            best = p
    # accept if >=40% key overlap or any strong substring
    if best is not None and best_score >= 0.4:
        return best
    return None


def _commitment_blob(out: dict, raw_text: str | None = None) -> str:
    """Text where solution commitments live — not model_gap / competing_models restatements."""
    parts = []
    for k in ("requirements", "tests", "success", "parts", "material_failures"):
        v = out.get(k)
        if v is None:
            continue
        if isinstance(v, (list, dict)):
            parts.append(json.dumps(v, ensure_ascii=False))
        else:
            parts.append(str(v))
    # Include probe only if it looks like an implement-now action without measurement framing
    # (scored separately); do not scan whole raw freeform except requirements-like sections.
    blob = _norm(" ".join(parts))
    if raw_text and route_of(out) == "TASK":
        # freeform baseline: whole raw is the "solution"
        blob = (blob + " " + _norm(raw_text)).strip()
    return blob


def premature_commitment(case: dict, out: dict, raw_text: str | None = None) -> bool:
    """PROBLEM cases: committed to forbidden model-dependent solution content."""
    if case.get("gold_route_stage1") != "PROBLEM":
        return False
    blob = _commitment_blob(out, raw_text)
    for phrase in case.get("forbidden_premature_commitments") or []:
        if _norm(phrase) and _norm(phrase) in blob:
            return True
    if route_of(out) == "PROBLEM" and has_downstream_commit(out):
        if len(_as_list(out.get("requirements"))) >= 2:
            return True
    if route_of(out) == "TASK" and case.get("gold_route_stage1") == "PROBLEM":
        if has_downstream_commit(out):
            return True
        if any(_norm(p) in blob for p in (case.get("forbidden_premature_commitments") or []) if _norm(p)):
            return True
        if raw_text and len(raw_text) >= 400:
            return True
    return False


def unnecessary_reframe(case: dict, out: dict, raw_text: str | None = None) -> bool:
    """TASK cases: agent went PROBLEM / probe when unnecessary_probe is true."""
    if case.get("gold_route_stage1") != "TASK":
        return False
    if not case.get("unnecessary_probe", True):
        return False
    if route_of(out) == "PROBLEM":
        return True
    probe = out.get("probe")
    if probe and not has_downstream_commit(out) and route_of(out) == "TASK":
        if str(out.get("decision_readiness", "")).upper() in ("NEEDS_EVIDENCE", "BLOCKED"):
            return True
    blob = _text_blob(out)
    if raw_text:
        blob = (blob + " " + _norm(raw_text)).strip()
    for trap in case.get("false_positive_traps") or []:
        t = _norm(trap)
        if t and t in blob:
            return True
    return False


def score_stage1(case: dict, out: dict, meta: dict | None = None) -> dict:
    meta = meta or {}
    raw_text = meta.get("raw_text")
    parsed = bool(out)
    route = route_of(out)
    gold = case.get("gold_route_stage1")
    route_ok = route == gold
    stop_ok = None
    pcr = premature_commitment(case, out, raw_text) if gold == "PROBLEM" else False
    urr = unnecessary_reframe(case, out, raw_text) if gold == "TASK" else False
    if gold == "PROBLEM":
        stop_ok = route == "PROBLEM" and not pcr
    elif gold == "TASK":
        stop_ok = route == "TASK" and not urr

    probe_match = match_probe(case, out) if gold == "PROBLEM" else None
    return {
        "case_id": case["id"],
        "class": case.get("class"),
        "gold_route": gold,
        "json_valid": parsed and route is not None,
        "route": route,
        "route_correct": route_ok,
        "premature_commitment": pcr,
        "unnecessary_reframe": urr,
        "probe_matched": bool(probe_match),
        "probe_id": (probe_match or {}).get("id"),
        "has_downstream": has_downstream_commit(out),
        "decision_readiness": out.get("decision_readiness"),
        "stop_discipline_ok": stop_ok,
        "latency_s": meta.get("latency_s"),
        "chars": meta.get("chars"),
        "system": meta.get("system"),
        "model": meta.get("model"),
        "run": meta.get("run"),
        "stage": "stage1",
    }


def score_stage2(case: dict, out: dict, meta: dict | None = None) -> dict:
    meta = meta or {}
    route = route_of(out)
    gold2 = case.get("stage2_gold_route")
    return {
        "case_id": case["id"],
        "json_valid": bool(out) and route is not None,
        "route": route,
        "route_correct": (route == gold2) if gold2 else None,
        "has_downstream": has_downstream_commit(out),
        "decision_readiness": out.get("decision_readiness"),
        "latency_s": meta.get("latency_s"),
        "chars": meta.get("chars"),
        "system": meta.get("system"),
        "model": meta.get("model"),
        "run": meta.get("run"),
        "stage": "stage2",
    }


def stable_true(values: list, min_runs: int = 2) -> bool | None:
    """Stable affirmative: >= min_runs True among non-null values.
    If only one non-null value (smoke/dev single-run), that value decides.
    """
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    if len(vals) == 1:
        return bool(vals[0] is True)
    need = min(min_runs, len(vals))
    # classic >=2/3 when 3 runs: need 2
    if len(vals) >= 3:
        need = 2
    return sum(1 for v in vals if v is True) >= need


def maj(values: list):
    vals = [v for v in values if v is not None]
    return Counter(vals).most_common(1)[0][0] if vals else None


def aggregate(stage1_rows: list[dict], cases: list[dict]) -> dict:
    by_case_sys = defaultdict(list)
    for r in stage1_rows:
        by_case_sys[(r["case_id"], r.get("system"))].append(r)

    systems = sorted(s for s in {r.get("system") for r in stage1_rows} if isinstance(s, str))
    out = {"systems": {}, "case_stable": {}}

    for sys in systems:
        srows = [r for r in stage1_rows if r.get("system") == sys]
        task_rows = [r for r in srows if r.get("gold_route") == "TASK"]
        prob_rows = [r for r in srows if r.get("gold_route") == "PROBLEM"]

        # stable per case then mean
        case_ids = sorted({r["case_id"] for r in srows})
        route_ok, pcr, urr, probe_ok, json_ok = [], [], [], [], []
        for cid in case_ids:
            rows = by_case_sys[(cid, sys)]
            gold = rows[0]["gold_route"] if rows else None
            json_ok.append(stable_true([r["json_valid"] for r in rows]))
            route_ok.append(stable_true([r["route_correct"] for r in rows]))
            if gold == "PROBLEM":
                pcr.append(stable_true([r["premature_commitment"] for r in rows]))
                probe_ok.append(stable_true([r["probe_matched"] for r in rows]))
            if gold == "TASK":
                urr.append(stable_true([r["unnecessary_reframe"] for r in rows]))
            out["case_stable"].setdefault(cid, {})[sys] = {
                "route_correct": stable_true([r["route_correct"] for r in rows]),
                "premature_commitment": stable_true([r["premature_commitment"] for r in rows]),
                "unnecessary_reframe": stable_true([r["unnecessary_reframe"] for r in rows]),
                "probe_matched": stable_true([r["probe_matched"] for r in rows]),
                "maj_route": maj([r["route"] for r in rows]),
            }

        def mean_bool(xs):
            xs = [x for x in xs if x is not None]
            return (sum(1 for x in xs if x) / len(xs)) if xs else None

        lats = [r["latency_s"] for r in srows if isinstance(r.get("latency_s"), (int, float))]
        chars = [r["chars"] for r in srows if isinstance(r.get("chars"), (int, float))]
        out["systems"][sys] = {
            "n_runs": len(srows),
            "json_valid_rate": mean_bool(json_ok),
            "route_accuracy": mean_bool(route_ok),
            "problem_route_recall": mean_bool([
                stable_true([r["route_correct"] for r in by_case_sys[(cid, sys)]])
                for cid in case_ids
                if any(r.get("gold_route") == "PROBLEM" for r in by_case_sys[(cid, sys)])
            ]),
            "task_route_specificity": mean_bool([
                stable_true([r["route_correct"] for r in by_case_sys[(cid, sys)]])
                for cid in case_ids
                if any(r.get("gold_route") == "TASK" for r in by_case_sys[(cid, sys)])
            ]),
            "premature_commitment_rate": mean_bool(pcr),
            "unnecessary_reframe_rate": mean_bool(urr),
            "probe_match_rate": mean_bool(probe_ok),
            "latency_median_s": median(lats) if lats else None,
            "chars_mean": (sum(chars) / len(chars)) if chars else None,
            "task_runs": len(task_rows),
            "problem_runs": len(prob_rows),
        }
    return out


def check_gates(agg: dict, baseline: str = "B5", candidate: str = "NPA-B5") -> dict:
    """Apply preregistered gates; returns pass/fail per gate. Missing metrics -> fail."""
    b = agg["systems"].get(baseline, {})
    c = agg["systems"].get(candidate, {})
    gates = {}

    def g(name, ok, detail):
        gates[name] = {"pass": bool(ok), "detail": detail}

    pr = c.get("problem_route_recall")
    g("A_problem_detection", pr is not None and pr >= 0.80, f"PROBLEM recall={pr}")

    pcr_b, pcr_c = b.get("premature_commitment_rate"), c.get("premature_commitment_rate")
    if pcr_b is None or pcr_c is None:
        g("B_pcr_reduction", False, f"PCR baseline={pcr_b} candidate={pcr_c}")
    else:
        # PCR_NPA <= 0.60 * PCR_B5  (40% relative reduction). If baseline PCR=0, require candidate=0.
        limit = 0.0 if pcr_b == 0 else 0.60 * pcr_b
        g("B_pcr_reduction", pcr_c <= limit + 1e-9, f"PCR {pcr_c} <= {limit} (baseline {pcr_b})")

    urr = c.get("unnecessary_reframe_rate")
    g("C_paranoia_guard", urr is not None and urr <= 0.10, f"URR={urr}")

    # D/E/F need requirement recall — placeholder until semantic layer wired
    g("D_b5_preservation", False, "requires semantic requirement recall (not in deterministic layer)")
    g("E_hallucination", False, "requires semantic unsupported rate")
    g("F_recovery", False, "requires post-probe semantic recall")

    lat_b, lat_c = b.get("latency_median_s"), c.get("latency_median_s")
    if lat_b and lat_c:
        g("cost_latency", lat_c <= 1.5 * lat_b + 1e-9, f"lat {lat_c} vs {lat_b}")
    else:
        g("cost_latency", False, f"lat baseline={lat_b} candidate={lat_c}")

    ch_b, ch_c = b.get("chars_mean"), c.get("chars_mean")
    if ch_b and ch_c:
        g("cost_chars", ch_c <= 1.7 * ch_b + 1e-9, f"chars {ch_c} vs {ch_b}")
    else:
        g("cost_chars", False, f"chars baseline={ch_b} candidate={ch_c}")

    det_ok = all(gates[k]["pass"] for k in ("A_problem_detection", "B_pcr_reduction", "C_paranoia_guard"))
    return {"gates": gates, "deterministic_core_pass": det_ok, "full_adoption_pass": all(g["pass"] for g in gates.values())}


if __name__ == "__main__":
    # self-check with synthetic outputs
    case = {
        "id": "t",
        "gold_route_stage1": "PROBLEM",
        "class": "MODEL_MISMATCH",
        "forbidden_premature_commitments": ["hire more agents"],
        "acceptable_probes": [{
            "id": "p1",
            "description": "assignment wait vs handle time",
            "aliases": ["pre-assignment delay"],
            "evidence_returned": "x",
        }],
        "unnecessary_probe": False,
        "false_positive_traps": [],
    }
    good = {
        "intended_outcome": "SLA",
        "route": "PROBLEM",
        "probe": "Compare assignment wait vs handle time for late tickets",
        "requirements": [],
        "material_failures": [],
        "decision_readiness": "NEEDS_EVIDENCE",
    }
    bad = {
        "intended_outcome": "SLA",
        "route": "TASK",
        "requirements": ["hire more agents next month", "open seats"],
        "material_failures": ["not enough agents"],
        "decision_readiness": "READY",
    }
    print(json.dumps({"good": score_stage1(case, good), "bad": score_stage1(case, bad)}, indent=2))
