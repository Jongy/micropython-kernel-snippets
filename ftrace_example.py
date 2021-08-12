from kernel_ffi import ftrace, str as s

filename = lookup_struct("filename")


def IS_ERR(n):
    return n > (1 << 64) - 4096


files = []


def do_filp_open_hook(orig, dfd, pathname, op):
    ret = orig(dfd, pathname, op)

    if not IS_ERR(ret):
        fn = s(int(filename(pathname).name))
        if fn == "/mysecret":
            files.append(ret)

    return ret


h1 = ftrace("do_filp_open", do_filp_open_hook)


def vfs_write_hook(orig, file, buf, count, pos):
    if file in files:
        memset(buf, ord('*'), count)
    return orig(file, buf, count, pos)


h2 = ftrace("vfs_write", vfs_write_hook)

# run "echo dsfgsdfgdsfgdf > /mysecret"
# print it: it's gonna be all ***

h1.rm()
h2.rm()
