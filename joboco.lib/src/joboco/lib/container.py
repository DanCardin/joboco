from dataclasses import dataclass, field
from typing import Dict

import docker
from docker.models.containers import Container

from joboco.lib.event import Event
from joboco.lib.job import ContainerJob


@dataclass
class ContainerState:
    job_id: str
    job_name: str
    container: Container

    def logs(self):
        for line in self.container.logs(stream=True):
            yield line

    def done(self):
        self.container.reload()
        for line in self.logs():
            print(line)
        return self.container.status == "exited"

    def kill(self):
        self.container.kill()

    def new_events(self):
        # TODO: Actually make this do something
        if self.done():
            yield [Event(type="complete", target=self.job_name)]
        yield []


@dataclass
class ContainerManager:
    client: docker.client.DockerClient
    containers: Dict[str, ContainerState] = field(default_factory=dict)

    @classmethod
    def from_env(cls):
        client = docker.from_env()
        return cls(client)

    def submit(self, job_id, job: ContainerJob, reason):
        print("executing", job_id)
        container = self.client.containers.run(
            job.image,
            environment={
                "JOBOCO_UPSTREAM_JOB": reason.job,
                "JOBOCO_JOB_ID": job_id,
                "JOBOCO_JOB_NAME": job.name,
                "JOBOCO_JOB_IMAGE": job.image,
                **job.environment,
            },
            detach=True,
        )
        container_state = ContainerState(job_id, job.name, container)
        self.containers[job_id] = container_state
        return container_state

    def collect_events(self):
        finished_jobs = self.cleanup()
        print("finished_jobs", finished_jobs)
        return [Event(target=container.job_name, type="completed") for container in finished_jobs]

    def cleanup(self):
        finished_job_ids = []
        print("containers", len(self.containers))
        for job_id, container in self.containers.items():
            if container.done():
                finished_job_ids.append(job_id)

        finished_jobs = []
        for job_id in finished_job_ids:
            finished_jobs.append(self.containers.pop(job_id))

        return finished_jobs

    def shutdown(self):
        for container_state in self.containers.values():
            self.container_state.kill()
