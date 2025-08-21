
from typing import List, Tuple
from .repo import InMemoryRepository
from .models import GRADE_DESC

WEEKDAY_INDEX = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}

class AttendanceService:
    def __init__(self, repo: InMemoryRepository | None = None) -> None:
        self.repo = repo or InMemoryRepository()

    def record_attendance(self, name: str, weekday: str) -> None:
        p = self.repo.get_or_create(name)
        wd = weekday.lower()
        if wd not in WEEKDAY_INDEX:
            raise ValueError(f"Unknown weekday: {weekday}")
        idx = WEEKDAY_INDEX[wd]
        p.weekday_counts[idx] += 1
        if idx == 2:
            p.points += 3
        elif idx in (5,6):
            p.points += 2
        else:
            p.points += 1

    def finalize(self) -> None:
        for p in self.repo.all():
            p.grade = 1 if p.points >= 50 else (2 if p.points >= 30 else 0)

    def results(self) -> List[Tuple[str,int,str]]:
        return [(p.name, p.points, GRADE_DESC[p.grade]) for p in self.repo.all()]
