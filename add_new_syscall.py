# array of pointers to syscalls
sys_call_table

for i in range(1000):
    print(i, p64(int(sys_call_table) + 8 * i))

# let's add names...

sprint_symbol

from kernel_ffi import kmalloc, str as s

buf = kmalloc(1000)

for i in range(1000):
    addr = p64(int(sys_call_table) + 8 * i)

    l = sprint_symbol(buf, addr)
    print(i, hex(addr), s(buf))

# see anything repeating?

def mysys(a, b, c):
    printk("I got: %lx %lx %lx\n", a, b, c)
    print("I got:", a, b, c)
    return 42


from kernel_ffi import callback

p = callback(mysys)

p64(int(sys_call_table) + 8 * 333, p.ptr())

# in usermode:

import ctypes
libc = ctypes.CDLL("libc.so.6")
libc.syscall(345)

libc.syscall(333, 0x1, 0x2, 0x3)
