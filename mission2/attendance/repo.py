from typing import Dict, Iterable
from .models import Player


class InMemoryRepository:
    def __init__(self) -> None:
        self._by_name: Dict[str, Player] = {}
        self._next_id = 0

    def get_or_create(self, name: str) -> Player:
        if name not in self._by_name:
            self._next_id += 1
            self._by_name[name] = Player(id=self._next_id, name=name)
        return self._by_name[name]

    def all(self) -> Iterable[Player]:
        return list(self._by_name.values())
