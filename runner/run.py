import argparse, json, random, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from providers import call_api, call_agy

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = {'B0':'baseline_b0.md','B1':'baseline_b1.md','CDE-STANDARD':'cde_standard.md','CDE-LIGHT':'cde_light.md'}

def load():
    return json.loads((ROOT/'cases/index.json').read_text()), json.loads((ROOT/'gold/gold.json').read_text())

def one(job, mode):
    c, run, system = job
    prompt = (ROOT/'prompts'/PROMPTS[system]).read_text() + '\n\nBRIEF:\n' + c['brief'] + '\n\nARTIFACT:\n' + c['artifact']
    meta = {}
    try:
        r = call_agy(prompt) if mode == 'agy' else call_api(prompt, config={})
        text, meta = r['text'], {k:r.get(k) for k in ('usage','latency_s','model')}
    except Exception as e:
        text, meta = 'ERROR: ' + str(e), {'error': str(e)}
    return {'case_id':c['id'],'system':system,'run':run,'output':text,'gold_sent':False,'mode':mode,**meta}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['mock','api','agy'], required=True)
    ap.add_argument('--systems', default='B0,B1,CDE-STANDARD,CDE-LIGHT')
    ap.add_argument('--runs', type=int, default=3)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--seed', type=int, default=404)
    a = ap.parse_args()
    cases, _ = load(); systems = a.systems.split(',')
    if any(s not in PROMPTS for s in systems): raise ValueError('unknown system')
    out = ROOT/'results'/('agy_parallel' if a.mode == 'agy' and a.workers > 1 else a.mode)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    jobs=[]
    for c in cases:
        for run in range(1, a.runs+1):
            order=systems[:]; rng.shuffle(order)
            jobs.extend((c,run,s) for s in order)
    manifest={'mode':a.mode,'seed':a.seed,'systems':systems,'runs':a.runs,'workers':a.workers,'jobs':len(jobs),'gold_hidden':True,'started':time.time()}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    results=[]
    if a.mode == 'mock':
        for c,run,s in jobs:
            results.append({'case_id':c['id'],'system':s,'run':run,'output':'SMOKE_ONLY: '+('REJECT' if c['gold_defect'] else 'ACCEPT'),'gold_sent':False,'mode':'mock'})
    else:
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futures=[ex.submit(one,j,a.mode) for j in jobs]
            for f in as_completed(futures): results.append(f.result())
    results.sort(key=lambda r:(r['case_id'],r['run'],r['system']))
    with (out/'raw_outputs.jsonl').open('w') as f:
        for r in results: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    (out/'RUN_COMPLETE').write_text('Pipeline completed. Mock outputs are excluded from empirical conclusions.\n')
    print(json.dumps({'completed':len(results),'output_dir':str(out),'workers':a.workers}))

if __name__=='__main__': main()
