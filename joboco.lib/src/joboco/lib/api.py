import contextlib
from dataclasses import dataclass
from typing import Tuple

from joboco.job import Job
from joboco.trigger import List, Trigger


@dataclass
class TriggerFlow:
    def job(self):
        job = Job()
        return job


@dataclass
class Flow:
    triggers: List[Trigger]

    @contextlib.contextmanager
    def trigger(self, *triggers: Tuple[Trigger]) -> TriggerFlow:
        trigger_flow = TriggerFlow()
        yield trigger_flow

        import pdb

        pdb.set_trace()


@contextlib.contextmanager
def flow():
    yield Flow([])
