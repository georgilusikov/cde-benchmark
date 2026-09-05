import json,re
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parent; cs={c['id']:c for c in json.loads((R/'cases.json').read_text())}
raw=[json.loads(x) for x in (R/'results/raw_outputs.jsonl').read_text().splitlines()]
for x in json.loads('[]'): pass
retry={ (x['case_id'],x['run'],x['system']):x for x in [json.loads(y) for y in (R/'results/retries.jsonl').read_text().splitlines()] }
jud=[]
for line in (R/'results/raw_judgments.jsonl').read_text().splitlines():
 x=json.loads(line); x=retry.get((x['case_id'],x['run'],x['system']),x); jud.append(x)
def status(text):
 m=re.findall(r'DEFECT STATUS\s*[:*]*\s*(?:\*\*)?\s*(PASS|FAIL)',text,re.I); n=re.findall(r'DECISION READINESS\s*[:*]*\s*(?:\*\*)?\s*(READY|NEEDS_EVIDENCE|BLOCKED)',text,re.I); return (m[-1].upper() if m else 'MISSING',n[-1].upper() if n else 'MISSING')
def jparse(text):
 m=re.search(r'\{.*\}',text,re.S)
 try:return json.loads(m.group()) if m else {}
 except:return {}
by=defaultdict(list); jb=defaultdict(list)
for x in raw: by[(x['case_id'],x['system'])].append(status(x['output']))
for x in jud: jb[(x['case_id'],x['system'])].append(jparse(x['judgment']))
def maj(vals):
 from collections import Counter
 return Counter(vals).most_common(1)[0][0] if vals else None
scores={}
for s in ['B1','B2','B3']:
 target_cases=[c for c in cs.values() if c['target_class']!='NONE']
 recall=[]; cls=[]; uns=[]; read=[]
 for c in cs.values():
  st=maj([v[0] for v in by[(c['id'],s)]])
  rd=maj([v[1] for v in by[(c['id'],s)]])
  read.append(rd==c['readiness'])
  if c['target_class']!='NONE':
   q=[x for x in jb[(c['id'],s)] if x]
   recall.append(any(x.get('target_detected') is True for x in q) if c['target_finding'] else True)
   cls.append(all(x.get('target_class_correct') is True for x in q))
  uns += [x.get('unsupported_confirmed_defect') is True for x in jb[(c['id'],s)] if x]
 scores[s]={'target_finding_recall':sum(recall)/len(recall),'finding_class_accuracy':sum(cls)/len(cls),'unsupported_confirmed_defect_rate':sum(uns)/len(uns),'readiness_calibration':sum(read)/len(read),'output_chars':sum(len(x['output']) for x in raw if x['system']==s)/3}
print(json.dumps({'scores':scores,'judge_errors_after_retry':sum(bool(x.get('error')) for x in jud),'status_missing':sum(status(x['output'])[0]=='MISSING' or status(x['output'])[1]=='MISSING' for x in raw)},indent=2))
(R/'results/scoreboard.json').write_text(json.dumps(scores,indent=2))
