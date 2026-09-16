# Semantic model for mutable vector search (v0.2, frozen candidate)

Status: **draft for the Day-30 protocol freeze.** Implemented in `../vdbo/` (`snapshot.py`, `oracle.py`, `runner.py`). Every term here is engine-independent; product behaviour enters only through the adapter's *advertised* column in §6.

## 1. Observables

A **collection** holds **records** `(id, version, vector, metadata)`. The client issues **operations**; the engine **acknowledges** each one before the next is issued (sequential mode). Concurrent mode (recorded interleavings) is out of scope for v0.1.

| Operation | Meaning |
|---|---|
| `insert(r)` | new id; `version = 1` |
| `upsert(r)` | existing id; `version = previous + 1`; replaces vector **and** metadata |
| `delete(id)` | removes the record |
| `query(q, k, φ)` | top-k by distance among records whose metadata satisfies filter `φ` |
| `get(id)` | point lookup |
| `count()` | number of live records |
| `flush` | client-visible synchronisation point, if the engine has one |
| `rebuild` | index rebuild / optimize / compaction hint |
| `restart` | clean close and reopen from the same path |
| `crash` | SIGKILL of the engine process, then reopen from the same path |
| `crash_rebuild` | `rebuild` issued, then SIGKILL after a delay drawn from [0, duration of the last rebuild] |

The version tag is stored in the payload (`_v`), so an engine that returns payloads makes versions observable without cooperation.

## 2. Logical snapshot

`S_i` is the state after the first `i` acknowledged operations: the map `live: id → record`, the set `deleted`, and for every id the **write position** and the **epoch** (number of restarts/crashes so far) of its last write or delete, plus a **synced** flag that becomes true once any flush, rebuild, restart, or crash has happened after the write.

**Exact answer.** `Exact(S, q, k, φ)` = the first `k` of `live` filtered by `φ`, ordered by `(distance(q, v), id)`. The **tie group** is every candidate whose distance equals the k-th distance (relative tolerance `1e-5`); any tie-group member may stand in for another.

## 3. Contracts

| # | Contract | Statement (after acknowledgement, at snapshot S) |
|---|---|---|
| C1 | Insert visibility | every live record is eligible to be returned by `query` |
| C2 | Read-your-write | `get(id)` returns the current version of a live id |
| C3 | Version replacement | no query or `get` returns a superseded version |
| C4 | Delete safety | no query or `get` returns a deleted id |
| C5 | Filter consistency | every returned item's **current** metadata satisfies `φ` |
| C6 | Durability | C1–C5 hold after `restart` and after `crash` for every acknowledged operation |
| C7 | Restart recovery | `count()` after `restart`/`crash` equals `|live|` |

An engine may **advertise** a weaker contract (for example eventual visibility until `flush`). The oracle records that per adapter (§6) and reports contract *ambiguities* separately from violations.

## 4. Failure classes and decision procedure

Each returned item and each missing exact neighbour receives exactly one class. Rules apply in order.

**Returned item `h = (id, version)`**

1. `id ∉ live`, `id ∈ deleted`, deleted in an earlier epoch → **durability loss** (delete undone by restart/crash).
2. `id ∉ live`, `id ∈ deleted`, delete not yet synced, item present on a repeat query and absent after `flush` → **visibility lag** (of the delete).
3. `id ∉ live` → **ghost result**.
4. `version ≠ current`, written in an earlier epoch → **durability loss** (upsert undone).
5. `version ≠ current`, write not yet synced, stable on repeat and current after `flush` → **visibility lag** (of the upsert).
6. `version ≠ current` → **stale version**.
7. current metadata violates `φ` → **filter inconsistency**.
8. `id ∉ Exact ∪ TieGroup` → **approximation** (valid but outside the exact set).
9. otherwise → ok.

**Missing exact neighbour `m`** (strictly inside the k-th distance, or a tie-group member when too few tie members were returned)

10. written in an earlier epoch and `get(m)` is absent or returns an old version → **durability loss**.
11. write not yet synced, absent on the repeat query, present after `flush` → **visibility lag**.
12. otherwise → **approximation** (counted in recall).

