from dataclasses import dataclass
from typing import Callable, Optional

from joboco.lib.context import Context
from joboco.lib.event import EventTypes
from joboco.lib.job import Job


@dataclass
class Trigger:
    target: Job
    on: Callable

    def __call__(self, context: Context):
        result = self.on(context)
        if result:
            if not isinstance(result, Job):
                result = None
            return TriggerResult(self.target, result)
        return None


@dataclass(frozen=True)
class TriggerResult:
    target: Job = None
    job: Optional[Job] = None


def dt_condition(dt):
    def decorator(context: Context) -> bool:
        return context.dt_during(dt)

    return decorator


def once():
    executed = False

    def decorator(context: Context) -> Optional[bool]:
        nonlocal executed
        if not executed:
            executed = True
            return True

    return decorator


def on_event(*jobs, kind: EventTypes):
    job_set = set(job.name for job in jobs)

    def decorator(context: Context) -> Optional[Job]:
        for event in context.events:
            if event.target in job_set and event.type == kind:
                return event.target

    return decorator


def completed(*jobs):
    return on_event(*jobs, EventTypes.job_complete)
