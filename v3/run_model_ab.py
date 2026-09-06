#!/usr/bin/env python3
"""Model A/B on frozen B5 suite: B1 vs B5 × gemini-3.6-flash-high vs gemini-3.8-flash-high.

Does NOT touch results_b5. Writes to results_model_ab/.
Judge is fixed to gemini-3.8-flash-high for both evaluator arms.
"""
import json, random, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent / '../runner'))
from providers import call_agy

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results_model_ab'
PROMPTS = {'B1': 'b1.md', 'B5': 'b5.md'}
EVAL_MODELS = ['gemini-3.6-flash-high', 'gemini-3.8-flash-high']
JUDGE_MODEL = 'gemini-3.8-flash-high'
RUNS = 3
SEED = 5105  # same shuffle seed family as run_b5
WORKERS = 8

JUDGE_PROMPT = (
    'You are one blinded judge. Evaluate whether the anonymous output identifies '
    'the TARGET FINDING and TARGET CLASS. Return JSON only with keys '
    'target_detected, target_class_correct, unsupported_confirmed_defect, rationale. '
    'target_detected is true only when the target issue is explicitly identified, '
    'not a generic nearby concern.'
)


def eval_one(job):
    c, run, system, model = job
    prompt = (
        (ROOT / 'prompts' / PROMPTS[system]).read_text()
        + '\nBRIEF:\n' + c['brief']
        + '\nARTIFACT:\n' + c['artifact']
    )
    try:
        r = call_agy(prompt, model=model)
        return {
            'case_id': c['id'], 'run': run, 'system': system, 'model': model,
            'output': r['text'], 'latency_s': r.get('latency_s'), 'error': None,
        }
    except Exception as e:
        return {
            'case_id': c['id'], 'run': run, 'system': system, 'model': model,
            'output': '', 'latency_s': None, 'error': str(e),
        }


