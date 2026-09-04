import json,re,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results/spec_agy'
J='You are a blinded independent judge for a SPEC requirements-discovery test. Given a brief, one hidden future mutation, and anonymous generated requirements, return JSON only with keys covered (boolean), hard_gate_appropriate (boolean), actionable (boolean), rationale. covered=true only if the requirements clearly state a check/test/gate that would detect the mutation before implementation. Do not reward vague generic quality language.'
def one(t):
 c,r,s,m=t; p=J+'\nBRIEF:\n'+c['brief']+'\nHIDDEN MUTATION:\n'+m+'\nGENERATED REQUIREMENTS:\n'+r['output'];
 try: x=call_agy(p,model='claude-sonnet-4-6'); return {'case_id':c['id'],'run':r['run'],'system':s,'mutation':m,'judgment':x['text'],'error':None}
 except Exception as e:return {'case_id':c['id'],'run':r['run'],'system':s,'mutation':m,'judgment':'','error':str(e)}
def main():
 cases=json.loads((ROOT/'spec/spec_cases.json').read_text()); cs={c['id']:c for c in cases}; rs=[json.loads(x) for x in (OUT/'raw_outputs.jsonl').read_text().splitlines()]; tasks=[(cs[r['case_id']],r,s,m) for r in rs for s in [r['system']] for m in cs[r['case_id']]['mutations']];
 with ThreadPoolExecutor(max_workers=8) as ex: out=[f.result() for f in as_completed([ex.submit(one,t) for t in tasks])]
 (OUT/'raw_judgments.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)); print(json.dumps({'judgments':len(out),'errors':sum(bool(x['error']) for x in out)}))
if __name__=='__main__':main()
