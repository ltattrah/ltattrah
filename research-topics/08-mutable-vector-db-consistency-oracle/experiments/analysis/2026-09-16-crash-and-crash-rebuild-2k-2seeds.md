| engine | version | queries | mean recall | queries w/ violation | stale | ghost | lag | filter | durability |
|---|---|---|---|---|---|---|---|---|---|
| reference+crash | n/a [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| chroma+crash | chromadb 1.5.9 (PersistentClient, HNSW) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| chroma-smallsync+crash | chromadb 1.5.9 (PersistentClient, HNSW, sync_threshold=20, batch_size=10) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| lancedb+crash | lancedb 0.38.0 (flat scan) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| lancedb-ivfflat+crash | lancedb 0.38.0 (IVF_FLAT at rebuild) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| milvus-lite+crash | pymilvus 3.0.1 / milvus-lite 3.2.1 (Strong, FLAT) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| milvus-lite-eventually+crash | pymilvus 3.0.1 / milvus-lite 3.2.1 (Eventually, FLAT) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| qdrant-local+crash | qdrant-client 1.19.0 (local mode) [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
| sqlite-vec+crash | sqlite-vec 0.1.9 on SQLite 3.45.1 [child process, SIGKILL crashes] | 744 | 1.0000 | 0 | 0 | 0 | 0 | 0 | 0 |
