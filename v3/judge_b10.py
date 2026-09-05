import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent/'../runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results_b10'
J='''You are one blinded judge. Evaluate the anonymous output against the TARGET FINDING and TARGET CLASS. Return JSON only with keys target_detected, target_class_correct, unsupported_confirmed_defect, unsupported_necessary_condition, necessary_conditions, rationale. target_detected is true only when the target issue is explicitly identified, not a generic nearby concern. Additionally list every condition the output treats as necessary for the outcome as necessary_conditions: [{condition, class}] where class is one of EXPLICIT (stated in brief), LOGICALLY_NECESSARY (outcome cannot materially hold without it given supplied facts), DESIRABLE_NOT_NECESSARY (helpful but outcome could still hold), UNSUPPORTED (invented or ungrounded). Set unsupported_necessary_condition true when the output promotes a DESIRABLE_NOT_NECESSARY or UNSUPPORTED condition to a confirmed failure or requirement. Separately verify: could the stated outcome materially still hold without this condition? If yes, it is not necessary.'''
def one(t):
 c,r,s=t; p=J+'\nTARGET FINDING: '+c['target_finding']+'\nTARGET CLASS: '+c['target_class']+'\nBRIEF:\n'+c['brief']+'\nARTIFACT:\n'+c['artifact']+'\nOUTPUT:\n'+r['output'][:14000]
 try:
  x=call_agy(p,model='gemini-3.8-flash-high'); return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':x['text'],'error':None}
 except Exception as e:return {'case_id':c['id'],'run':r['run'],'system':s,'judgment':'','error':str(e)}
def main():
 cs={c['id']:c for c in json.loads((ROOT/'b10_cases.json').read_text())}; rs=[json.loads(x) for x in (OUT/'raw_outputs.jsonl').read_text().splitlines()]; tasks=[(cs[r['case_id']],r,r['system']) for r in rs]
 with ThreadPoolExecutor(max_workers=8) as ex: out=[f.result() for f in as_completed([ex.submit(one,t) for t in tasks])]
 (OUT/'raw_judgments.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)); print(json.dumps({'judgments':len(out),'errors':sum(bool(x['error']) for x in out)}))
if __name__=='__main__':main()
