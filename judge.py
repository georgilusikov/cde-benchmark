import json, random, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent/'runner'))
from providers import call_agy
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'/'agy_parallel'

def one(pair):
    c, x, y = pair
    judge=(ROOT/'prompts/judge.md').read_text()
    prompt=f'''{judge}\n\nARTIFACT:\n{c["artifact"]}\n\nGOLD DEFECT DESCRIPTION (judge-only reference):\n{c["gold_defect"] or "No defect; clean control."}\n\nANONYMOUS OUTPUT X:\n{x["output"]}\n\nANONYMOUS OUTPUT Y:\n{y["output"]}\n\nReturn JSON with keys x_detected, y_detected, x_classification_correct, y_classification_correct, x_ignore_unsafe, y_ignore_unsafe, x_verdict_correct, y_verdict_correct, rationale.''' 
    try:
        r=call_agy(prompt, model='claude-sonnet-4-6')
        return {'case_id':c['id'],'run':x['run'],'x_system':'B1','y_system':'CDE-STANDARD','judgment':r['text'],'model':r.get('model'),'latency_s':r.get('latency_s')}
    except Exception as e: return {'case_id':c['id'],'run':x['run'],'x_system':'B1','y_system':'CDE-STANDARD','error':str(e)}

def main():
    cases={c['id']:c for c in json.loads((ROOT/'cases/index.json').read_text())}
    rows=[json.loads(x) for x in (OUT/'raw_outputs.jsonl').read_text().splitlines()]
    by={(r['case_id'],r['run'],r['system']):r for r in rows}
    pairs=[]
    for cid,c in cases.items():
        for run in sorted(r['run'] for r in rows if r['case_id']==cid and r['system']=='B1'):
            pairs.append((c,by[(cid,run,'B1')],by[(cid,run,'CDE-STANDARD')]))
    with ThreadPoolExecutor(max_workers=8) as ex: results=[f.result() for f in as_completed([ex.submit(one,p) for p in pairs])]
    results.sort(key=lambda r:(r['case_id'],r['run']))
    (OUT/'raw_judgments.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in results))
    print(json.dumps({'judgments':len(results),'errors':sum('error' in r for r in results),'path':str(OUT/'raw_judgments.jsonl')}))
if __name__=='__main__': main()
