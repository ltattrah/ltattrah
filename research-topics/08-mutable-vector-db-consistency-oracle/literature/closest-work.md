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
| FreshDiskANN (Singh et al.) | arXiv 2021 | Streaming updates (insert/delete) for graph ANN with StreamingMerge | | | Index-internal update mechanism; no black-box contract oracle across engines | to verify |
| Elle / Jepsen (Kingsbury and Alvaro) | VLDB 2020 | Infers transactional anomalies from client-observed histories | | | Exact-equality histories for KV/SQL; here the answer is approximate top-k, so the oracle needs the tie group and the approximation class | to verify |
| big-ann-benchmarks streaming track | NeurIPS 2023 competition | Recall under a fixed insert/delete runbook | | | Measures recall only; no versions, filters, restarts, or failure classification | to verify |
| Filtered-DiskANN (Gollapudi et al.) / ACORN (Patel et al.) | WWW 2023 / SIGMOD 2024 | Filtered ANN search algorithms | | | Filter *performance*; here filter *consistency* under metadata upserts is a tested contract (C5) | to verify |
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
