"""vdbo — black-box consistency and freshness oracle for mutable vector databases.

Modules
-------
model      Records, filters, operations, histories (the observable vocabulary).
generator  Deterministic version-tagged history generator.
snapshot   Logical snapshot state machine (the ground truth the engine is compared against).
oracle     Exact top-k under filters with explicit tie rules, and the discrepancy classifier.
runner     Executes a history against an adapter in lockstep with the snapshot; collects findings.
reducer    Delta-debugging minimizer for failing histories.
adapters   Engine adapters: reference (correct), faulty variants, Qdrant local, Chroma, LanceDB.
"""
from .model import Filter, History, Hit, Op, OpKind, Record
from .oracle import FailureClass, Finding

__all__ = ["Filter", "History", "Hit", "Op", "OpKind", "Record", "FailureClass", "Finding"]
