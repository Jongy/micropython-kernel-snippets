# a small patch to remove the BPF_MAXINSNS check (for kernels where it was 4096)

bpf_prog_load


from kernel_ffi import bytes as b

x = b(bpf_prog_load, 0x500)

# objdump -D -Mintel,x86_64 -m i386 -b binary
#  128: 81 fa ff 0f 00 00       cmp    edx,0xfff
x.index(b"\x81\xfa\xff\x0f\x00\x00")

hex(p64(int(bpf_prog_load) + 296 + 2))
# 0x2fa870f00000fff

# changed to 0x10000
p64(int(bpf_prog_load) + 296 + 2, 0x2fa870f00010000)


# try loading now...
