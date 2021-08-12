task_struct = lookup_struct("task_struct")

from kernel_ffi import current
p = task_struct(current())

# p.<TAB>

from struct_access import dump_struct
dump_struct(p)

print(p.comm.read())
p.comm = "very very very long comm"  # ValueError
p.comm = "short comm"  # no ValueError
print(p.comm.read())  # short comm
# ps -ef | grep short
