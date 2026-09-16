| engine | version | queries | mean recall | queries w/ violation | stale | ghost | lag | filter | durability |
|---|---|---|---|---|---|---|---|---|---|
| reference | n/a | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| chroma | chromadb 1.5.9 (PersistentClient, HNSW) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| chroma-smallsync | chromadb 1.5.9 (PersistentClient, HNSW, sync_threshold=20, batch_size=10) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| lancedb | lancedb 0.38.0 (flat scan) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| lancedb-ivfflat | lancedb 0.38.0 (IVF_FLAT at rebuild) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| milvus-lite | pymilvus 3.0.1 / milvus-lite 3.2.1 (Strong, FLAT) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| milvus-lite-eventually | pymilvus 3.0.1 / milvus-lite 3.2.1 (Eventually, FLAT) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| qdrant-local | qdrant-client 1.19.0 (local mode) | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| sqlite-vec | sqlite-vec 0.1.9 on SQLite 3.45.1 | 352 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
