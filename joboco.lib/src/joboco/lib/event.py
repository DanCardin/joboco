import enum
from dataclasses import dataclass
from typing import Any


@enum.unique
class EventTypes(enum.Enum):
    job_start = "job_start"
    job_complete = "job_complete"


@dataclass(frozen=True)
class Event:
    type: EventTypes
    target: Any
    result: Any = None
