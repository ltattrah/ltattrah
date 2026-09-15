# Closest-work matrix

Topic 08: Beyond Static Recall: A Black-Box Consistency and Freshness Oracle for Mutable Vector Databases

Fill every row until at least five neighboring papers have an **exact** statement of how this paper's claim differs. Seeded from the audit; add the papers found in `search-log.csv`. Reference numbers link to `../../REFERENCES.md`.

| Work | Venue / year | What it claims | Method and data | Limitation it states | Exact claim difference from this paper | Status |
|---|---|---|---|---|---|---|
| SPFresh [[24]](https://arxiv.org/abs/2410.14452) | | In-place updates for billion-scale search | | | System; no black-box correctness oracle | seeded |
| Quantization under streaming updates [[25]](https://arxiv.org/abs/2512.18335) | | Formalizes consistency for a specific technique | | | Technique-level; this model is engine-independent and black-box | seeded |
| ANN benchmarks (ann-benchmarks, big-ann)  | | Static recall and latency | | | No mutations, versions, deletes, or restarts | seeded |
| Jepsen-style consistency testing  | | Histories and linearizability checkers for KV/SQL | | | Adapted to approximate top-k where exact equality is not the contract | seeded |
| Vector DB vendor consistency docs  | | Product-specific contracts | | | Treated as claims to test | seeded |
| | | | | | | to find |
| | | | | | | to find |
| | | | | | | to find |

## Claim–method–data–limitation notes

One subsection per paper read in full (target 25–40 by Day 14).

### <Author year> — <short title>
- **Claim:**
- **Method:**
- **Data / systems:**
- **Stated limitations:**
- **Relevance to RQs:**
- **Reusable artifact?**
