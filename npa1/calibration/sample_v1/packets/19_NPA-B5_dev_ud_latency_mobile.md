# Packet 19 | NPA-B5 | dev_ud_latency_mobile | run 1
class=UNDERDETERMINED_PROBLEM gold_route=PROBLEM

## BRIEF
Mobile p95 latency +40% after app release. Could be client regression OR backend slowdown. Backend dashboards incomplete in brief. Request: hotfix client performance.

## ARTIFACT
Mobile team RFC: ship client performance hotfix tomorrow.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Client-side regression vs backend regression.",
  "valid_models": [
    {
      "id": "A_client",
      "description": "app build regression",
      "implied_action": "client hotfix"
    },
    {
      "id": "A_backend",
      "description": "API slowdown",
      "implied_action": "backend fix"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_client_vs_server_spans",
      "description": "split p95 into client render vs network/API server time pre/post",
      "aliases": [
        "client vs server time breakdown",
        "RTT vs main-thread"
      ],
      "evidence_returned": "Server time +35pp of the regression; client main-thread flat; API /feed p95 180→620ms."
    }
  ],
  "forbidden_premature_commitments": [
    "ship client performance hotfix as primary without layer evidence"
  ],
  "stage2_requirements": [
    "fix backend /feed path first",
    "do not client-hotfix as primary"
  ],
  "stage2_material_failures": [
    "API /feed slowdown dominates"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "Restore mobile p95 latency without applying a wrong-layer fix.",
  "route": "PROBLEM",
  "supra_goal": "Restore mobile p95 latency performance to baseline.",
  "model_gap": "Whether the +40% mobile p95 latency spike is caused by a client-side regression or a backend slowdown is unresolved due to incomplete backend dashboards.",
  "competing_models": [
    "Client Regression Model: The +40% p95 latency spike is driven by client-side code changes introduced in the latest app release.",
    "Backend Slowdown Model: The +40% p95 latency spike is driven by server-side degradation, making a client hotfix a wrong-layer fix."
  ],
  "probe": "Inspect server request logs / APM trace breakdowns comparing client network timing vs backend processing duration for the mobile endpoints.",
  "success": [],
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Backend endpoint latency metrics and telemetry comparing pre-release vs post-release performance."
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
Server time +35pp of the regression; client main-thread flat; API /feed p95 180→620ms.

## AGENT STAGE2
{
  "intended_outcome": "Restore mobile /feed API p95 latency to baseline (~180ms) by resolving backend server-side processing slowdown.",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": [
    "Backend /feed API p95 latency reduced from 620ms back to baseline (<= 180ms).",
    "Mobile client overall p95 latency restored to pre-regression baseline."
  ],
  "parts": [
    {
      "component": "Backend /feed Endpoint Handler",
      "local_contribution": "Processes mobile client requests for /feed and orchestrates response generation within allocated server latency budget."
    },
    {
      "component": "Backend Subservices & Database",
      "local_contribution": "Executes data queries and RPC calls required to assemble /feed payload within server processing bounds."
    },
    {
      "component": "Client-Backend Interface",
      "local_contribution": "Transmits requests and receives payload without client main-thread blocking or network retry amplification."
    }
  ],
  "material_failures": [
    "Backend /feed processing latency regression (p95 spiked 180ms -> 620ms), accounting for +35pp of the total mobile regression.",
    "Downstream database query slowdown or RPC bottleneck within the /feed service handler.",
    "Interface handoff failure where increased server duration triggers client timeouts or retry loops despite flat client main-thread state."
  ],
  "requirements": [
    "Backend /feed service must process p95 requests in <= 180ms under production load.",
    "Backend database and RPC queries supporting /feed must complete within internal execution budgets (<= 150ms total server work).",
    "Client network interface must maintain request concurrency without triggering unneeded retries while waiting on /feed responses."
  ],
  "tests": [
    "APM trace breakdown and server request log profiling on /feed endpoint to confirm server-side duration p95 <= 180ms.",
    "Database query performance audit and microbenchmarks for backend /feed retrieval routines.",
    "End-to-end canary load test verifying overall mobile p95 latency returns to pre-regression baseline."
  ],
  "evidence_gaps": [
    "Internal trace breakdown (e.g. database query execution vs downstream microservice RPC) within the backend /feed endpoint implementation to pinpoint the specific code or infrastructure regression."
  ],
  "decision_readiness": "READY"
}