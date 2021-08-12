# prints the thread's fsbase in /proc/pid/status.

from kernel_ffi import ftrace

task_struct = partial_struct("task_struct")


def my_status(orig, m, ns, pid, task):
    ret = orig(m, ns, pid, task)
    fs = task_struct(task).thread.fsbase
    seq_printf(m, "fs: %px\n", fs)
    return ret


f = ftrace("proc_pid_status", my_status)
