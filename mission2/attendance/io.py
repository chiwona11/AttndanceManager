
from typing import Iterable, Tuple

def parse_lines(lines: Iterable[str]) -> Iterable[Tuple[str, str]]:
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            yield parts[0], parts[1]

def load_from_file(path: str) -> Iterable[Tuple[str, str]]:
    with open(path, encoding="utf-8") as f:
        yield from parse_lines(f)
