from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from joboco.lib.event import Event


@dataclass(frozen=True)
class Context:
    time: datetime
    time_delta: timedelta
    events: List[Event]

    @property
    def prev_time(self):
        return self.time - self.time_delta

    def dt_during(self, dt):
        return self.prev_time <= dt < self.time
