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
        if context.dt_during(dt):
            return TriggerReason()
        return False

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


def on_event(*jobs, kind):
    job_set = set(job.name for job in jobs)
    print(job_set, kind)

    def decorator(context: Context):
        for event in context.events:
            print(event.target, event.type)
            if event.target in job_set and event.type == kind:
                return TriggerReason(event.target)
        return False

    return decorator
