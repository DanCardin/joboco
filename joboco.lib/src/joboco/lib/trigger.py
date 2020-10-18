from dataclasses import dataclass
from typing import Callable, Optional

from joboco.lib.context import Context
from joboco.lib.job import Job


@dataclass
class Trigger:
    target: Callable
    on: Callable

    def __call__(self, context: Context):
        result = self.on(context)
        if result:
            return (result, self.target)
        return None


@dataclass(frozen=True)
class TriggerReason:
    job: Optional[Job] = None


def dt_condition(dt):
    def decorator(context: Context):
        return context.dt_during(dt)

    return decorator


def once():
    executed = False

    def decorator(context: Context):
        nonlocal executed
        if not executed:
            executed = True
            return TriggerReason()
        return False

    return decorator


def completed(*jobs):
    job_set = set(id(t) for t in jobs)

    def decorator(context: Context):
        for event in context.events:
            if id(event.target) in job_set and event.type == "complete":
                return TriggerReason(event.target)
        return False

    return decorator
