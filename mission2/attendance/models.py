
from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:
    id: int
    name: str
    points: int = 0
    grade: int = 0  # 0=NORMAL, 1=GOLD, 2=SILVER
    weekday_counts: List[int] = field(default_factory=lambda: [0]*7)
    wednesday_count: int = 0
    weekend_count: int = 0

GRADE_DESC = {0: "NORMAL", 1: "GOLD", 2: "SILVER"}
