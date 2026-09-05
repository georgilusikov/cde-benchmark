# B4 (DEEP lenses) preregistration — FROZEN before first evaluator run

## Hypothesis

Independent coverage lenses (high recall) + separate conservative synthesizer
(high precision) increase material-failure coverage without raising false
requirements, resolving the B2/B3 trade-off inside one architecture instead of
one prompt.

## Comparison

- **B1**: `v3/prompts/b1.md`, unchanged, single pass.
- **B4**: B1-equivalent core question answered via 4 independent discovery
  lenses (no cross-visibility, no verdicts) + 1 separate synthesizer that alone
  decides DEFECT STATUS / DECISION READINESS under the B3 confirmation gate.

## Frozen files

- lenses: `v3/prompts/lens_constraint.md`, `lens_failure.md`, `lens_outcome.md`,
  `lens_domain_<sql|medical|summary|strategy|naming>.md` (selected by case
  domain, mapping below)
- synthesizer: `v3/prompts/b4_synth.md`
- cases: `v3/cases.json` (corrected v3.1 dataset, unmodified)
- gold: `v3/gold.json` (unmodified, hidden from evaluator and lenses)

## Domain lens mapping (frozen)

- sql → `lens_domain_sql.md` (runtime/data-integrity specialist)
- medical → `lens_domain_medical.md` (safety/contraindication specialist)
- summary → `lens_domain_summary.md` (fidelity/decision specialist)
- strategy → `lens_domain_strategy.md` (uncertainty/adaptation specialist)
- naming → `lens_domain_naming.md` (normative/linguistic-legal specialist)

## Protocol

- 25 cases × 2 systems × 3 runs = 150 jobs, randomized system order per case/run
- evaluator model/settings identical to v3.1: `gemini-3.6-flash-high` via agy
- lenses run in parallel with no shared context; synthesizer sees brief +
  artifact + the 4 lens outputs only (never gold)
- judged artifact for B4 is the synthesizer output only (lens outputs stored
  separately for transparency, never judged)
- same blind judge model/rubric as v3.1: `gemini-3.8-flash-high`
- quota/error retry with the same judge model only
- stable case result = ≥2/3 runs; scorer = `v3/score.py` ≥2/3 logic

## Cost accounting

Per B4 job: 5 model calls (4 lenses + 1 synth). Report calls, output chars,
latency median/p95 alongside quality metrics.

## Decision rule

B4 earns a permanent DEEP mode only if ALL hold:

1. Target Finding Recall ≥ B1
2. Finding Class Accuracy ≥ B1
3. Unsupported Confirmed Defect Rate ≤ B1
4. Readiness Calibration ≥ B1

If any fail: B4 FAILS — no B4.1, no prompt patching, freeze research and
select among already-tested simpler variants.
