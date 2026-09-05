import json,random,sys,time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results_b4'
MODEL='gemini-3.6-flash-high'
LENSES=['lens_constraint.md','lens_failure.md','lens_outcome.md']
DOMAIN={'sql':'lens_domain_sql.md','medical':'lens_domain_medical.md','summary':'lens_domain_summary.md','strategy':'lens_domain_strategy.md','naming':'lens_domain_naming.md'}
def lens_call(lens_file, brief, artifact):
 p=(ROOT/'prompts'/lens_file).read_text()+'\nBRIEF:\n'+brief+'\nARTIFACT:\n'+artifact
 r=call_agy(p,model=MODEL); return {'lens':lens_file,'text':r['text'],'latency_s':r.get('latency_s')}
def one_b4(c, run):
 t=time.time(); brief=c['brief']; artifact=c['artifact']
 lenses=LENSES+[DOMAIN[c['domain']]]
 with ThreadPoolExecutor(max_workers=4) as ex:
  futs=[ex.submit(lens_call,f,brief,artifact) for f in lenses]
  lens_out=[f.result() for f in futs]
 lens_block='\n\n'.join('=== LENS '+l['lens']+' ===\n'+l['text'] for l in lens_out)
 sp=(ROOT/'prompts'/'b4_synth.md').read_text()+'\nBRIEF:\n'+brief+'\nARTIFACT:\n'+artifact+'\n\nCANDIDATES:\n'+lens_block
 r=call_agy(sp,model=MODEL)
 return {'case_id':c['id'],'run':run,'system':'B4','output':r['text'],'latency_s':time.time()-t,'lens_latency_s':[l['latency_s'] for l in lens_out],'calls':5,'lens_outputs':lens_out,'error':None}
def one_b1(c, run):
 p=(ROOT/'prompts'/'b1.md').read_text()+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']
 try:
  r=call_agy(p,model=MODEL); return {'case_id':c['id'],'run':run,'system':'B1','output':r['text'],'latency_s':r.get('latency_s'),'calls':1,'error':None}
 except Exception as e:return {'case_id':c['id'],'run':run,'system':'B1','output':'','latency_s':None,'calls':1,'error':str(e)}
def one(job):
 c,run,s=job
 if s=='B4':
  try:return one_b4(c,run)
  except Exception as e:return {'case_id':c['id'],'run':run,'system':'B4','output':'','latency_s':None,'calls':5,'error':str(e)}
 return one_b1(c,run)
def main():
 cs=json.loads((ROOT/'cases.json').read_text()); ss=['B1','B4']; rng=random.Random(4104); jobs=[]
 for c in cs:
  for run in range(1,4):
   o=ss[:]; rng.shuffle(o); jobs += [(c,run,s) for s in o]
 OUT.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=6) as ex: rs=[f.result() for f in as_completed([ex.submit(one,j) for j in jobs])]
 rs.sort(key=lambda x:(x['case_id'],x['run'],x['system']))
 judged=[{k:v for k,v in x.items() if k!='lens_outputs'} for x in rs]
 (OUT/'raw_outputs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in judged))
 (OUT/'lens_outputs.jsonl').write_text(''.join(json.dumps({'case_id':x['case_id'],'run':x['run'],'lenses':x.get('lens_outputs',[])},ensure_ascii=False)+'\n' for x in rs if x['system']=='B4'))
 (OUT/'manifest.json').write_text(json.dumps({'jobs':len(rs),'systems':ss,'runs':3,'model':MODEL,'gold_hidden':True,'cases':'cases.json','lenses':LENSES,'domain_map':DOMAIN},indent=2)); print(json.dumps({'completed':len(rs),'errors':sum(bool(x['error']) for x in rs)}))
if __name__=='__main__':main()
