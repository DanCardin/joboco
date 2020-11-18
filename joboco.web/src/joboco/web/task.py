from datetime import datetime, timedelta

from joboco.lib import completed, dt_condition, flow, Job, on_event, once

# t1
#   \
#    g --- t3
#   /
# t2
with flow() as f:
    with f.gate(dt_condition(datetime.now() + timedelta(seconds=10))) as g:
        t1 = g.job("task1", image="task1")

    with f.gate(once()) as g:
        t2 = g.job("task2", image="task2")

    with f.gate(completed(t1), completed(t2)) as g:
        t3 = g.job("task3", image="task3")
        t3.trigger(t1, t2)


with flow() as f:
    with f.gate(dt_condition(datetime.now() + timedelta(seconds=10))) as g:
        t1 = g.job("task1", image="task1")

    with f.gate(once()) as g:
        t2 = g.job("task2", image="task2")

    with f.gate(completed(t1), completed(t2)) as g:
        t3 = g.job("task3", image="task3")
        t3.trigger(t1, t2)
