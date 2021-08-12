# kallsyms
no_such_symbol
printk

printk("buf: %*pE\n", 5, "aaa\x15a")
printk("IPv4: %pI4\n", "\x7f\x00\x00\x01")

from kernel_ffi import kmalloc
x = kmalloc(8)
memcpy(x, "\xc0\xa8\x01\x01", 4)
printk("IPv4: %pI4\n", x)

printk("IPv4: %pi4\n", "\x7f\x00\x00\x01")
