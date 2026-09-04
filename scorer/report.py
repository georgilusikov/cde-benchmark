import argparse,json,collections
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--results',default='results'); ap.add_argument('--out',default='REPORT.md'); a=ap.parse_args(); root=Path(__file__).resolve().parents[1]; p=root/a.results/'scores.json'; rows=json.loads(p.read_text()) if p.exists() else []
lines=['# CDE Benchmark Report','','Status: '+('SMOKE ONLY — not empirical evidence' if any(r.get('mode')=='mock' for r in rows) else 'real evaluator outputs'),'']
for s,g in sorted((x, list(v for v in rows if v['system']==x)) for x in sorted(set(r['system'] for r in rows))):
 lines += [f'## {s}',f'- outputs: {len(g)}',f'- defect recall (run-level heuristic): {sum(r["defect_detected"] for r in g)}/{sum(bool(r["case_id"]) for r in g)}',f'- verdict accuracy (run-level heuristic): {sum(r["verdict_correct"] for r in g)}/{len(g)}',f'- ignore safety violations: {sum(r["ignore_unsafe"] for r in g)}','']
(root/a.out).write_text('\n'.join(lines)+'\n'); print(root/a.out)
