from typing import Iterable, List, Tuple, Callable
from .repo import InMemoryRepository
from .models import GRADE_DESC, Player
from .points import WeekdayPointStrategy, DefaultWeekdayPointStrategy
from .bonus import BonusPolicy, WednesdayBonusPolicy, WeekendBonusPolicy
from .grade import GradePolicy, ThresholdGradePolicy


class RemovalPolicy:
    def __call__(self, p: Player) -> bool:
        return (p.grade == 0) and (p.weekday_counts[2] == 0) and ((p.weekday_counts[5] + p.weekday_counts[6]) == 0)


class AttendanceService:
    def __init__(
            self,
            repo: InMemoryRepository | None = None,
            weekday_strategy: WeekdayPointStrategy | None = None,
            bonus_policies: Iterable[BonusPolicy] | None = None,
            grade_policy: GradePolicy | None = None,
            removal_policy: Callable[[Player], bool] | None = None,
    ) -> None:
        self.repo = repo or InMemoryRepository()
        self.weekday_strategy = weekday_strategy or DefaultWeekdayPointStrategy()
        self.bonus_policies = list(bonus_policies) if bonus_policies is not None else [WednesdayBonusPolicy(),
                                                                                       WeekendBonusPolicy()]
        self.grade_policy = grade_policy or ThresholdGradePolicy()
        self.removal_policy = removal_policy or RemovalPolicy()

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

    def results(self) -> List[Tuple[str, int, str]]:
        return [(p.name, p.points, GRADE_DESC[p.grade]) for p in self.repo.all()]

    def removed_players(self) -> List[str]:
        return [p.name for p in self.repo.all() if self.removal_policy(p)]
