import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'
J='''You are a blinded judge. Given an artifact, gold target labels, and one anonymous output, return JSON only: defect_status (PASS/FAIL), decision_readiness (READY/NEEDS_EVIDENCE/BLOCKED), defect_status_correct, readiness_correct, false_defect, rationale. PASS means no demonstrated violation; missing evidence belongs to NEEDS_EVIDENCE, not FAIL.'''
def one(t):
 c,r,s=t; p=J+'\\nTARGET LABELS (judge reference): '+json.dumps({'defect_status':c['gold_defect_status'],'readiness':c['gold_readiness']})+'\\nBRIEF:\\n'+c['brief']+'\\nARTIFACT:\\n'+c['artifact']+'\\nOUTPUT:\\n'+r['output']
 try:
  x=call_agy(p,model='gemini-3.8-flash-high'); return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':x['text'],'error':None,'judge_model':'gemini-3.8-flash-high'}
 except Exception as e:return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':'','error':str(e),'judge_model':'gemini-3.8-flash-high'}
def main():
 cs={c['id']:c for c in json.loads((ROOT/'cases.json').read_text())}; rs=[json.loads(x) for x in (OUT/'raw_outputs.jsonl').read_text().splitlines()]; old=[json.loads(x) for x in (OUT/'raw_judgments.jsonl').read_text().splitlines()]; failed={(r['case_id'],r['run'],r['system']) for r in old if r.get('error')}; tasks=[(cs[r['case_id']],r,r['system']) for r in rs if (r['case_id'],r['run'],r['system']) in failed]
 with ThreadPoolExecutor(max_workers=8) as ex: out=[f.result() for f in as_completed([ex.submit(one,t) for t in tasks])]
 (OUT/'retry_judgments.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\\n' for x in out)); print(json.dumps({'retried':len(out),'errors':sum(bool(x['error']) for x in out)}))
if __name__=='__main__':main()
