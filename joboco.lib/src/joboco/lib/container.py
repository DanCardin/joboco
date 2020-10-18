from dataclasses import dataclass
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
    containers: Dict[str, ContainerState]

    @classmethod
    def from_env(cls):
        client = docker.from_env()
        return cls(client)

    def submit(self, job_id, job: ContainerJob, reason):
        container = self.client.containers.run(
            job.image,
            environment={
                "JOBOCO_UPSTREAM_JOB": reason.job,
                "JOBOCO_JOB_ID": job_id,
                "JOBOCO_JOB_IMAGE": job.image,
            },
            detach=True,
        )
        return ContainerState(job_id, job.name, container)

    def cleanup(self):
        finished_job_ids = []
        for job_id, container in self.containers.items():
            if container.done():
                finished_job_ids.append(job_id)

        for job_id in finished_job_ids:
            self.containers.pop(job_id)

    def shutdown(self):
        for container_state in self.containers.values():
            self.container_state.kill()
