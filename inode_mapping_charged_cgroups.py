from kernel_ffi import kmalloc, p64, str as s
from struct_access import sizeof, partial_struct


# this snippet shows the cgroups that are charged with each page of an inode's mapping.
# the memory charge per page is arbitrary ("first touch approach") and this utility is helpful
# in determining which cgroups are actually charged.
# if you try it on containerized environments, note that this doesn't read through overlayfs inodes, so
# you have to give it the real inode (e.g a file from /var/lib/docker/overlay2/l and not a file from
# /proc/pid/root or from the /merged/ dir of a container).

# this, as the rest of the scripts here, is the results of 1-2 hours of work, so don't trust it too much...
# the results appear on par with the numbers mincore/vmtouch report (amount of mapped pages)


def inode_from_path(path):
    path_p = kmalloc(sizeof("path"))
    assert path_p != 0
    assert 0 == kern_path(
        path,
        0x1,  # LOOKUP_FOLLOW
        path_p,
    )

    path = partial_struct("path")

    p = path(path_p)
    i = p.dentry.d_inode

    path_put(path_p)
    kfree(path_p)

    return i


def iter_inode_pages(i):
    PAGE_SHIFT = 12
    PATH_MAX = 4096

    assert i.i_mapping.____ptr != 0
    buf = kmalloc(PATH_MAX)
    total_pages = ((i.i_size - 1) >> PAGE_SHIFT) + 1
    total_mapped = 0

    for idx in range(0, total_pages):
        p = xa_load(i.i_mapping.i_pages, idx)

        if p == 0:
            status = "not mapped"
        else:
            total_mapped += 1
            p = partial_struct("page")(p)
            try:
                ret = cgroup_path_ns(
                    p.mem_cgroup.css.cgroup, buf, PATH_MAX, init_cgroup_ns
                )
            except ValueError as e:
                status = "ValueError: {}".format(e)
            finally:
                if ret < 0:
                    status = "cgroup_path_ns() ret: {}".format(ret)
                else:
                    status = "cgroup {}".format(s(buf))

        print("page {:02} {}".format(idx, status))

    print("mapped pages: {}/{}".format(total_mapped, total_pages))
    kfree(buf)
