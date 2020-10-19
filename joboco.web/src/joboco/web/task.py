from datetime import datetime, timedelta

from joboco.lib import dt_condition, Gate, Job, on_event, once, Trigger

t1 = Job("task1", image="task1")
t2 = Job("task2", image="task2")

t3 = Job("task3", image="task3")
g = Gate("gate-t3", t3, (t1, t2))

# t1
#   \
#    g --- t3
#   /
# t2

now = datetime.now()
triggers = [
    Trigger(t1, on=dt_condition(now + timedelta(seconds=3))),
    Trigger(t2, on=once()),
    Trigger(g, on=on_event(t1, t2, kind="completed")),
    Trigger(t3, on=on_event(g, kind="gate")),
]
