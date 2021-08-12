from kernel_ffi import bytes as b
from kernel_ffi import str as s

s(init_task)
s(linux_proc_banner)

b(init_task, 100)
