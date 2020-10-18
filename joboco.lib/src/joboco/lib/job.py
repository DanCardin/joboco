from __future__ import annotations

import functools
import inspect
import textwrap
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Protocol, Tuple

from joboco.lib.event import Event


class AbstractJob(Protocol):
    name: str

    def build(self) -> ContainerJob:
        """Produce a `ContainerJob` instance.
        """


@dataclass(frozen=True)
class ContainerJob:
    name: str
    image: str
    environment: Dict[str, str]

    def build(self):
        return self

    def __call__(self, _):
        result = self.fn()
        return Event(target=self, type="complete", result=result)


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

    def __call__(self, _):
        result = self.fn()
        return Event(target=self, type="complete", result=result)


Job = ContainerJob


@dataclass
class JobLocalState:
    state: Dict = field(default_factory=dict)

    def set(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)


def gate():
    # TODO: Need interface for task-local state, without that, this will just be an or-gate
    if set(id(c) for c in completions) == set(id(c) for c in self.conditions):
        return Event(target=self, type="complete", result={})
    return None


def gate(name, *_jobs):
    def _gate():
        import ast
        import os
        import sys

        jobs = ast.literal_eval(f"{_jobs}")
        if os.environ.get("JOBOCO_UPSTREAM_JOB") in jobs:
            return
        sys.exit(1)

    return PythonJob(name, _gate)
