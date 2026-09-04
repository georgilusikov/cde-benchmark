import json,csv,re,argparse
from pathlib import Path

def score(root, results_dir=None):
 root=Path(root); results_dir=Path(results_dir) if results_dir else root/'results'; cases={c['id']:c for c in json.loads((root/'cases/index.json').read_text())}; rows=[]
 for line in (results_dir/'raw_outputs.jsonl').read_text().splitlines():
  r=json.loads(line); c=cases[r['case_id']]; t=r['output'].lower(); want='reject' if c['gold_verdict']=='REJECT' else 'accept' if c['gold_verdict']=='ACCEPT' else None
  rows.append({**r,'verdict_correct': bool(want and want in t),'defect_detected': bool(c['gold_defect'] and any(x in t for x in ['reject','gate','defect','error','missing','contradict','unsupported'])),'ignore_unsafe': bool(c['gold_defect'] and 'ignore' in t and any(x in t for x in ['critical','normative','gate']))})
 with (results_dir/'scores.json').open('w') as f: json.dump(rows,f,indent=2,ensure_ascii=False)
 return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1])); a=ap.parse_args(); print('scored',len(score(a.root)))
