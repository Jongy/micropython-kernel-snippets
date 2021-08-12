task_struct = lookup_struct("task_struct")

from kernel_ffi import current
from struct_access import container_of


def ps(grep=None):
    p = task_struct(current())
    p1 = p
    while True:
        if grep is None or grep in p.comm.read():
            print("pid {} comm {!r}".format(p.pid, p.comm.read()))
        p = container_of(p.tasks.next, "task_struct", "tasks")
        if p == p1:
            break


def pgrep_pid(pid):
    p = task_struct(current())
    p1 = p
    while True:
        if p.pid == pid:
            return p

        p = container_of(p.tasks.next, "task_struct", "tasks")
        if p == p1:
            break


def pgrep(s):
    p = task_struct(current())
    p1 = p
    while True:
        if p.comm.read() == s:
            return p

        p = container_of(p.tasks.next, "task_struct", "tasks")
        if p == p1:
            break
