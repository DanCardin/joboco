import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, List

from joboco.lib.container import ContainerManager
from joboco.lib.context import Context
from joboco.lib.event import Event
from joboco.lib.registry import JobRegistry
from joboco.lib.trigger import Trigger


@dataclass
class Scheduler:
    last_loop_time: datetime = field(default_factory=datetime.now)
    executor: ContainerManager = field(default_factory=ContainerManager.from_env)

    def run(self):
        while True:
            self.evaluate()
            time.sleep(0.2)

    def evaluate(self, job_registry: JobRegistry, new_events: List[Event]):
        events = [
            *new_events,
            *self.executor.collect_events(),
        ]

        context = self.collect_context(events)
        self.last_loop_time = context.time

        jobs_to_trigger = job_registry.evaluate_events(context)
        self.schedule_jobs(*jobs_to_trigger)

    def collect_context(self, events):
        now = datetime.now()
        return Context(time=now, time_delta=now - self.last_loop_time, events=events)

    def schedule_jobs(self, *jobs):
        for job, cause in jobs:
            job_id = str(uuid.uuid4())
            self.executor.submit(job_id, job, cause)

    def __del__(self):
        self.executor.shutdown()
