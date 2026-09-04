import json,random,time,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results/spec_agy'
PROMPTS={'B1':'spec_b1.md','B1-ENRICHED':'spec_b1_enriched.md','CDE':'spec_cde.md'}
def one(job):
 c,run,s=job; prompt=(ROOT/'prompts'/PROMPTS[s]).read_text()+c['brief'];
 try:
  r=call_agy(prompt,model='gemini-3.6-flash-high'); return {'case_id':c['id'],'run':run,'system':s,'output':r['text'],'latency_s':r.get('latency_s'),'model':r.get('model'),'error':None}
 except Exception as e: return {'case_id':c['id'],'run':run,'system':s,'output':'','error':str(e)}
def main():
 cases=json.loads((ROOT/'spec/spec_cases.json').read_text()); systems=list(PROMPTS); rng=random.Random(404); jobs=[]
 for c in cases:
  for run in range(1,4):
   o=systems[:]; rng.shuffle(o); jobs += [(c,run,s) for s in o]
 with ThreadPoolExecutor(max_workers=8) as ex: rs=[f.result() for f in as_completed([ex.submit(one,j) for j in jobs])]
 rs.sort(key=lambda x:(x['case_id'],x['run'],x['system'])); (OUT/'raw_outputs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rs)); (OUT/'manifest.json').write_text(json.dumps({'jobs':len(jobs),'systems':systems,'runs':3,'model':'gemini-3.6-flash-high','gold_hidden':True},indent=2)); print(json.dumps({'completed':len(rs),'errors':sum(bool(x['error']) for x in rs)}))
if __name__=='__main__': main()
