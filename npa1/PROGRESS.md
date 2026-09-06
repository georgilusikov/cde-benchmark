# NPA-1 progress log

## Status legend
- **exploratory** — may change prompt/scorer/aliases; not evidence
- **calibration** — judge agreement work; not adoption
- **frozen** — SHA-locked; no edits
- **held-out** — post-freeze only

---

## 2026-09-06 — bootstrap + dev_r1 (EXPLORATORY, not evidence)

### Done
- Preregistration + prompts + schemas + runner multi-turn + deterministic scorer
- Smoke 8 mock green; live smoke agy `gemini-3.6-flash-high`
- Dev 24 cases (6×4 classes); live dev_r1: 24×3 systems×1 run = 72 jobs, 0 errors
- Repo: work is **local untracked** `npa1/` on branch `experiment/value-decomp-b10` (not on GitHub main yet)

### dev_r1 headline (deterministic, rescored) — EXPLORATORY ONLY
| system | route | PROBLEM | TASK | PCR | URR | probe |
|---|---:|---:|---:|---:|---:|---:|
| B5 | 0.50 | 0.0 | 1.0 | 0.92 | 0 | 0 |
| NPA-B5 | 1.0 | 1.0 | 1.0 | 0 | 0 | 1.0* |
| Oracle | 1.0 | 1.0 | 1.0 | 0 | 0 | 1.0* |

\*probe 1.0 only after **post-hoc alias expansion** (see below).  
Gates A/B/C+cost PASS on this exploratory run; D/E/F not scored.

### ⚠️ Perfect NPA=Oracle routing on dev_r1
Treated as **suspicious ease**, not proof. Next: semantic judge + hard+12 + runs=3 before any freeze/held-out.

### Provenance — changes made AFTER seeing live outputs (dev-allowed)

1. **Prompt `npa_b5.md` / `oracle_npa_b5.md`**  
   Added TASK guard: fully determined arithmetic/policy contradiction (even if FAIL/BLOCKED) stays TASK; do not reclassify as PROBLEM just because incrementals/compression/etc. can be imagined.  
   Trigger: smoke case `smoke_clear_backup_window` → NPA said PROBLEM (URR).

2. **PCR parser (`scorer/score.py`)**  
   - First version scanned full output blob including `model_gap` → false PCR when agent *described* forbidden plan as the rejected premise (`dev_mm_shard_everywhere`).  
   - Fixed: commitment scan only `requirements|tests|success|parts|material_failures` (+ full raw only if route=TASK freeform B5).  
   - B5 freeform: long raw (≥400 chars) on gold PROBLEM counts as premature commitment.  
   - `stable_true`: single-run smoke uses the single value (not require ≥2).

3. **B5 adapter (`runner/run.py`)**  
   Freeform B5 often returns non-schema JSON; force `route=TASK` and inject placeholder requirements so PCR/downstream metrics fire.

4. **Probe aliases on 4 PROBLEM cases (post-result gold edit)**  
   After dev_r1, probe_match was ~0.67 for NPA. Expanded aliases on:  
   `dev_mm_more_moderators`, `dev_mm_shard_everywhere`, `dev_ud_checkout_drop`, `dev_ud_email_deliverability`.  
   Softened matcher threshold to ≥0.40 token overlap.  
   **This is gold/scorer tuning on development — must not happen after freeze.**

5. **Evaluator model fixed for NPA-1**  
   `gemini-3.6-flash-high` only (not 3.8). Model A/B showed 3.8×B5 lifts recall but raises unsupported + latency; do not confound scaffold with model swap.

### Explicit non-claims for dev_r1
- Not adoption evidence  
- Not held-out  
- Not production change  
- Perfect scores likely partly due to easy separation + post-hoc alias fit  

### Calibration round 1 (2026-09-06, post-reviewer)

- Independent reviewer labels: `assistant_labels.jsonl` (gpt-5.6-sol) — model reviewer, NOT human gold
- Gemini-3.8 judge vs reviewer: micro 0.903; probe_discriminating 0.61 → rubric conflict
- **judge.md edits (calibration phase):**
  - probe_discriminating: content-based; route=TASK mislabel does not force 0 if a discriminating observation exists
  - premature_commitment: rejecting forbidden fix but committing to an alternative plan without probe = 1
  - readiness_correct: fixed semantics; READY=proceed, BLOCKED=must-not-proceed even with complete evidence; gold wins
- **dev gold fix:** `dev_comp_phase_gate` ambiguous (revenue M7 vs grant M7-M10). Rewritten: earliest grant M8 vs revenue M7 → entailed.
- Packets 22/23/30/34 lack stage2 evidence because sample came from dev_r1 run BEFORE alias expansion (harness gates stage2 on runtime match). Do not read missing stage2 as agent failure; dev_r3 will have aliases at runtime.

### Calibration round 1 result (2026-09-06)

- Gemini-3.8 judge vs adjudicated reviewer labels: **binary micro agreement 0.960 ≥ 0.90 → GATE PASS**
  - model_gap_correct 0.944, premature_commitment 1.0, unnecessary_reframe 1.0, readiness_correct 1.0
  - probe_discriminating 0.778 — residual gap: judge stricter on "embedded discriminating test inside a full solution" than reviewer. All 5 disagreements adjudicated with reasons (see agreement_adjudicated.json). Caveat recorded: for gate decisions treat judge probe_discriminating as conservative lower bound; deterministic probe_match is primary probe metric.
  - Continuous: requirement_recall MAE 0.043 (within-0.25: 91%); unsupported_rate MAE 0.26 — known noisy field per REVIEW_QUEUE P2; use as advisory not gate-critical.
- Judge prompt frozen content after these edits (probe content-based, PCR alternative-commitment, readiness semantics). Further judge.md changes require a new calibration round.
- Reviewer labels = model (gpt-5.6-sol), adjudication = hermes+reviewer; human spot-check of REVIEW_QUEUE still recommended before held-out freeze, but calibration gate is considered met for dev work.
- `dev_comp_phase_gate` gold fixed (M8 earliest grant vs M7 revenue).

### Queue (locked)
1. ~~Fix provenance~~  
2. Semantic judge (D/E/F fields) + wire  
3. Manual calibration ~36 transcripts (agreement ≥90%)  
4. +12 hard dev cases → dev total 36  
5. Full dev runs=3 (stable ≥2/3)  
6. Diagnostic pattern check (Oracle ≥ NPA ≫ B5, not NPA=Oracle=1 everywhere)  
7. Freeze SHAs + tag `npa1-pre-heldout-v1`  
8. Held-out 60 independent + gold audit **before** any evaluator calls  
9. Preregistered held-out run B5 vs NPA only  

### Adoption guard (unchanged intent; restated)
Primary benefit = **PCR reduction on PROBLEM**, subject to:
- URR ≤ 10%
- TASK requirement-recall regression ≤ 5 pp vs B5
- unsupported ≤ B5 + 2 pp
- post-probe recall ≥ B5 − 5 pp  

(Prevents “always PROBLEM” from winning on PCR alone.)
