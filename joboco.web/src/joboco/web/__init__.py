from collections import defaultdict
from typing import Dict

from fastapi import FastAPI, Request
from joboco.lib import Scheduler
from joboco.lib.event import Event
from joboco.lib.job import JobLocalState
from joboco.lib.registry import JobRegistry
from pydantic import BaseModel

from joboco.web.task import jobs, triggers

app = FastAPI()


jls_collection: Dict = defaultdict(JobLocalState)

job_registry = JobRegistry.from_jobs(jobs, triggers)
scheduler = Scheduler()
events = []


@app.get("/{job_id}/state")
def get_state(job_id):
    jls = jls_collection[job_id]
    return jls.state


@app.post("/{job_name}/state")
async def set_state(job_name, request: Request):
    key = (await request.body()).decode("utf-8")
    print(key)
    jls = jls_collection[job_name]
    jls.set(key, True)
    return jls.state


class Emit(BaseModel):
    target: str
    type: str


@app.post("/emit")
def emit_event(emit: Emit):
    event = Event(emit.target, type=emit.type)
    events.append(event)


@app.get("/tick")
def tick():
    scheduler.evaluate(job_registry, events)
    events.clear()
