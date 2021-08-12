# see https://granulate.io/dynamic-ftrace-filtering/

from kernel_ffi import KP_ARGS_MODIFY, callback, current, ftrace, kprobe

# create struct casters
tcphdr = partial_struct("tcphdr")
sk_buff = partial_struct("sk_buff")
net_protocol_s = partial_struct("net_protocol")


def swap16(n):
    n = n & 0xffff
    return ((n & 0xff) << 8) + (n >> 8)


trace_task = None


def my_trace_ignore_this_task(orig, filtered_pids, task):
    """
    Returns true if @task should *NOT* be traced.
    Returns false if @task should be traced.
    """
    return 0 if task == trace_task else 1


# trace_ignore_this_task can't be ftraced itself (probably because it's a core function of
# ftrace?)
# but kprobe works :)
kp = kprobe("trace_ignore_this_task", KP_ARGS_MODIFY, my_trace_ignore_this_task)


def my_pre_tcp_v4_rcv(skb):
    global trace_task

    trace = False
    skb = sk_buff(skb)
    th = tcphdr(skb.head + skb.transport_header)
    # is it TCP dport 9000?
    if swap16(th.dest) == 9000:
        trace = True
        trace_task = current()
        ftrace_filter_pid_sched_switch_probe(global_trace, False, None, current())
        __trace_printk(0, "trace of tcp_v4_rcv starts...")

    ret = tcp_v4_rcv(int(skb))

    if trace:
        trace_task = 0
        ftrace_filter_pid_sched_switch_probe(global_trace, False, None, current())
        __trace_printk(0, "trace of tcp_v4_rcv is done.")

    return ret


cb = callback(my_pre_tcp_v4_rcv)
net_protocol_s(tcp_protocol).handler = cb.ptr()

net_protocol_s(tcp_protocol).handler = int(tcp_v4_rcv)

# to enable:

# mount -t tracefs none /sys/kernel/tracing
# cd /sys/kernel/tracing
# echo tcp_v4_rcv > set_graph_function
# echo function_graph > current_tracer

# echo 2 > set_ftrace_pid
