
from typing import Iterable, List, Tuple
from .repo import InMemoryRepository
from .models import GRADE_DESC, Player
from .points import WeekdayPointStrategy, DefaultWeekdayPointStrategy
from .bonus import BonusPolicy, WednesdayBonusPolicy, WeekendBonusPolicy
from .grade import GradePolicy, ThresholdGradePolicy

class AttendanceService:
    def __init__(
        self,
        repo: InMemoryRepository | None = None,
        weekday_strategy: WeekdayPointStrategy | None = None,
        bonus_policies: Iterable[BonusPolicy] | None = None,
        grade_policy: GradePolicy | None = None,
    ) -> None:
        self.repo = repo or InMemoryRepository()
        self.weekday_strategy = weekday_strategy or DefaultWeekdayPointStrategy()
        self.bonus_policies = list(bonus_policies) if bonus_policies is not None else [WednesdayBonusPolicy(), WeekendBonusPolicy()]
        self.grade_policy = grade_policy or ThresholdGradePolicy()

    def record_attendance(self, name: str, weekday: str) -> None:
        p = self.repo.get_or_create(name)
        add, idx, _, _ = self.weekday_strategy.calc_daily_point(weekday)
        p.weekday_counts[idx] += 1
        p.points += add

    def finalize(self) -> None:
        for p in self.repo.all():
            for policy in self.bonus_policies:
                p.points += policy.apply(p)
            p.grade = self.grade_policy.assign(p)

    def results(self) -> List[Tuple[str,int,str]]:
        return [(p.name, p.points, GRADE_DESC[p.grade]) for p in self.repo.all()]
