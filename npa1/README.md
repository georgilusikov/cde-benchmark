# NPA-1 — Problem/Task Router Benchmark

Separate experiment under `cde-benchmark`. **Does not change production Requirements Finder / B5.**

See `preregistration.md` for locked design, metrics, and adoption gates.

## Layout

```
npa1/
├── README.md
├── preregistration.md
├── schema/           # case + output JSON schemas
├── prompts/          # b5.md (frozen copy), npa_b5.md, oracle, judge
├── smoke/cases.json  # 8 infrastructure cases
├── dev/cases.json    # 24 development cases (6×4 classes)
├── heldout/          # 60 cases later (frozen)
├── adversarial/      # 10 post-decision framing cases
├── runner/run.py     # mock|agy, multi-turn probe harness
├── scorer/score.py   # deterministic route/PCR/URR/probe + gates
└── results/
```

## Status

- [x] Preregistration + prompts + schemas + runner + deterministic scorer
- [x] Smoke + live smoke; dev_r1 exploratory (perfect scores = ease risk)
- [x] Provenance logged in `PROGRESS.md`
- [x] Semantic judge prompt + `runner/judge_semantic.py`
- [x] Calibration harness (`build_calibration_sample`, `calibration_agree`)
- [x] +12 hard dev cases → **36** total in `dev/cases.json`
- [x] `FREEZE_AND_HELDOUT.md` checklist
- [ ] Human calibration labels (agreement ≥90%)
- [ ] Dev runs=3 on 36
- [ ] Freeze tag `npa1-pre-heldout-v1`
- [ ] Held-out 60

## Quick start

```bash
# harness only (not evidence)
python3 runner/run.py --cases smoke/cases.json --systems B5,NPA-B5,ORACLE-NPA-B5 --runs 1 --mode mock

# calibration sample from existing run
python3 runner/build_calibration_sample.py --run-dir results/dev_r1 --cases dev/cases.json --out calibration/sample_v1

# semantic judge
python3 runner/judge_semantic.py --run-dir calibration/sample_v1 --cases dev/cases.json --model gemini-3.8-flash-high

# follow FREEZE_AND_HELDOUT.md — do not jump to held-out
```

Production B5 remains untouched until NPA passes **all** preregistered gates **and** canary.
