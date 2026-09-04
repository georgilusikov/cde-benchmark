# CDE / What Matters — Criterion Discovery Engine benchmark

Reproducible, preregistered benchmark comparing B1 (strong structured prompt) with CDE v0.4. The benchmark is deliberately synthetic and adversarial: 5 domains, 20 artifacts (5 controls + 15 mutations), and a separate SPEC-mode requirement-discovery test.

## Status

The completed run answers only the **AUDIT** question (detect defects in an existing artifact). It does not answer the original **SPEC / requirements-discovery** question: the preregistered pre-artifact SPEC coverage phase was not executed. `REPORT.md` records this limitation. Dataset and gold are frozen before evaluator runs. `python runner/run.py --mode mock` is only a pipeline smoke test and MUST NOT be treated as evidence. Real runs require an evaluator provider configured in `runner/config.yaml` or environment variables. `results/` stores raw outputs and scores.

## Quick start

```bash
python -m pytest -q
python runner/run.py --mode mock --systems B1,CDE-STANDARD,CDE-LIGHT --runs 3
python scorer/report.py --results results --out REPORT.md
```

For real runs, set `CDE_API_BASE`, `CDE_API_KEY`, and `CDE_MODEL`, then use `--mode api`. The runner randomizes system order per case/run, records prompts and metadata, and never sends gold to the evaluator. Judge calls are intentionally a separate explicit phase.

## Decision rule

See `preregistration.md`. No threshold is changed after observing results. The mock smoke run is excluded from the decision.
