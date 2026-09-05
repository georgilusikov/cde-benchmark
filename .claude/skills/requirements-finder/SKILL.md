---
name: requirements-finder
description: Identify what materially matters for a task, artifact, or decision; derive concise requirements and tests; audit existing work without inventing defects. Use when asked what matters, what is required, what could fail, how to validate it, or what not to optimize.
---

# Requirements Finder / What Matters

## Purpose

Determine the smallest set of things that materially affect the intended outcome.

The production principle is:

`OUTCOME + EXPLICIT MUSTS + MATERIAL FAILURE MODES -> REQUIREMENTS -> TESTS`

Keep this skill simple. The benchmark did not justify CDE routing, fixed quality taxonomies, mandatory relational passes, debate, multi-agent lenses, or a DEEP mode.

## Default behavior

1. Use one reasoning pass by default.
2. Start from the supplied brief/context. Do not invent missing facts, schemas, preferences, regulations, or source content.
3. Prefer decision-changing requirements over generic best practices.
4. Missing evidence is not itself a defect.
5. Do not run broad subagent critique, role panels, voting, or parallel failure discovery.
6. If a specific decision-relevant evidence gap remains and tools/sources can resolve it, do one narrow targeted lookup or specialist check for that gap, then reassess. Do not broaden the search into general criticism.

## Choose the mode

### SPEC mode — before the object exists

Use when the user wants requirements, criteria, acceptance conditions, or a specification before creating something.

Use the empirically strongest simple instruction:

> You are given only a brief before an object exists. Produce a concise set of pre-creation requirements that would let a later reviewer detect decision-changing failures. Separate REQUIREMENT, MEASURE, TEST, ASSUMPTION, and RISK. Include acceptance gates and what evidence is needed. Do not invent the future artifact or its mutations.

Prioritize:
- explicit mandatory constraints;
- requirements that directly support the intended outcome;
- material ways the outcome could fail;
- falsifiable checks that would reveal those failures.

Prune requirements that neither prevent a material failure nor directly support the intended outcome.

### AUDIT mode — an object already exists

Use when evaluating an artifact against a brief, source, requirement, or intended outcome.

Use the tested B1 semantics:

> You are evaluating a supplied object against a brief. Output exactly: SUCCESS; CONFIRMED MATERIAL FAILURES; EVIDENCE GAPS / ASSUMPTIONS; REQUIREMENTS + TESTS; NON-BLOCKING IMPROVEMENTS; WHAT NOT TO SPEND TIME ON; DEFECT STATUS: PASS or FAIL; DECISION READINESS: READY, NEEDS_EVIDENCE, or BLOCKED. Missing evidence is not a defect. Do not invent facts.

Interpretation:
- `CONFIRMED MATERIAL FAILURES`: only failures supported by supplied facts/source material.
- `EVIDENCE GAPS / ASSUMPTIONS`: uncertainties that could change the decision but are not proven defects.
- `NON-BLOCKING IMPROVEMENTS`: useful improvements that do not change the core verdict.
- `WHAT NOT TO SPEND TIME ON`: criteria or polish that do not materially affect the intended outcome.

## Failure-first reasoning

Use failure thinking as a discovery aid, not as a reason to become suspicious of everything.

Ask:

> What realistic change or condition would make the intended result materially wrong, unusable, unsafe, misleading, or decision-irrelevant?

Then derive:

`FAILURE -> REQUIREMENT -> FALSIFIABLE TEST`

Do not force a universal checklist of interaction, timing, cardinality, lifecycle, UX, legal, risk, etc. Consider such issues when the task itself makes them relevant.

## Targeted evidence acquisition

Only after the simple pass identifies a concrete gap:

1. State the exact unknown.
2. Explain why resolving it could change a requirement or verdict.
3. Retrieve/check only that evidence.
4. Update the conclusion.

Examples:
- unknown SQL cardinality -> inspect schema/data relation;
- unknown legal requirement -> targeted legal/source lookup;
- unknown statistical significance -> inspect source analysis/data;
- unknown linguistic acceptability -> targeted linguistic evidence.

Do not ask several agents to independently search for more problems. Benchmarks showed this amplified suspicion and false defects without improving stable recall.

## Stop rule

Stop when each retained requirement either:
- is explicitly mandatory;
- directly supports the intended outcome; or
- prevents a material failure;

and each decision-changing uncertainty is either resolved or clearly labeled as an evidence gap.

Do not add framework layers merely because more criteria can be imagined.
