import time
from datetime import datetime, timedelta

from joboco.lib import completed, dt_condition, Gate, once, System, Task, Trigger


def task1():
    print("starting 1")
    time.sleep(2)
    print("done 1")


def task2():
    print("starting 2")
    time.sleep(2)
    print("done 2")


def task3():
    print("starting 3")
    time.sleep(2)
    print("done 3")


t1 = Task(task1)
t2 = Task(task2)
t3 = Task(task3)
g = Gate(t3, (t1, t2))

# t1
#   \
#    g --- t3
#   /
# t2

now = datetime.now()
system = System.from_triggers(
    Trigger(t1, on=dt_condition(now + timedelta(seconds=3))),
    Trigger(t2, on=once()),
    Trigger(g, on=completed(t1, t2)),
    Trigger(t3, on=completed(g)),
)
system.run()
