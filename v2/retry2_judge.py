import json,subprocess,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'; cs={c['id']:c for c in json.loads((ROOT/'cases.json').read_text())}
keys=[('d4_strategy_v2_clean_ready',3,'B1'),('d4_strategy_v2_clean_ready',3,'B2'),('d5_naming_19_v2',1,'B2'),('d5_naming_v2_clean_incomplete',2,'B1'),('d5_naming_v2_clean_ready',3,'B1'),('d5_naming_v2_clean_ready',2,'B1'),('d5_naming_20_v2',3,'B1')]
raw={ (r['case_id'],r['run'],r['system']):r for r in map(json.loads,(OUT/'raw_outputs.jsonl').read_text().splitlines()) }
J='Return JSON only with keys defect_status, decision_readiness, defect_status_correct, readiness_correct, false_defect, rationale. PASS means no demonstrated violation; missing evidence means NEEDS_EVIDENCE, not FAIL.'
out=[]
for key in keys:
 c=cs[key[0]]; r=raw[key]; p=J+'\nGold labels: '+json.dumps({'defect_status':c['gold_defect_status'],'readiness':c['gold_readiness']})+'\nBrief: '+c['brief']+'\nArtifact: '+c['artifact']+'\nOutput to judge:\n'+r['output'][:12000]
 q=subprocess.run(['agy','--model','gemini-3.8-flash-high',f'--print={p}','--print-timeout=120s'],capture_output=True,text=True,timeout=140)
 out.append({'case_id':key[0],'run':key[1],'system':key[2],'judgment':q.stdout.strip(),'error':None if q.returncode==0 else q.stderr.strip()})
Path(OUT/'retry2_judgments.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out)); print(json.dumps({'retried':len(out),'errors':sum(bool(x['error']) for x in out)}))
