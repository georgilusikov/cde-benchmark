# Packet 14 | NPA-B5 | dev_mm_cdn_more_pops | run 1
class=MODEL_MISMATCH gold_route=PROBLEM

## BRIEF
Request: buy 12 more CDN PoPs because TTFB p95 is 900ms in region R. Facts: origin p95 820ms; CDN cache hit ratio in R is 18%; HTML is marked uncacheable; edge already has PoPs in R.

## ARTIFACT
Proposal: purchase 12 additional PoPs in adjacent cities.

## GOLD (for labeler only — hide from naive second rater if testing pure blindness)
{
  "material_model_gap": "Whether latency is missing PoPs or uncacheable origin-bound responses.",
  "valid_models": [
    {
      "id": "A_pops",
      "description": "insufficient PoP density",
      "implied_action": "buy PoPs"
    },
    {
      "id": "A_cache",
      "description": "content uncacheable / origin slow",
      "implied_action": "fix cache headers/origin"
    }
  ],
  "acceptable_probes": [
    {
      "id": "probe_hit_ratio_origin",
      "description": "measure cache hit ratio and origin time share for R",
      "aliases": [
        "cdn hit ratio region R",
        "origin time vs edge"
      ],
      "evidence_returned": "Hit ratio 18%; 80% of TTFB is origin generate; Cache-Control: private no-store on HTML."
    }
  ],
  "forbidden_premature_commitments": [
    "buy 12 more PoPs",
    "purchase additional PoPs"
  ],
  "stage2_requirements": [
    "make cacheable assets cacheable",
    "reduce origin time before more PoPs"
  ],
  "stage2_material_failures": [
    "PoP purchase does not fix uncacheable origin-bound HTML"
  ],
  "stage2_readiness": "BLOCKED",
  "unnecessary_probe": false
}

## AGENT STAGE1
{
  "intended_outcome": "TTFB p95 <200ms for region R",
  "route": "PROBLEM",
  "supra_goal": "Achieve TTFB p95 <200ms in region R independent of CDN PoP expansion.",
  "model_gap": "The proposed solution assumes edge network latency and PoP density drive the 900ms TTFB p95 in region R, whereas facts show origin processing latency (820ms) and uncacheable HTML (18% cache hit ratio) dominate TTFB.",
  "competing_models": [
    "Model 1 (Proposal): High TTFB p95 (900ms) in region R is caused by insufficient edge CDN PoP coverage; purchasing 12 additional PoPs will reduce TTFB p95 to <200ms.",
    "Model 2 (Evidence-backed): High TTFB p95 (900ms) is driven by origin latency (820ms p95) and cache bypass (HTML uncacheable, 18% hit ratio); adding edge PoPs will have negligible impact on TTFB p95."
  ],
  "probe": "Profile request latency breakdown on existing region R PoPs (edge-to-origin transit vs origin processing time) and measure TTFB impact of caching HTML headers or optimizing origin response time.",
  "success": null,
  "parts": [],
  "material_failures": [],
  "requirements": [],
  "tests": [],
  "evidence_gaps": [
    "Origin latency breakdown (database queries, application rendering, backend API calls)",
    "Technical feasibility and policy constraints of enabling edge caching for HTML responses in region R"
  ],
  "decision_readiness": "BLOCKED"
}

## EVIDENCE
Hit ratio 18%; 80% of TTFB is origin generate; Cache-Control: private no-store on HTML.

## AGENT STAGE2
{
  "intended_outcome": "TTFB p95 <200ms for region R",
  "route": "TASK",
  "supra_goal": null,
  "model_gap": null,
  "competing_models": [],
  "probe": null,
  "success": "TTFB p95 for region R is verified to be under 200ms under representative production traffic.",
  "parts": [
    {
      "name": "Origin Application Rendering Engine",
      "local_contribution": "Generates dynamic HTML response payloads upon request receipt within origin latency budget."
    },
    {
      "name": "HTTP Cache Control Policy Interface",
      "local_contribution": "Defines response header directives that govern whether edge CDN PoPs store and serve responses."
    },
    {
      "name": "Edge CDN PoP Distribution Network",
      "local_contribution": "Terminates client connections in region R, serves cached HTML responses directly, and proxies cache misses to origin."
    }
  ],
  "material_failures": [
    {
      "mode": "Excessive Origin Generation Latency",
      "description": "Origin generate time accounts for 80% of TTFB (~720ms), making the 200ms TTFB target arithmetically impossible through edge network optimizations alone."
    },
    {
      "mode": "Cache Policy Contradiction",
      "description": "Cache-Control: private, no-store directive on HTML responses prevents edge caching, resulting in an 18% hit ratio and forcing 82% of traffic to execute full origin generation."
    },
    {
      "mode": "Edge-Origin Interface Handoff Failure",
      "description": "Edge CDN correctly honors non-cacheable headers, but the handoff design forces client requests directly to origin processing without edge caching benefit."
    }
  ],
  "requirements": [
    {
      "id": "REQ-1",
      "target": "Origin Processing Time",
      "specification": "Origin HTML generation time p95 must be <= 120ms."
    },
    {
      "id": "REQ-2",
      "target": "Cache Control Header Policy",
      "specification": "HTML Cache-Control header directive must permit edge caching or stale-while-revalidate strategy to achieve edge cache hit ratio >= 80% for region R."
    },
    {
      "id": "REQ-3",
      "target": "Edge-to-Origin Network Latency",
      "specification": "Combined client-to-edge and edge-to-origin transit latency must remain <= 60ms at p95."
    }
  ],
  "tests": [
    {
      "id": "TEST-1",
      "target_requirement": "REQ-1",
      "procedure": "Profile origin execution metrics during peak traffic in region R to verify HTML generation p95 is <= 120ms."
    },
    {
      "id": "TEST-2",
      "target_requirement": "REQ-2",
      "procedure": "Inspect HTML response headers and monitor edge CDN cache hit ratio for region R over a 24-hour window to confirm hit ratio >= 80%."
    },
    {
      "id": "TEST-3",
      "target_requirement": "REQ-3",
      "procedure": "Measure synthetic and RUM network RTT metrics between edge PoPs and backend origin servers for region R."
    }
  ],
  "evidence_gaps": [],
  "decision_readiness": "BLOCKED"
}