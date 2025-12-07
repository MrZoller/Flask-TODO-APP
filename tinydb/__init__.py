import json
from pathlib import Path
from typing import Callable, Iterable, List, Optional


class MemoryStorage:
    """Minimal stand-in for TinyDB's in-memory storage."""
    pass


class Field:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return lambda doc: doc.get(self.name) == other


class Query:
    def __getattr__(self, item: str):
        return Field(item)


class TinyDB:
    def __init__(self, path: Optional[str] = None, storage=None):
        self._path = Path(path) if path else None
        self._storage = storage
        self._data: List[dict] = []
        if storage is None:
            if not self._path:
                raise ValueError("File path required when no storage is provided")
            if self._path.exists():
                try:
                    self._data = json.loads(self._path.read_text())
                except json.JSONDecodeError:
                    self._data = []
        else:
            # When using MemoryStorage we keep everything in-memory
            self._path = None

    def insert(self, document: dict):
        self._data.append(dict(document))
        self._persist()

    def all(self) -> List[dict]:
        return list(self._data)

    def update(self, fields: dict, cond: Callable[[dict], bool]):
        for item in self._data:
            if cond(item):
                item.update(fields)
        self._persist()

    def remove(self, cond: Callable[[dict], bool]):
        self._data = [item for item in self._data if not cond(item)]
        self._persist()

    def search(self, cond: Callable[[dict], bool]) -> List[dict]:
        return [item for item in self._data if cond(item)]

    def close(self):
        self._persist()

    def _persist(self):
        if self._path:
            self._path.write_text(json.dumps(self._data, indent=2))


__all__ = ["TinyDB", "Query", "MemoryStorage"]
