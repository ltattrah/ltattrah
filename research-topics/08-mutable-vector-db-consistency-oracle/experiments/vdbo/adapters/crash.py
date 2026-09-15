"""Run any registered adapter inside a child process so the history can SIGKILL it mid-run.

A clean ``restart()`` lets an engine flush buffers in ``close()``. A ``crash()`` does not: the process is
killed with SIGKILL and a fresh process reopens the same on-disk path. What survives is what the engine
made durable *before acknowledging* the write, which is exactly the durability contract.
"""
from __future__ import annotations

import multiprocessing as mp
import os
import signal
from typing import Any, Optional

import numpy as np

from ..model import Filter, Hit, Record
from .base import EngineAdapter


def _worker(conn, engine_name: str, path: str, dim: int, metric: str) -> None:  # pragma: no cover - runs in child
    from . import make

    eng = make(engine_name, path=path, dim=dim, metric=metric)
    eng.open()
    conn.send(("ok", eng.version_info()))
    while True:
        cmd, args = conn.recv()
        if cmd == "close":
            try:
                eng.close()
            finally:
                conn.send(("ok", None))
            return
        try:
            conn.send(("ok", getattr(eng, cmd)(*args)))
        except Exception as exc:  # noqa: BLE001 - forwarded to the parent
            conn.send(("err", f"{type(exc).__name__}: {exc}"))


class CrashableEngine(EngineAdapter):
    has_flush = False
    has_restart = True
    has_crash = True

    def __init__(self, engine_name: str, path: str, dim: int, metric: str = "l2") -> None:
        super().__init__(path, dim, metric)
        from . import REGISTRY, available_real_engines

        base = {**REGISTRY, **available_real_engines()}[engine_name]
        self.engine_name = engine_name
        self.name = f"{engine_name}+crash"
        self.advertised = getattr(base, "advertised", {})
        self.metric = metric
        self._version = ""
        self.proc: Optional[mp.Process] = None
        self.crashes = 0

    # ---- process management ----
    def open(self) -> None:
        ctx = mp.get_context("spawn")
        self.conn, child = ctx.Pipe()
        self.proc = ctx.Process(target=_worker, args=(child, self.engine_name, self.path, self.dim, self.metric), daemon=True)
        self.proc.start()
        child.close()
        status, payload = self.conn.recv()
        if status != "ok":
            raise RuntimeError(payload)
        self._version = payload

    def close(self) -> None:
        if self.proc is not None and self.proc.is_alive():
            try:
                self.conn.send(("close", ()))
                self.conn.recv()
            except (EOFError, BrokenPipeError):
                pass
            self.proc.join(timeout=30)
        self.proc = None

    def crash(self) -> None:
        assert self.proc is not None
        os.kill(self.proc.pid, signal.SIGKILL)
        self.proc.join(timeout=30)
        self.crashes += 1
        self.open()

    def _call(self, cmd: str, *args: Any) -> Any:
        self.conn.send((cmd, args))
        status, payload = self.conn.recv()
        if status != "ok":
            raise RuntimeError(f"{self.engine_name}.{cmd}: {payload}")
        return payload

    # ---- forwarded operations ----
    def upsert(self, records: list[Record]) -> None:
        self._call("upsert", records)

    def delete(self, ids: list[int]) -> None:
        self._call("delete", ids)

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        return self._call("query", vector, k, filt)

    def get(self, record_id: int) -> Optional[Hit]:
        return self._call("get", record_id)

    def count(self) -> Optional[int]:
        return self._call("count")

    def flush(self) -> None:
        self._call("flush")

    def rebuild(self) -> None:
        self._call("rebuild")

    def version_info(self) -> str:
        return f"{self._version} [child process, SIGKILL crashes]"
