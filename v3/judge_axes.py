import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent
J='''You are one blinded judge. Evaluate whether the anonymous output identifies the TARGET FINDING and TARGET CLASS. Return JSON only with keys target_detected, target_class_correct, unsupported_confirmed_defect, rationale. target_detected is true only when the target issue is explicitly identified, not a generic nearby concern.'''
def judge_exp(exp):
 OUT=ROOT/f'results_{exp}'
 def one(t):
  c,r,s=t; p=J+'\nTARGET FINDING: '+c['target_finding']+'\nTARGET CLASS: '+c['target_class']+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']+'\nOUTPUT:\n'+r['output'][:14000]
  try:
   x=call_agy(p,model='gemini-3.8-flash-high'); return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':x['text'],'error':None}
  except Exception as e:return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':'','error':str(e)}
 cs={c['id']:c for c in json.loads((ROOT/f'{exp}_cases.json').read_text())}; rs=[json.loads(x) for x in (OUT/'raw_outputs.jsonl').read_text().splitlines()]; tasks=[(cs[r['case_id']],r,r['system']) for r in rs]
 with ThreadPoolExecutor(max_workers=8) as ex: out=[f.result() for f in as_completed([ex.submit(one,t) for t in tasks])]
 (OUT/'raw_judgments.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)); print(json.dumps({'exp':exp,'judgments':len(out),'errors':sum(bool(x['error']) for x in out)}))
if __name__=='__main__':judge_exp(sys.argv[1])
