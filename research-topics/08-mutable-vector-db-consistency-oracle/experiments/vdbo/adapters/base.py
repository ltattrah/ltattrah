"""Adapter interface. Thin by design so that product releases do not invalidate the model."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from ..model import Filter, Hit, Record


class EngineAdapter(ABC):
    name: str = "abstract"
    metric: str = "l2"
    has_flush: bool = False  # True if flush() is a real synchronisation point (else visibility lag is unobservable)
    has_restart: bool = False
    advertised: dict[str, str] = {}  # contract name -> what the engine documents (filled per adapter)

    def __init__(self, path: str, dim: int, metric: str = "l2") -> None:
        self.path, self.dim, self.metric = path, dim, metric

    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def upsert(self, records: list[Record]) -> None: ...

    @abstractmethod
    def delete(self, ids: list[int]) -> None: ...

    @abstractmethod
    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]: ...

    @abstractmethod
    def get(self, record_id: int) -> Optional[Hit]: ...

    @abstractmethod
    def count(self) -> Optional[int]: ...

    def flush(self) -> None:  # noqa: B027 - optional hook
        pass

    def rebuild(self) -> None:  # noqa: B027 - optional hook
        pass

    def restart(self) -> None:
        self.close()
        self.open()

    def version_info(self) -> str:
        return "n/a"
