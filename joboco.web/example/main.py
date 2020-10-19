import os

import requests

gate1 = os.environ["JOBOCO_GATE_NAME1"]
gate2 = os.environ["JOBOCO_GATE_NAME2"]
trigger = os.environ["JOBOCO_GATE_TRIGGER"]
print("starting", gate1, gate2, trigger)

job_name = os.environ["JOBOCO_JOB_NAME"]
upstream = os.environ["JOBOCO_UPSTREAM_JOB"]

if upstream == gate1 or upstream == gate2:
    print(upstream)
    requests.post(f"http://host.docker.internal:5555/{job_name}/state", data=upstream)

response = requests.get(f"http://host.docker.internal:5555/{job_name}/state")
state = response.json()
print("state", state)

if len(state) == 2:
    requests.post(
        "http://host.docker.internal:5555/emit", json={"target": job_name, "type": "gate"}
    )
