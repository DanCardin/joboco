from dataclasses import dataclass
from typing import Dict, List

from joboco.lib.context import Context
from joboco.lib.job import Job
from joboco.lib.trigger import Trigger


class DuplicateJobNames(ValueError):
    def __init__(self, registered_jobs: Dict[str, Job], conflicting_jobs: List[Job]):
        self.registered_jobs = registered_jobs
        self.conflicting_jobs = conflicting_jobs

        message_parts = [
            "Jobs were registered with conflicting names.",
        ]
        # TODO: Pretty print registered jobs/conflicts. Ideally with identifying info (like source?)

        message = "\n".join(message_parts)
        super().__init__(self, message)


@dataclass
class JobRegistry:
    jobs_by_name: Dict[str, Job]
    triggers: List[Trigger]

    @classmethod
    def from_parts(cls, jobs: List[Job], triggers: List[Trigger]):
        verify_job_uniqueness(jobs)

        jobs_by_name = {job.name: job for job in jobs}
        return cls(jobs_by_name, triggers)

    def evaluate_events(self, context: Context):
        jobs_to_trigger = []
        for trigger in self.triggers:
            result = trigger(context)
            if result:
                jobs_to_trigger.append(result)
        return jobs_to_trigger


def verify_job_uniqueness(jobs: List[Job]):
    registered_jobs = {}
    duplicate_jobs = []
    for job in jobs:
        if job.name in registered_jobs:
            duplicate_jobs.append(job)
        else:
            registered_jobs[job.name] = job

    if duplicate_jobs:
        duplicate_names = set(job.name for job in duplicate_jobs)
        registered_jobs = {
            name: job for name, job in registered_jobs.items() if name in duplicate_names
        }

        conflicting_jobs = {}
        for job in duplicate_jobs:
            job_list = conflicting_jobs.setdefault(job.name, [])
            job_list.append(job)

        raise DuplicateJobNames(registered_jobs, conflicting_jobs)
