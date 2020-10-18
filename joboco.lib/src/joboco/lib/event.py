from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Event:
    target: Any
    type: str
    result: Any = None
