import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

from joboco.lib.container import ContainerManager
from joboco.lib.context import Context
from joboco.lib.trigger import Trigger


@dataclass
class Scheduler:
    triggers: Iterable[Trigger] = field(default_factory=list)
    last_loop_time: datetime = field(default_factory=datetime.now)
    executor: ContainerManager = field(default_factory=ContainerManager.from_env)

    @classmethod
    def from_triggers(cls, *triggers):
        return cls(triggers, last_loop_time=datetime.now())

    def run(self):
        while True:
            self.evaluate()
            time.sleep(0.2)

    def evaluate(self, events):
        events.extend(self.executor.collect_events())

        print("events", events)
        context = self.collect_context(events)
        print("context", context)
        self.last_loop_time = context.time

        jobs_to_trigger = []
        for trigger in self.triggers:
            result = trigger(context)
            if result:
                reason, job = result
                jobs_to_trigger.append((reason, job))

        print("jobs", jobs_to_trigger)
        self.schedule_jobs(*jobs_to_trigger)

    def collect_context(self, events):
        # events = self.check_completion()
        now = datetime.now()
        return Context(time=now, time_delta=now - self.last_loop_time, events=events)

    def schedule_jobs(self, *jobs):
        for reason, job in jobs:
            job_id = str(uuid.uuid4())
            self.executor.submit(job_id, job, reason)

    # def check_completion(self):
    #     events = []
    #     for container in self.excutor.containers.values():
    #         for event in container.new_events():
    #             events.append(event)
    #     return events

    def __del__(self):
        self.executor.shutdown()
