import importlib.util, json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent; D=ROOT/'results_b10'
spec=importlib.util.spec_from_file_location('v3_score',ROOT/'score.py')
assert spec is not None and spec.loader is not None
score=importlib.util.module_from_spec(spec); spec.loader.exec_module(score)
ANCHORS={'a01_filter_range','a02_dose_conflict','a03_summary_reversal','a04_gate_skip'}
CLEANS=['c01_video_complete','c02_checkout_complete','c03_migration_complete']
GAPS=['g01_fee_unknown','g02_freshness_unknown','g03_tolerance_unknown']
cs={c['id']:c for c in json.loads((ROOT/'b10_cases.json').read_text())}
raw=[json.loads(x) for x in (D/'raw_outputs.jsonl').read_text().splitlines()]
jud=[json.loads(x) for x in (D/'raw_judgments.jsonl').read_text().splitlines()]
by=defaultdict(list); jb=defaultdict(list)
for x in raw: by[(x['case_id'],x['system'])].append(score.status(x['output']))
for x in jud: jb[(x['case_id'],x['system'])].append(score.jparse(x['judgment']))
def sub(ids, s, field):
 vals=[]
 for cid in ids:
  c=cs[cid]; q=[x for x in jb[(cid,s)] if x]
  if field=='det': vals.append(score.stable_true([x.get('target_detected') is True for x in q]) if c['target_finding'] else True)
  else: vals.append(score.stable_true([x.get('target_class_correct') is True for x in q]) if c['target_class']!='NONE' else True)
 return sum(vals)/len(vals)
report={'cases':{}}
for cid,c in cs.items():
 row={'gold':{'target_class':c['target_class'],'status':c['status'],'readiness':c['readiness']},'systems':{}}
 for s in ['B5','B10']:
  q=[x for x in jb[(cid,s)] if x]
  det=[x.get('target_detected') is True for x in q] if c['target_finding'] else [None]*len(q)
  cls=[x.get('target_class_correct') is True for x in q] if c['target_class']!='NONE' else [None]*len(q)
  nc=[x.get('unsupported_necessary_condition') is True for x in q]
  st=[v[0] for v in by[(cid,s)]]; rd=[v[1] for v in by[(cid,s)]]
  row['systems'][s]={'target_detected_runs':det,'stable_detected':(score.stable_true(det) if c['target_finding'] else None),'class_correct_runs':cls,'stable_class':(score.stable_true(cls) if c['target_class']!='NONE' else None),'stable_status':score.maj(st),'stable_readiness':score.maj(rd),'unsupported_confirmed_runs':[x.get('unsupported_confirmed_defect') is True for x in q],'unsupported_nc_runs':nc,'nc_conditions':[x.get('necessary_conditions',[]) for x in q],'latency_s':[x.get('latency_s') for x in raw if x['case_id']==cid and x['system']==s],'output_chars':[len(x['output']) for x in raw if x['case_id']==cid and x['system']==s]}
 report['cases'][cid]=row
value=[c['id'] for c in cs.values() if c['kind']=='VALUE_DEFECT']
agg={}
for s in ['B5','B10']:
 det=[]; cls=[]; uns=[]; unc=[]; read=[]
 for c in cs.values():
  rd=score.maj([v[1] for v in by[(c['id'],s)]])
  read.append(rd==c['readiness'])
  if c['target_class']!='NONE':
   q=[x for x in jb[(c['id'],s)] if x]
   det.append(score.stable_true([x.get('target_detected') is True for x in q]) if c['target_finding'] else True)
   cls.append(score.stable_true([x.get('target_class_correct') is True for x in q]))
  uns += [x.get('unsupported_confirmed_defect') is True for x in jb[(c['id'],s)] if x]
  unc += [x.get('unsupported_necessary_condition') is True for x in jb[(c['id'],s)] if x]
 lat=score.latency_summary([x.get('latency_s') for x in raw if x['system']==s])
 agg[s]={'target_finding_recall':sum(det)/len(det),'finding_class_accuracy':sum(cls)/len(cls),'value_recall':sub(value,s,'det'),'value_class':sub(value,s,'cls'),'anchor_recall':sub(sorted(ANCHORS),s,'det'),'unsupported_confirmed_defect_rate':sum(uns)/len(uns),'unsupported_nc_rate':sum(unc)/len(unc),'readiness_calibration':sum(read)/len(read),'output_chars':sum(len(x['output']) for x in raw if x['system']==s)/3,'latency':lat}
report['aggregate']=agg
report['judge_errors']=sum(bool(x.get('error')) for x in jud)
report['evaluator_errors']=sum(bool(x.get('error')) for x in raw)
report['status_missing']=sum(score.status(x['output'])[0]=='MISSING' or score.status(x['output'])[1]=='MISSING' for x in raw)
(D/'b10_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'aggregate':agg,'judge_errors':report['judge_errors'],'evaluator_errors':report['evaluator_errors'],'status_missing':report['status_missing']},indent=2))
