from kernel_ffi import callback, current

task_struct = lookup_struct("task_struct")
file_operations = lookup_struct("file_operations")

real_urandom_read = urandom_read


def my_urandom_read(filp, buf, count, ppos):
    if task_struct(current()).comm.read() == "head":
        # lousy copy_to_user, should be improved if you use with untrusted programs
        src = b"abc" * (count // 3)
        memcpy(buf, src, len(src))
        return len(src)

    return real_urandom_read(filp, buf, count, ppos)


cb = callback(my_urandom_read)

file_operations(urandom_fops).read = cb.ptr()

# to stop
file_operations(urandom_fops).read = int(real_urandom_read)
