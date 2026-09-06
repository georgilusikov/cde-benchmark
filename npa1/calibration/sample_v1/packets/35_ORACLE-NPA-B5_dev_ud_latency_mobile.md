# Packet 35 | ORACLE-NPA-B5 | dev_ud_latency_mobile | run 1
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
  "intended_outcome": "Restore mobile p95 latency without wrong-layer fix.",
  "route": "PROBLEM",
  "supra_goal": "Restore mobile p95 latency to baseline performance by addressing the true root cause rather than shipping a wrong-layer fix.",
  "model_gap": "Whether the 40% p95 latency increase is caused by a client-side release regression or backend service slowdown.",
  "competing_models": [
    "Client-side Regression Model: The mobile release introduced client-side performance degradation (e.g., UI main thread blocking, redundant network calls, inefficient serialization).",
    "Backend Slowdown Model: Backend API endpoints or downstream services slowed down independently of client code changes, manifesting as higher p95 latency on mobile."
  ],
  "probe": "Compare backend APM/server response time metrics during the release window against client network request execution breakdown (server duration vs network/client processing duration).",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Complete backend service/endpoint latency dashboards for the app release window",
    "Client-side APM breakdown separating network transmission/server time from client processing time"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}

## EVIDENCE
Server time +35pp of the regression; client main-thread flat; API /feed p95 180→620ms.

## AGENT STAGE2
{
  "intended_outcome": "Restore mobile p95 latency without wrong-layer fix.",
  "route": "PROBLEM",
  "supra_goal": "Restore mobile p95 latency to baseline performance by addressing the backend /feed service root cause rather than shipping a wrong-layer fix.",
  "model_gap": "Whether the /feed endpoint p95 latency regression (180ms to 620ms) is caused by database query execution slowdown or downstream microservice latency.",
  "competing_models": [
    "Database Layer Regression Model: The /feed endpoint slowdown is driven by unindexed queries, database contention, or cache misses within the feed data tier.",
    "Downstream Service Dependency Model: The /feed endpoint slowdown is driven by latency, queuing, or blocking RPC calls to downstream microservices."
  ],
  "probe": "Analyze backend distributed APM traces for /feed p95 requests to isolate time spent in database execution versus downstream microservice RPC calls.",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Backend APM distributed trace breakdown for /feed endpoint p95 requests separating database execution duration from downstream service call latency"
  ],
  "decision_readiness": "NEEDS_EVIDENCE"
}