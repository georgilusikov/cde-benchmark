# NPA-1 — FREEZE and HELDOUT execution checklist

**Do not skip steps. Do not start held-out evaluator calls before freeze tag.**

Evaluator model for all NPA-1 evidence runs: `gemini-3.6-flash-high` (agy).  
Judge model (after calibration lock): `gemini-3.8-flash-high` unless calibration says otherwise.  
Do **not** change model and scaffold in the same experiment.

---

## Phase A — Provenance (done when checked)

- [x] `PROGRESS.md` records post-output prompt/parser/alias changes
- [x] dev_r1 marked **exploratory, not evidence**
- [x] Perfect NPA=Oracle flagged as ease risk
- [ ] Local `npa1/` committed on experiment branch (optional until freeze; not required on GitHub main)

---

## Phase B — Semantic judge

- [x] `prompts/judge.md` with fixed JSON keys (no overall quality score)
- [x] `runner/judge_semantic.py`
- [ ] Run judge on calibration sample (not full 324 yet)
- [ ] Human labels on ~36 packets
- [ ] `calibration_agree.py` → binary micro-agreement ≥ 0.90
- [ ] All disagreements adjudicated; judge prompt frozen after that

Commands:

```bash
python3 runner/build_calibration_sample.py \
  --run-dir results/dev_r1 --cases dev/cases.json \
  --out calibration/sample_v1 --per-system 12

# label packets in calibration/sample_v1/packets/ → human_labels.jsonl

python3 runner/judge_semantic.py \
  --run-dir calibration/sample_v1 \
  --cases dev/cases.json \
  --model gemini-3.8-flash-high

python3 runner/calibration_agree.py \
  --human calibration/sample_v1/human_labels.jsonl \
  --judge calibration/sample_v1/semantic_judgments.jsonl \
  --out calibration/sample_v1/agreement.json
```

If agreement < 90%: edit **judge.md only**, rebuild labels as needed, repeat.  
Do not edit NPA prompt to fit judge.

---

## Phase C — Hard development (falsification)

- [x] +12 hard cases authored (`dev/hard12_cases.json`, merged into `dev/cases.json` → 36)
- [ ] Smoke hard-only optional:  
  `python3 runner/run.py --cases dev/hard12_cases.json --systems B5,NPA-B5,ORACLE-NPA-B5 --runs 1 --mode agy --out results/dev_hard12_r1`
- [ ] Expectation: if NPA stays perfect on hard12, signal stronger; if collapses, tune **on dev only**

Hard subclasses:
- TASK_WITH_MISSING_INFO
- TASK_WITH_FALSE_USER_CAUSAL_STORY
- PROBLEM_WITH_TEMPTING_DEFAULT
- PROBLEM_WITH_BAD_OBVIOUS_PROBE

---

## Phase D — Full development runs=3

Only after judge calibration gate passes (or explicitly waived with written reason).

```bash
python3 runner/run.py \
  --cases dev/cases.json \
  --systems B5,NPA-B5,ORACLE-NPA-B5 \
  --runs 3 --mode agy --model gemini-3.6-flash-high \
  --workers 8 --out results/dev_r3

python3 runner/judge_semantic.py \
  --run-dir results/dev_r3 \
  --cases dev/cases.json \
  --model gemini-3.8-flash-high
```

Budget order-of-magnitude: 36 × 3 × 3 = 324 stage1 calls (+ PROBLEM stage2).

Stable = ≥2/3.

### Diagnostic pattern gate (before freeze)

Want roughly:

| Metric | B5 | NPA | Oracle |
|---|---|---|---|
| PROBLEM recall | low | high | ≈1 |
| URR | low | ≤0.10 | ≈0 |
| PCR | high | ≪ B5 | ≈0 |
| Probe disc. | low | high | high |
| D/E/F | baseline | not worse | ceiling |

**Red flag:** NPA = Oracle = 1.00 on *every* metric including hard subclasses → held-out must be harder; do not freeze claiming victory.

**Adoption-style guard on dev (informational, not held-out):**  
PCR reduction subject to URR≤10%, TASK recall regression≤5pp, unsupported≤B5+2pp, post-probe recall≥B5−5pp.

---

## Phase E — FREEZE (no edits after)

Record SHAs:

```bash
cd npa1
sha256sum prompts/npa_b5.md prompts/b5.md prompts/judge.md prompts/oracle_npa_b5.md \
  scorer/score.py runner/run.py runner/judge_semantic.py \
  dev/cases.json > FREEZE_SHA256.txt
git add -A npa1
git commit -m "npa1: freeze pre-heldout v1"
git tag npa1-pre-heldout-v1
```

Fill:

| Artifact | SHA256 |
|---|---|
| NPA_PROMPT | |
| B5_PROMPT | |
| JUDGE_PROMPT | |
| SCORER | |
| RUNNER | |
| JUDGE_RUNNER | |
| DEV_DATA | |
| git tag | `npa1-pre-heldout-v1` |
| evaluator model | `gemini-3.6-flash-high` |
| judge model | |

**After tag: zero prompt/parser/alias/threshold changes.**

---

## Phase F — Held-out 60 (independent authoring)

Distribution:
- 15 CLEAR_TASK
- 15 COMPOSITE_TASK
- 15 MODEL_MISMATCH
- 15 UNDERDETERMINED_PROBLEM

Within each class: 5 easy / 5 medium / 5 adversarial.  
≥20/60 with plausible distractor that can induce wrong route.  
**Do not** clone dev with noun swaps.

### Gold audit (before any evaluator call)

For each PROBLEM, independent reviewer proves:
1. Model A consistent with all stage-1 facts  
2. Model B consistent with all stage-1 facts  
3. Action(A) ≠ Action(B)  
4. Named probe separates A/B  

For each TASK:
- No unresolved fact can materially change the required decision  

Fail any proof → drop case.

Audit checklist file: `heldout/GOLD_AUDIT.md` (create at authoring).

---

## Phase G — Held-out run

```bash
# ONLY after freeze + gold audit complete
python3 runner/run.py \
  --cases heldout/cases.json \
  --systems B5,NPA-B5 \
  --runs 3 --mode agy --model gemini-3.6-flash-high \
  --out results/heldout_v1

python3 runner/judge_semantic.py \
  --run-dir results/heldout_v1 \
  --cases heldout/cases.json \
  --model gemini-3.8-flash-high
```

- No intermediate scoreboard peek that triggers methodology change  
- Prefer finish all evaluator calls, then judge, then one report  
- Apply **only** preregistered gates in `preregistration.md`  
- Oracle not in held-out adoption decision  

### Primary endpoint
PCR reduction on PROBLEM, **subject to** composite guard (URR, TASK recall, unsupported, post-probe recall).

---

## Phase H — Outcomes

| Result | Action |
|---|---|
| Fail gates | Keep B5 production; close or redesign under new prereg |
| Oracle≫NPA, NPA fails | Idea OK, router weak — routing-only follow-up |
| Pass all + guard | Canary 100 real tasks; no algo change during canary |
| Pass synthetic only | Not enough for merge |

Production Requirements Finder stays frozen until canary policy in preregistration §12.

---

## Explicit forbidden actions
- Held-out before freeze tag  
- Alias expansion after freeze  
- Switching evaluator to 3.8 mid-NPA  
- Changing PCR threshold after seeing held-out  
- Treating dev_r1 perfect scores as evidence  
- Shipping NPA because “always PROBLEM” lowered PCR without URR/TASK guards  
