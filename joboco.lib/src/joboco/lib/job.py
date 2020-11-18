from __future__ import annotations

import functools
import inspect
import textwrap
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Protocol


class AbstractJob(Protocol):
    name: str

    def build(self) -> ContainerJob:
        """Produce a `ContainerJob` instance.
        """


@dataclass(frozen=True)
class ContainerJob:
    name: str
    image: str
    environment: Dict[str, str] = field(default_factory=dict)

    def build(self):
        return self


@dataclass(frozen=True)
class PythonJob:
    """Build an image dynamically from a given python callable.
    """

    name: str
    fn: Callable
    requirements: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.source_code:
            raise ValueError(f"Cannot invoke {self.fn.__name__} as a python job")

    @functools.cached_property
    def source_code(self):
        try:
            lines = inspect.getsource(self.fn)
        except OSError:
            return None
        return textwrap.dedent(lines)

    def build(self):
        image = ...
        return ContainerJob(image)


Job = ContainerJob


@dataclass
class JobLocalState:
    state: Dict = field(default_factory=dict)

    def set(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)


def Gate(name, target, tasks):
    # This environment thing isn't the right mechanism
    return Job(
        name,
        image="gate",
        environment={
            "JOBOCO_GATE_NAME1": tasks[0].name,
            "JOBOCO_GATE_NAME2": tasks[1].name,
            "JOBOCO_GATE_TRIGGER": target.name,
        },
    )
