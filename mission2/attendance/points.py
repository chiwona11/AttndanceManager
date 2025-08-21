from abc import ABC, abstractmethod
from typing import Tuple

WEEKDAY_INDEX = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}


class WeekdayPointStrategy(ABC):
    @abstractmethod
    def calc_daily_point(self, weekday: str) -> Tuple[int, int, bool, bool]:
        """return (add, idx, is_wed, is_weekend)"""
        ...


class DefaultWeekdayPointStrategy(WeekdayPointStrategy):
    def calc_daily_point(self, weekday: str) -> Tuple[int, int, bool, bool]:
        wd = weekday.lower()
        if wd not in WEEKDAY_INDEX:
            raise ValueError(f"Unknown weekday: {weekday}")
        idx = WEEKDAY_INDEX[wd]
        is_wed = idx == 2
        is_weekend = idx in (5, 6)
        add = 3 if is_wed else (2 if is_weekend else 1)
        return add, idx, is_wed, is_weekend