def judge_one(task):
    c, row = task
    p = (
        JUDGE_PROMPT
        + '\nTARGET FINDING: ' + c['target_finding']
        + '\nTARGET CLASS: ' + c['target_class']
        + '\nBRIEF:\n' + c['brief']
        + '\nARTIFACT:\n' + c['artifact']
        + '\nOUTPUT:\n' + row['output'][:14000]
    )
    try:
        x = call_agy(p, model=JUDGE_MODEL)
        return {
            'case_id': c['id'], 'run': row['run'], 'system': row['system'],
            'model': row['model'], 'judgment': x['text'], 'error': None,
            'judge_model': JUDGE_MODEL,
        }
    except Exception as e:
        return {
            'case_id': c['id'], 'run': row['run'], 'system': row['system'],
            'model': row['model'], 'judgment': '', 'error': str(e),
            'judge_model': JUDGE_MODEL,
        }


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else 'all'
    OUT.mkdir(exist_ok=True)
    cases = json.loads((ROOT / 'b5_cases.json').read_text())
    by_id = {c['id']: c for c in cases}

    if phase in ('eval', 'all'):
        rng = random.Random(SEED)
        jobs = []
        for model in EVAL_MODELS:
            for c in cases:
                for run in range(1, RUNS + 1):
                    order = list(PROMPTS)
                    rng.shuffle(order)
                    jobs += [(c, run, s, model) for s in order]
        t0 = time.time()
        print(json.dumps({'phase': 'eval', 'jobs': len(jobs), 'models': EVAL_MODELS}), flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            rs = [f.result() for f in as_completed([ex.submit(eval_one, j) for j in jobs])]
        rs.sort(key=lambda x: (x['model'], x['case_id'], x['run'], x['system']))
        (OUT / 'raw_outputs.jsonl').write_text(
            ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rs)
        )
        manifest = {
            'jobs': len(rs),
            'systems': list(PROMPTS),
            'runs': RUNS,
            'eval_models': EVAL_MODELS,
            'judge_model': JUDGE_MODEL,
            'gold_hidden': True,
            'cases': 'b5_cases.json',
            'seed': SEED,
            'eval_seconds': round(time.time() - t0, 1),
            'evaluator_errors': sum(bool(x['error']) for x in rs),
        }
        (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
        print(json.dumps({'eval_done': True, **{k: manifest[k] for k in ('jobs', 'evaluator_errors', 'eval_seconds')}}), flush=True)

    if phase in ('judge', 'all'):
        raw = [json.loads(x) for x in (OUT / 'raw_outputs.jsonl').read_text().splitlines()]
        # Only judge non-error outputs; keep empty slots for errors
        tasks = [(by_id[r['case_id']], r) for r in raw if not r.get('error') and r.get('output')]
        t0 = time.time()
        print(json.dumps({'phase': 'judge', 'tasks': len(tasks)}), flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            out = [f.result() for f in as_completed([ex.submit(judge_one, t) for t in tasks])]
        # Include error-row placeholders so counts match
        for r in raw:
            if r.get('error') or not r.get('output'):
                out.append({
                    'case_id': r['case_id'], 'run': r['run'], 'system': r['system'],
                    'model': r['model'], 'judgment': '', 'error': r.get('error') or 'empty_output',
                    'judge_model': JUDGE_MODEL,
                })
        out.sort(key=lambda x: (x['model'], x['case_id'], x['run'], x['system']))
        (OUT / 'raw_judgments.jsonl').write_text(
            ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in out)
        )
        print(json.dumps({
            'judge_done': True,
            'judgments': len(out),
            'judge_errors': sum(bool(x.get('error')) for x in out),
            'judge_seconds': round(time.time() - t0, 1),
        }), flush=True)

    if phase in ('score', 'all'):
        import importlib.util
        from collections import defaultdict
        spec = importlib.util.spec_from_file_location('v3_score', ROOT / 'score.py')
        score = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(score)
        raw = [json.loads(x) for x in (OUT / 'raw_outputs.jsonl').read_text().splitlines()]
        jud = [json.loads(x) for x in (OUT / 'raw_judgments.jsonl').read_text().splitlines()]
        report = {'models': {}, 'paired': {}}
        for model in EVAL_MODELS:
            by = defaultdict(list)
            jb = defaultdict(list)
            mraw = [x for x in raw if x['model'] == model]
            mjud = [x for x in jud if x['model'] == model]
            for x in mraw:
                by[(x['case_id'], x['system'])].append(score.status(x['output']))
            for x in mjud:
                jb[(x['case_id'], x['system'])].append(score.jparse(x['judgment']))
            scores = {}
            case_rows = {}
            for s in PROMPTS:
                det, cls, uns, read = [], [], [], []
                for c in cases:
                    rd = score.maj([v[1] for v in by[(c['id'], s)]])
                    read.append(rd == c['readiness'])
                    q = [x for x in jb[(c['id'], s)] if x]
                    if c['target_class'] != 'NONE':
                        det.append(score.stable_true([x.get('target_detected') is True for x in q]) if c['target_finding'] else True)
                        cls.append(score.stable_true([x.get('target_class_correct') is True for x in q]))
                    uns += [x.get('unsupported_confirmed_defect') is True for x in q]
                lat = score.latency_summary([x.get('latency_s') for x in mraw if x['system'] == s])
                scores[s] = {
                    'target_finding_recall': sum(det) / len(det) if det else None,
                    'finding_class_accuracy': sum(cls) / len(cls) if cls else None,
                    'unsupported_confirmed_defect_rate': sum(uns) / len(uns) if uns else None,
                    'readiness_calibration': sum(read) / len(read),
                    'output_chars': sum(len(x['output']) for x in mraw if x['system'] == s) / RUNS,
                    'latency': lat,
                }
            for c in cases:
                row = {'gold': {'target_class': c['target_class'], 'status': c['status'], 'readiness': c['readiness']}, 'systems': {}}
                for s in PROMPTS:
                    q = [x for x in jb[(c['id'], s)] if x]
                    det = [x.get('target_detected') is True for x in q] if c['target_finding'] else [None] * len(q)
                    clsv = [x.get('target_class_correct') is True for x in q] if c['target_class'] != 'NONE' else [None] * len(q)
                    st = [v[0] for v in by[(c['id'], s)]]
                    rd = [v[1] for v in by[(c['id'], s)]]
                    row['systems'][s] = {
                        'stable_detected': (score.stable_true(det) if c['target_finding'] else None),
                        'stable_class': (score.stable_true(clsv) if c['target_class'] != 'NONE' else None),
                        'stable_status': score.maj(st),
                        'stable_readiness': score.maj(rd),
                    }
                case_rows[c['id']] = row
            report['models'][model] = {
                'aggregate': scores,
                'cases': case_rows,
                'evaluator_errors': sum(bool(x.get('error')) for x in mraw),
                'judge_errors': sum(bool(x.get('error')) for x in mjud),
                'status_missing': sum(
                    score.status(x['output'])[0] == 'MISSING' or score.status(x['output'])[1] == 'MISSING'
                    for x in mraw
                ),
            }
        # Paired deltas: 3.8 - 3.6 for each system
        m36 = 'gemini-3.6-flash-high'
        m38 = 'gemini-3.8-flash-high'
        paired = {}
        for s in PROMPTS:
            a = report['models'][m36]['aggregate'][s]
            b = report['models'][m38]['aggregate'][s]
            paired[s] = {
                'recall_delta': (b['target_finding_recall'] or 0) - (a['target_finding_recall'] or 0),
                'class_delta': (b['finding_class_accuracy'] or 0) - (a['finding_class_accuracy'] or 0),
                'unsup_delta': (b['unsupported_confirmed_defect_rate'] or 0) - (a['unsupported_confirmed_defect_rate'] or 0),
                'readiness_delta': b['readiness_calibration'] - a['readiness_calibration'],
                'chars_ratio': (b['output_chars'] / a['output_chars']) if a['output_chars'] else None,
            }
        # Case-level flips for B5
        flips = {'B5_36miss_38hit': [], 'B5_36hit_38miss': [], 'B1_36miss_38hit': [], 'B1_36hit_38miss': []}
        for c in cases:
            if not c['target_finding']:
                continue
            for s, key_hit, key_miss in [
                ('B5', 'B5_36miss_38hit', 'B5_36hit_38miss'),
                ('B1', 'B1_36miss_38hit', 'B1_36hit_38miss'),
            ]:
                d36 = report['models'][m36]['cases'][c['id']]['systems'][s]['stable_detected']
                d38 = report['models'][m38]['cases'][c['id']]['systems'][s]['stable_detected']
                if d36 is False and d38 is True:
                    flips[key_hit].append(c['id'])
                if d36 is True and d38 is False:
                    flips[key_miss].append(c['id'])
        report['paired'] = {'deltas': paired, 'flips': flips, 'baseline_model': m36, 'candidate_model': m38}
        (OUT / 'model_ab_report.json').write_text(json.dumps(report, indent=2))
        # Human summary
        lines = ['# Model A/B — B5 suite (B1 vs B5 × 3.6 vs 3.8 Flash High)', '',
                 f'Judge fixed: `{JUDGE_MODEL}`. Cases: `b5_cases.json` (10). Runs: {RUNS}. Stable ≥2/3.', '']
        lines.append('| model | system | recall | class | unsup | readiness | chars | lat med |')
        lines.append('|---|---|---:|---:|---:|---:|---:|---:|')
        for model in EVAL_MODELS:
            for s in PROMPTS:
                a = report['models'][model]['aggregate'][s]
                lat = (a.get('latency') or {}).get('median')
                lines.append(
                    f"| {model} | {s} | {a['target_finding_recall']:.2f} | {a['finding_class_accuracy']:.2f} | "
                    f"{a['unsupported_confirmed_defect_rate']:.3f} | {a['readiness_calibration']:.2f} | "
                    f"{int(a['output_chars'])} | {lat} |"
                )
        lines += ['', '## Paired deltas (3.8 − 3.6)', '']
        for s, d in paired.items():
            lines.append(
                f"- **{s}**: recall {d['recall_delta']:+.2f}, class {d['class_delta']:+.2f}, "
                f"unsup {d['unsup_delta']:+.3f}, readiness {d['readiness_delta']:+.2f}, "
                f"chars×{d['chars_ratio']:.2f}" if d['chars_ratio'] else f"- **{s}**: {d}"
            )
        lines += ['', '## Detection flips (stable)', '']
        for k, v in flips.items():
            lines.append(f"- {k}: {v or '—'}")
        lines += ['', '## Errors', '']
        for model in EVAL_MODELS:
            m = report['models'][model]
            lines.append(
                f"- {model}: eval_err={m['evaluator_errors']} judge_err={m['judge_errors']} "
                f"status_missing={m['status_missing']}"
            )
        (OUT / 'MODEL_AB_RESULTS.md').write_text('\n'.join(lines) + '\n')
        print(json.dumps({'score_done': True, 'paired': paired, 'flips': flips}, indent=2), flush=True)
        print((OUT / 'MODEL_AB_RESULTS.md').read_text(), flush=True)


if __name__ == '__main__':
    main()
