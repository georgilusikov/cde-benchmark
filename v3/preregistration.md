# v3 preregistration

Compare B1, B2, B3 on 25 real artifacts: 10 controls (5 CLEAN_READY, 5 CLEAN_INCOMPLETE) and 15 single-failure mutations, 3 runs each, randomized ordering. Gold contains TARGET FINDING, TARGET CLASS (CONFIRMED_DEFECT/EVIDENCE_GAP/NON_BLOCKING/NONE), EXPECTED STATUS, EXPECTED READINESS. Evaluator sees no gold.

Primary metrics: TARGET FINDING RECALL and TARGET CLASS ACCURACY at >=2/3 runs; unsupported confirmed-defect rate; readiness calibration; output size and latency (median and p95). Status is parsed deterministically from explicit headings. LLM judge asks only target detected, target class correct, unsupported confirmed defect. One judge model is used; quota failures are retried with the same model, never fallback.

B3 passes only if recall >= B2, class accuracy > B2, unsupported confirmed defects <= B1, readiness >= B2, and output size < B2.
