# Packet 10 | B5 | dev_mm_cdn_more_pops | run 1
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
  "COMPONENTS_AND_INTERFACES": [
    {
      "component": "Edge PoP Layer",
      "local_contribution": "Terminates client TCP/TLS connections in Region R and serves cached responses with minimal network RTT.",
      "interface_with_next": "Passes incoming requests to Cacheability & Policy Layer for cache lookup."
    },
    {
      "component": "Cacheability & Policy Layer",
      "local_contribution": "Evaluates HTTP headers and caching policies to serve responses from edge cache or trigger an origin fetch.",
      "interface_with_next": "Routes cache-miss requests across the Edge-to-Origin network handoff."
    },
    {
      "component": "Edge-to-Origin Handoff & Transport",
      "local_contribution": "Transfers cache-miss requests from edge PoPs to backend origin infrastructure over backhaul connections.",
      "interface_with_next": "Delivers HTTP request payload to Origin Application Layer."
    },
    {
      "component": "Origin Application Layer",
      "local_contribution": "Executes backend code, database queries, and dynamic rendering to generate HTML responses.",
      "interface_with_next": "Returns HTML HTTP response payload back through edge to client."
    }
  ],
  "SUCCESS": false,
  "CONFIRMED MATERIAL FAILURES": [
    "Proposal misidentifies the primary latency bottleneck: 12 additional CDN PoPs are requested to lower TTFB, but origin latency alone is 820ms p95 (accounting for ~91% of the 900ms total TTFB).",
    "Proposal ignores the root cause of edge cache misses: HTML is marked uncacheable, resulting in a low CDN cache hit ratio of 18% in Region R and forcing 82% of requests to hit the 820ms origin.",
    "Redundant infrastructure expansion: Region R already has edge PoPs. Adding 12 PoPs in adjacent cities will not reduce origin processing time or fix uncacheable HTML headers."
  ],
  "EVIDENCE GAPS / ASSUMPTIONS": [
    "Lack of origin latency decomposition (e.g., breakdown between backend application code execution, database latency, and backhaul network transit).",
    "Unspecified justification for marking HTML uncacheable (e.g., dynamic user sessions vs missing or misconfigured Cache-Control headers).",
    "Lack of baseline client-to-edge network latency metrics for existing PoPs in Region R."
  ],
  "REQUIREMENTS + TESTS": [
    {
      "component": "Cacheability & Policy Layer",
      "coherent_quality_responsibility": "Maximize edge cacheability of HTML responses",
      "material_failure_mode": "HTML marked uncacheable causes 82% of requests to bypass edge cache and hit origin.",
      "requirement": "Refactor HTML response caching strategy (e.g., decouple personalized state, use stale-while-revalidate, or implement Edge Side Includes) to achieve cache hit ratio >= 85% in Region R.",
      "test": "Audit response Cache-Control headers and verify Region R cache hit ratio telemetry post-deployment."
    },
    {
      "component": "Origin Application Layer",
      "coherent_quality_responsibility": "Deliver fast backend response processing for cache misses",
      "material_failure_mode": "Origin processing latency of 820ms p95 makes achieving overall TTFB p95 < 200ms impossible on cache misses.",
      "requirement": "Origin p95 processing latency must be reduced to < 150ms for uncached requests.",
      "test": "Execute load testing against origin endpoints and measure APM p95 response time under Region R load."
    },
    {
      "component": "Edge PoP Layer",
      "coherent_quality_responsibility": "Provide low RTT edge connectivity in Region R",
      "material_failure_mode": "Edge network latency to local clients exceeds latency budget.",
      "requirement": "Edge network RTT + cached response TTFB must be < 50ms p95 in Region R.",
      "test": "Synthetic probes measuring client-to-edge RTT and cached response TTFB across Region R ISP networks."
    },
    {
      "component": "Interface: Cache Miss Handoff (Edge -> Origin)",
      "coherent_quality_responsibility": "Efficient handoff of cache misses from edge to origin",
      "material_failure_mode": "Edge PoP and Origin are locally functional, but handoff forwards 82% of uncacheable traffic directly into an 820ms origin bottleneck.",
      "requirement": "Handoff must optimize backhaul transit (e.g., persistent connection pools, origin shield) and minimize origin request rate.",
      "test": "Trace edge-to-origin request latency on cache misses and monitor origin shield request deduplication efficiency."
    }
  ],
  "NON-BLOCKING IMPROVEMENTS": [
    "Deploy CDN Origin Shielding to collapse concurrent cache-miss requests into single origin fetches.",
    "Enable persistent HTTP/2 or HTTP/3 connection reuse on the edge-to-origin backhaul.",
    "Explore Edge Compute workers to render personalized HTML dynamically at the edge."
  ],
  "WHAT NOT TO SPEND TIME ON": [
    "Procuring, provisioning, or benchmarking 12 additional CDN PoPs in adjacent cities.",
    "Optimizing edge-to-client routing in Region R prior to fixing HTML cacheability and origin latency."
  ],
  "DEFECT STATUS": "FAIL",
  "DECISION READINESS": "READY",
  "route": "TASK",
  "requirements": [
    "(freeform B5 solution output)"
  ],
  "material_failures": [
    "(see raw)"
  ]
}

## EVIDENCE
(none)

## AGENT STAGE2
{}