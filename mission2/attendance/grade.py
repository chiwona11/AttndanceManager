from abc import ABC, abstractmethod
from .models import Player


class GradePolicy(ABC):
    @abstractmethod
    def assign(self, player: Player) -> int: ...


class ThresholdGradePolicy(GradePolicy):
    def __init__(self, gold: int = 50, silver: int = 30):
        self.gold = gold;
        self.silver = silver

    def assign(self, player: Player) -> int:
        if player.points >= self.gold: return 1
        if player.points >= self.silver: return 2
        return 0
