import json,random,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; STEM=sys.argv[1] if len(sys.argv)>1 else 'b10_dev_cases'; OUT=ROOT/f'results_{STEM}'
MODEL='gemini-3.6-flash-high'
def one(job):
 c,run=job; p=(ROOT/'prompts'/'b5.md').read_text()+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']
 try:
  r=call_agy(p,model=MODEL); return {'case_id':c['id'],'run':run,'system':'B5','output':r['text'],'latency_s':r.get('latency_s'),'error':None}
 except Exception as e:return {'case_id':c['id'],'run':run,'system':'B5','output':'','latency_s':None,'error':str(e)}
def main():
 cs=json.loads((ROOT/f'{STEM}.json').read_text()); jobs=[(c,run) for c in cs for run in range(1,4)]
 random.Random(1001).shuffle(jobs)
 OUT.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=8) as ex: rs=[f.result() for f in as_completed([ex.submit(one,j) for j in jobs])]
 rs.sort(key=lambda x:(x['case_id'],x['run'])); (OUT/'raw_outputs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rs)); (OUT/'manifest.json').write_text(json.dumps({'jobs':len(rs),'system':'B5','runs':3,'model':MODEL,'gold_hidden':True,'cases':f'{STEM}.json'},indent=2)); print(json.dumps({'completed':len(rs),'errors':sum(bool(x['error']) for x in rs)}))
if __name__=='__main__':main()