**Post-restart/crash probes** (independent of queries): sampled live ids must be returned by `get` with the current version; sampled deleted ids must not; `count()` must equal `|live|`. Any failure → **durability loss** with a detail string naming the write.

Only rules 8 and 12 depend on approximation tolerance, and they are reported as **recall**, not as violations. Rules 1–7 and 10–11 are tolerance-free; that is the claim the paper defends.

## 5. Probe protocol

Because approximate engines may be nondeterministic, **visibility lag** requires three observations: the original query, a **repeat query** with no intervening operation, and a query **after `flush`**. Lag is declared only when the discrepancy is identical on the first two and gone on the third. Without this rule a random top-k swap by an approximate engine can masquerade as lag (found by fault injection; see `LOG.md`).

The runner issues the repeat and flush probes only when a discrepancy involves an unsynced write or delete, so the probe cost is proportional to the number of fresh mutations near the query, not to the number of queries.

## 6. Adapters and advertised semantics

| Adapter | Mode | Sync point | Restart | Crash | Notes |
|---|---|---|---|---|---|
| `reference` | in-memory + atomic fsynced pickle | `flush` (no-op) | yes | yes | ground truth for the classifier |
| `faulty-*` | reference with one injected fault | varies | yes | yes | precision tests (`tests/test_oracle.py`) |
| `qdrant-local` | `QdrantClient(path=…)` | none exposed | yes | yes | local mode is a Python implementation, not the Rust server |
| `chroma` | `PersistentClient` (SQLite + HNSW) | none exposed | yes | yes | HNSW → approximate; index persisted every 1000 writes by default |
| `chroma-smallsync` | as above, `sync_threshold=20`, `batch_size=10` | none exposed | yes | yes | forces frequent HNSW persistence so crashes land between persist points |
| `lancedb` | embedded, flat scan | none | yes | yes | every write commits a new table version; `rebuild` = `optimize()` |
| `lancedb-ivfflat` | embedded, IVF_FLAT built at `rebuild` | none | yes | yes | rows written after the index are scanned unindexed |
| `milvus-lite` | `MilvusClient(uri=file)`, FLAT, `Strong` | `flush` (seals segments) | yes | yes | embedded Milvus core; `rebuild` = `compact()` |
| `milvus-lite-eventually` | as above at `Eventually` | `flush` | yes | yes | documented weaker visibility; none observed in Lite so far |
| `sqlite-vec` | `vec0` virtual table, exact, `synchronous=FULL` | none | yes | yes | transactional baseline; `rebuild` = `VACUUM` |

Crash mode wraps any adapter in a child process (`adapters/crash.py`) and kills it with SIGKILL, either between operations (`crash`) or while a rebuild is in flight (`crash_rebuild`).

## 7. Validation of the classifier

`tests/test_oracle.py` runs the same generated history against the reference engine (must be clean, recall 1.0) and five single-fault engines (each must produce **only** its own class). The approximate engine must produce no violation class and recall below 1.0. The reducer must shrink a ghost history to under a quarter of its length while preserving the class.

## 8. Known limitations of v0.1

- Sequential histories only; concurrent histories with recorded interleavings are Phase B work.
- Integer ids, one vector per record, one dense vector space, L2 metric by default.
- `flush` is a no-op on all three real engines, so visibility lag is unobservable there; any fresh-write discrepancy on them is classified as approximation with the detail "no flush probe available".
- Qdrant local mode is not the production server; a server-mode adapter (Docker) is needed before any claim about Qdrant.
- **SIGKILL is process-level durability, not power loss.** Data the engine handed to the kernel survives a kill even without `fsync`. Losing the page cache needs a block-device or VM-level fault injector (dm-log-writes / CrashMonkey-style); until then C6 is verified only against application buffers.
- Milvus Lite at `Eventually` shows the same behaviour as `Strong`; either Lite ignores the level in a single process or the window is shorter than one round trip. A server-mode Milvus adapter is needed to test the documented weakening.
- Scale so far: ≤ 50k vectors, dim ≤ 32 (see `LOG.md`). The evidence package requires 100k–1M.
