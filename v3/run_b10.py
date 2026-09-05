import json,random,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results_b10'
MODEL='gemini-3.6-flash-high'; PROMPTS={'B5':'b5.md','B10':'b10.md'}
def one(job):
 c,run,s=job; p=(ROOT/'prompts'/PROMPTS[s]).read_text()+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']
 try:
  r=call_agy(p,model=MODEL); return {'case_id':c['id'],'run':run,'system':s,'output':r['text'],'latency_s':r.get('latency_s'),'error':None}
 except Exception as e:return {'case_id':c['id'],'run':run,'system':s,'output':'','latency_s':None,'error':str(e)}
def main():
 cs=json.loads((ROOT/'b10_cases.json').read_text()); ss=list(PROMPTS); rng=random.Random(1010); jobs=[]
 for c in cs:
  for run in range(1,4):
   o=ss[:]; rng.shuffle(o); jobs += [(c,run,s) for s in o]
 OUT.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=8) as ex: rs=[f.result() for f in as_completed([ex.submit(one,j) for j in jobs])]
 rs.sort(key=lambda x:(x['case_id'],x['run'],x['system'])); (OUT/'raw_outputs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rs)); (OUT/'manifest.json').write_text(json.dumps({'jobs':len(rs),'systems':ss,'runs':3,'model':MODEL,'gold_hidden':True,'cases':'b10_cases.json'},indent=2)); print(json.dumps({'completed':len(rs),'errors':sum(bool(x['error']) for x in rs)}))
if __name__=='__main__':main()
