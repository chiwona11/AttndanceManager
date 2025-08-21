
from typing import List, Tuple
from .repo import InMemoryRepository
from .models import GRADE_DESC
from .points import WeekdayPointStrategy, DefaultWeekdayPointStrategy


class AttendanceService:
    def __init__(self, repo: InMemoryRepository | None = None, weekday_strategy: WeekdayPointStrategy | None = None) -> None:
        self.repo = repo or InMemoryRepository()
        self.weekday_strategy = weekday_strategy or DefaultWeekdayPointStrategy()

    def record_attendance(self, name: str, weekday: str) -> None:
        p = self.repo.get_or_create(name)
        add, idx, _, _ = self.weekday_strategy.calc_daily_point(weekday)
        p.weekday_counts[idx] += 1
        p.points += add

    def finalize(self) -> None:
        for p in self.repo.all():
            p.grade = 1 if p.points >= 50 else (2 if p.points >= 30 else 0)

    def results(self) -> List[Tuple[str,int,str]]:
        return [(p.name, p.points, GRADE_DESC[p.grade]) for p in self.repo.all()]
