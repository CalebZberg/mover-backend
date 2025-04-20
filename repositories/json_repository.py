# repositories/json_repository.py

import json
from pathlib import Path
from typing import Any, List, Type, TypeVar

T = TypeVar('T')

class JSONRepository:
    """
    A simple repository that persists items to a JSON file.
    Expects Pydantic models (or anything with .dict()).
    """
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        # ensure the directory exists
        self.filepath.parent.mkdir(exist_ok=True, parents=True)

    def _read_all(self) -> List[Any]:
        if not self.filepath.exists():
            return []
        text = self.filepath.read_text()
        return json.loads(text) if text else []

    def _write_all(self, items: List[Any]):
        self.filepath.write_text(json.dumps(items, indent=2))

    def list(self, model: Type[T]) -> List[T]:
        raw = self._read_all()
        return [model(**item) for item in raw]

    def add(self, item: Any) -> None:
        """
        Appends item.dict() to the JSON file.
        """
        data = self._read_all()
        data.append(item.dict())
        self._write_all(data)
