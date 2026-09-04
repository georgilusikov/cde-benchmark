import json
from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_frozen_dataset_has_20_cases_15_mutations_5_controls():
 d=json.loads((ROOT/'cases/index.json').read_text()); assert len(d)==20; assert sum('control' in x['tags'] for x in d)==5; assert sum('control' not in x['tags'] for x in d)==15
def test_gold_is_complete_and_pre_registered():
 g=json.loads((ROOT/'gold/gold.json').read_text()); assert g['frozen'] and g['created_before_evaluator_runs']; assert len(g['cases'])==20; assert {x['id'] for x in g['cases']}=={x['id'] for x in json.loads((ROOT/'cases/index.json').read_text())}
def test_no_real_drug_or_real_brand_claims():
 d=(ROOT/'cases/index.json').read_text().lower(); assert 'covelin' in d; assert 'real drug' not in d
