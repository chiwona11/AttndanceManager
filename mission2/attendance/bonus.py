from abc import ABC, abstractmethod
from .models import Player


class BonusPolicy(ABC):
    @abstractmethod
    def apply(self, player: Player) -> int: ...


class WednesdayBonusPolicy(BonusPolicy):
    def __init__(self, threshold: int = 10, bonus: int = 10):
        self.threshold = threshold;
        self.bonus = bonus

    def apply(self, player: Player) -> int:
        return self.bonus if player.weekday_counts[2] >= self.threshold else 0


class WeekendBonusPolicy(BonusPolicy):
    def __init__(self, threshold: int = 10, bonus: int = 10):
        self.threshold = threshold;
        self.bonus = bonus

    def apply(self, player: Player) -> int:
        wk = player.weekday_counts[5] + player.weekday_counts[6]
        return self.bonus if wk >= self.threshold else 0
