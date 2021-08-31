# Beleaf - nigtmare



```console
matan@matan:~/Documents/hacking/nightmare/CSAW_2019_beleaf$ ./beleaf 
Enter the flag
>>> aaaaa
Incorrect!
```

lets reverse it with ghidra,rename important vars and func calls:
```c
undefined8 main_func(void)

{
  size_t buffer_len;
  long lVar1;
  long in_FS_OFFSET;
  ulong counter;
  char local_98 [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Enter the flag\n>>> ");
  __isoc99_scanf(&DAT_00100a78,local_98);
  buffer_len = strlen(local_98);
  if (buffer_len < 0x21) {
    puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  counter = 0;
  while (counter < buffer_len) {
    lVar1 = get_char_index(local_98[counter]);
    if (lVar1 != *(long *)(&INDEX_BUFFER + counter * 8)) {
      puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    counter = counter + 1;
  }
  puts("Correct!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

we can see that the function check if get_char_index returns value that compare to INDEX_BUFFER.
we need to check what is the function `get_char_index` ,lets reverse it:
```c
long get_char_index(char ch)

{
  long counter;
  
  counter = 0;
  while ((counter != -1 && ((int)ch != *(int *)(&PASSWORD_BUFFER + counter * 4)))) {
    if ((int)ch < *(int *)(&PASSWORD_BUFFER + counter * 4)) {
      counter = counter * 2 + 1;
    }
    else {
      if (*(int *)(&PASSWORD_BUFFER + counter * 4) < (int)ch) {
        counter = (counter + 1) * 2;
      }
    }
  }
  return counter;
}
```
the function search the char given from input and return the index if exist else return -1.
so we need to dump both of the buffer and build script that match INDEX_BUFFER to PASSWORD_BUFFER so it will reorder the flag.

Dump buffer example:
```
        003014e0 01              ??         01h
        003014e1 00              ??         00h
        003014e2 00              ??         00h
        003014e3 00              ??         00h
        003014e4 00              ??         00h
        003014e5 00              ??         00h
        003014e6 00              ??         00h
        003014e7 00              ??         00h
        003014e8 09              ??         09h
	.
	.
	.
```

Solution:
```python
counters_buffer=[]
with open("index_buffer",'r') as f:
    while True:
        data = f.readline()
        for _ in range(7):
            f.readline()
        if not data:
            break
        counters_buffer.append(int(data.split("??")[1].strip().split('h')[0],16))


pass_buffer = []
with open("pass_buffer",'r') as f:
    while True:
        data = f.readline()
        for _ in range(3):
            f.readline()
        if not data:
            break
        pass_buffer.append(int(data.split("??")[1].strip().split('h')[0],16))

flag=""
for i in range(len(counters_buffer)):
    flag+=chr(pass_buffer[counters_buffer[i]])

print(flag)
```

Result:`flag{we_beleaf_in_your_re_future}`



