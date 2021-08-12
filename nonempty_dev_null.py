file_operations = partial_struct("file_operations")
null_fops = file_operations(null_fops)
from kernel_ffi import callback

def my_read_null(file, buf, count, ppos):
    pos = p64(ppos)
    b = "who said that /dev/null must be empty?\n"[pos:]
    l = min(len(b), count)
    memcpy(buf, b, l)
    p64(ppos, pos + l)
    return l

c = callback(my_read_null)
null_fops.read = c.ptr()
