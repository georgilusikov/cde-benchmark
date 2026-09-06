# Semantic judge calibration

**Goal:** agreement ≥ 90% on binary fields before trusting D/E/F gates.

## Sample (~36 transcripts)
From an existing run dir (prefer `results/dev_r1` or later hard-dev run):

- 12 B5, 12 NPA-B5, 12 ORACLE-NPA-B5  
- Balanced across 4 base classes (and hard subclasses when present)  
- Mix stage1-only and multi-turn when available  

```bash
python3 runner/build_calibration_sample.py \
  --run-dir results/dev_r1 \
  --cases dev/cases.json \
  --out calibration/sample_v1 \
  --per-system 12
```

## Human labels
Edit `calibration/sample_v1/human_labels.jsonl` (one JSON per line).  
Required keys match judge.md binaries + recalls:

```json
{
  "case_id": "...",
  "system": "B5|NPA-B5|ORACLE-NPA-B5",
  "run": 1,
  "model_gap_correct": 0,
  "probe_discriminating": 0,
  "premature_commitment": 1,
  "unnecessary_reframe": null,
  "requirement_recall": 0.5,
  "unsupported_confirmed_count": 1,
  "unsupported_confirmed_rate": 0.25,
  "readiness_correct": null,
  "stage2_requirement_recall": null,
  "labeler": "georgiy|reviewer2",
  "notes": ""
}
```

Use `null` when field N/A (same rules as judge.md).

## Run judge on the same sample
```bash
python3 runner/judge_semantic.py \
  --run-dir results/dev_r1 \
  --cases dev/cases.json \
  --model gemini-3.8-flash-high \
  --systems B5,NPA-B5,ORACLE-NPA-B5
# then filter to sample ids, or pass --limit after seed for a pilot
```

Prefer: judge only sample rows via:

```bash
python3 runner/judge_semantic.py \
  --run-dir calibration/sample_v1 \
  --cases dev/cases.json \
  --model gemini-3.8-flash-high
```
(`build_calibration_sample.py` copies a mini raw_outputs.jsonl into the sample dir.)

## Agreement
```bash
python3 runner/calibration_agree.py \
  --human calibration/sample_v1/human_labels.jsonl \
  --judge calibration/sample_v1/semantic_judgments.jsonl \
  --out calibration/sample_v1/agreement.json
```

**Gate:** binary fields pairwise agreement ≥ 0.90 (ignoring null-null).  
All disagreements must be listed and resolved; judge prompt editable **only in calibration phase**.

## Fields that count as binary for the 90% gate
- model_gap_correct  
- probe_discriminating  
- premature_commitment  
- unnecessary_reframe  
- readiness_correct  

Continuous fields (requirement_recall, unsupported rate, stage2 recall): report MAE / within-0.25 agreement; not part of the 90% binary gate but must not be anti-correlated with human.
