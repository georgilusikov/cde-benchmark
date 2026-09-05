import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
R=Path(__file__).resolve().parent; cs={x['id']:x for x in json.loads((R/'cases.json').read_text())}; rows=[json.loads(x) for x in (R/'results/raw_judgments.jsonl').read_text().splitlines()]
J='''You are one blinded judge. Evaluate whether the anonymous output identifies the TARGET FINDING and TARGET CLASS. Return JSON only with keys target_detected, target_class_correct, unsupported_confirmed_defect, rationale. target_detected is true only when the target issue is explicitly identified, not a generic nearby concern.'''
out=[]
for j in rows:
 if not j.get('error'): continue
 c=cs[j['case_id']]; raw=next(x for x in (R/'results/raw_outputs.jsonl').read_text().splitlines() if json.loads(x)['case_id']==c['id'] and json.loads(x)['run']==j['run'] and json.loads(x)['system']==j['system']); a=json.loads(raw)
 p=J+'\nTARGET FINDING: '+c['target_finding']+'\nTARGET CLASS: '+c['target_class']+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']+'\nOUTPUT:\n'+a['output'][:14000]
 try:
  x=call_agy(p,model='gemini-3.8-flash-high'); out.append({'case_id':c['id'],'run':j['run'],'system':j['system'],'judgment':x['text'],'error':None})
 except Exception as e: out.append({'case_id':c['id'],'run':j['run'],'system':j['system'],'judgment':'','error':str(e)})
Path(R/'results/retries.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)); print(json.dumps({'retried':len(out),'errors':sum(bool(x['error']) for x in out)}))
