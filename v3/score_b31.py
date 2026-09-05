import json,re
from pathlib import Path
from collections import defaultdict, Counter
from statistics import median, quantiles
R=Path(__file__).resolve().parent; D=R/'results_b31'
cs={c['id']:c for c in json.loads((R/'b31_regression_cases.json').read_text())}
raw=[json.loads(x) for x in (D/'raw_outputs.jsonl').read_text().splitlines()]
jud=[json.loads(x) for x in (D/'raw_judgments.jsonl').read_text().splitlines()]
def status(text):
 m=re.findall(r'DEFECT STATUS\s*[:*]*\s*(?:\*\*)?\s*(PASS|FAIL)',text,re.I); n=re.findall(r'DECISION READINESS\s*[:*]*\s*(?:\*\*)?\s*(READY|NEEDS_EVIDENCE|BLOCKED)',text,re.I); return (m[-1].upper() if m else 'MISSING',n[-1].upper() if n else 'MISSING')
def jparse(text):
 m=re.search(r'\{.*\}',text,re.S)
 try:return json.loads(m.group()) if m else {}
 except:return {}
def maj(vals):
 return Counter(vals).most_common(1)[0][0] if vals else None
def stable_true(values):
 return sum(value is True for value in values) >= 2
def latency_summary(values):
 values=sorted(value for value in values if isinstance(value,(int,float)))
 if not values:return {'median_s':None,'p95_s':None}
 return {'median_s':median(values),'p95_s':values[-1] if len(values)<2 else quantiles(values,n=20,method='inclusive')[18]}
by=defaultdict(list); jb=defaultdict(list)
for x in raw: by[(x['case_id'],x['system'])].append(status(x['output']))
for x in jud: jb[(x['case_id'],x['system'])].append(jparse(x['judgment']))
report={'cases':{}}
for cid,c in cs.items():
 row={'gold':{'target_class':c['target_class'],'status':c['status'],'readiness':c['readiness']},'systems':{}}
 for s in ['B3','B3.1']:
  q=[x for x in jb[(cid,s)] if x]
  det=[x.get('target_detected') is True for x in q] if c['target_finding'] else [None]*len(q)
  cls=[x.get('target_class_correct') is True for x in q] if c['target_class']!='NONE' else [None]*len(q)
  st=[v[0] for v in by[(cid,s)]]; rd=[v[1] for v in by[(cid,s)]]
  row['systems'][s]={'target_detected_runs':det,'stable_detected':(stable_true(det) if c['target_finding'] else None),'class_correct_runs':cls,'stable_class':(stable_true(cls) if c['target_class']!='NONE' else None),'stable_status':maj(st),'stable_readiness':maj(rd),'unsupported_confirmed_runs':[x.get('unsupported_confirmed_defect') is True for x in q],'latency_s':[x.get('latency_s') for x in raw if x['case_id']==cid and x['system']==s],'output_chars':[len(x['output']) for x in raw if x['case_id']==cid and x['system']==s]}
 report['cases'][cid]=row
scores={}
for s in ['B3','B3.1']:
 det=[]; cls=[]; uns=[]; read=[]
 for c in cs.values():
  st=maj([v[0] for v in by[(c['id'],s)]])
  rd=maj([v[1] for v in by[(c['id'],s)]])
  read.append(rd==c['readiness'])
  if c['target_class']!='NONE':
   q=[x for x in jb[(c['id'],s)] if x]
   det.append(stable_true([x.get('target_detected') is True for x in q]) if c['target_finding'] else True)
   cls.append(stable_true([x.get('target_class_correct') is True for x in q]))
  uns += [x.get('unsupported_confirmed_defect') is True for x in jb[(c['id'],s)] if x]
 lat=latency_summary([x.get('latency_s') for x in raw if x['system']==s])
 scores[s]={'target_finding_recall':sum(det)/len(det) if det else None,'finding_class_accuracy':sum(cls)/len(cls) if cls else None,'unsupported_confirmed_defect_rate':sum(uns)/len(uns) if uns else None,'readiness_calibration':sum(read)/len(read),'output_chars':sum(len(x['output']) for x in raw if x['system']==s)/3,'latency':lat}
report['aggregate']=scores
report['judge_errors']=sum(bool(x.get('error')) for x in jud)
report['status_missing']=sum(status(x['output'])[0]=='MISSING' or status(x['output'])[1]=='MISSING' for x in raw)
(D/'b31_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'aggregate':scores,'judge_errors':report['judge_errors'],'status_missing':report['status_missing']},indent=2))
