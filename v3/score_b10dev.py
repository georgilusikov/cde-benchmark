import importlib.util, json
from pathlib import Path
from collections import defaultdict
import sys as _sys
ROOT=Path(__file__).resolve().parent; STEM=_sys.argv[1] if len(_sys.argv)>1 else 'b10_dev_cases'; D=ROOT/f'results_{STEM}'
spec=importlib.util.spec_from_file_location('v3_score',ROOT/'score.py')
assert spec is not None and spec.loader is not None
score=importlib.util.module_from_spec(spec); spec.loader.exec_module(score)
J_PREFIX='''You are one blinded judge. Evaluate whether the anonymous output identifies the TARGET FINDING and TARGET CLASS. Return JSON only with keys target_detected, target_class_correct, unsupported_confirmed_defect, rationale. target_detected is true only when the target issue is explicitly identified, not a generic nearby concern.'''
cs={c['id']:c for c in json.loads((ROOT/f'{STEM}.json').read_text())}
raw=[json.loads(x) for x in (D/'raw_outputs.jsonl').read_text().splitlines()]
jud=[json.loads(x) for x in (D/'raw_judgments.jsonl').read_text().splitlines()]
jb=defaultdict(list)
for x in jud: jb[x['case_id']].append(score.jparse(x['judgment']))
defects=[c for c in cs.values() if c['kind']=='DEV_DEFECT']
hits={c['id']:score.stable_true([x.get('target_detected') is True for x in jb[c['id']] if x]) for c in defects}
recall=sum(hits.values())/len(hits)
print(json.dumps({'stable_recall_4_defects':recall,'per_case':hits,'judge_errors':sum(bool(x.get('error')) for x in jud),'evaluator_errors':sum(bool(x.get('error')) for x in raw),'status_missing':sum(score.status(x['output'])[0]=='MISSING' or score.status(x['output'])[1]=='MISSING' for x in raw)},indent=2))
print('GATE:', 'PASS' if 0.25 <= recall <= 0.75 else 'FAIL')
