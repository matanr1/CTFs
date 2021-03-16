
# Hatter

![](images/hatter.png)

Lets check file type:
```console
matan@matan:~/Documents/hacking/matrix2021$ file hatter 
\hatter: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a2c77f2dd3e98846ff36c37cf10ae21374cb928a, for GNU/Linux 3.2.0, stripped

```

It's executable file so lets run it:
```console
matan@matan:~/Documents/hacking/matrix2021$ ./hatter 
find_thE_hAttEr

```

open the file in ghidra an take a look on main function:
```c

undefined8 main(int param_1,undefined8 param_2)

{
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  undefined8 local_18;
  int local_10;
  undefined4 local_c;
  
  local_c = 0;
  local_38 = 0x20206010701;
  local_30 = 0x405000206000104;
  local_28 = 0x600050000020104;
  local_20 = 0xffff050104050600;
  local_18 = param_2;
  local_10 = param_1;
  FUN_00401350();
  if (DAT_004050c1 == '\x01') {
    FUN_00401440();
  }
  if (DAT_004050c2 == '\x01') {
    FUN_00401760();
  }
  else {
    if (DAT_004050c3 == '\x01') {
      FUN_00401940();
    }
    else {
      if (local_10 == 1) {
        FUN_00401260((long)&local_38);
      }
      else {
        FUN_00401320();
      }
    }
  }
  return 0;
}
```

in the beginning we call  FUN_00401350 lets reverse it.

FUN_00401350() - this function update state of environment variables , lets rename this function and some vars:
```c
void update_env_vars_state(void)
{
  char *pcVar1;
  
  pcVar1 = getenv("DEBUG");
  DEBUG = pcVar1 != (char *)0x0;
  pcVar1 = getenv("WHERE_IS_THE_HATTER");
  WHERE_IS_THE_HATTER = pcVar1 != (char *)0x0;
  pcVar1 = getenv("SHOW_PASSWORD");
  SHOW_PASSWORD = pcVar1 != (char *)0x0;
  pcVar1 = getenv("DUMP_DEBUG_DATA");
  DUMP_DEBUG_DATA = pcVar1 != (char *)0x0;
  return;
}

//main after rename global vars
update_env_vars_state();
  if (SHOW_PASSWORD == '\x01') {
    FUN_00401440();
  }
  if (WHERE_IS_THE_HATTER == '\x01') {
    FUN_00401760();
  }
  else {
    if (DUMP_DEBUG_DATA == '\x01') {
      FUN_00401940();
    }
    else {
      if (local_10 == 1) {
        FUN_00401260((long)&local_38);
      }
      else {
        FUN_00401320();
      }
    }
  }
```
it seems that when we export  each one of the env vars we can manipulate  what will be execute.
let reverse the first part
```console
if (SHOW_PASSWORD == '\x01') {
    FUN_00401440();
  }
```
rename FUN_00401440 ->show_password_func , this function invoked only in the block above.
lets do some dynamic analyze
```console
matan@matan:~/Documents/hacking/matrix2021$ export SHOW_PASSWORD=1
matan@matan:~/Documents/hacking/matrix2021$ ./hatter
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
...
find_thE_hAttEr

matan@matan:~/Documents/hacking/matrix2021$ export DEBUG=1
matan@matan:~/Documents/hacking/matrix2021$ ./hatter
Enter "P_tr01l"
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
...
Enter "pRnTE"
find_thE_hAttEr
...
```
after playing with the environment vars
i got this sentences:
1. Enter "P_tr01l"
2. Enter "hinT"
3. Enter "pRnTE"
4. in ordEr to find thE hAttEr YoU hAvE to find ALL thE 6 LinE5 
5. Enter "do v3rifY"
6. The hatter left no traces
#### number 4 looks suspicious maybe we need to print the buffer and see what we got.

Inside we can see that print some pic and than call to this function:
```c
FUN_004014a0(4);
```
lets reverse it, we check if DEBUG exist and call another function `FUN_004014d0(4)`,lets reverse this function.
```c
void FUN_004014d0(uint param_1)
{
  char cVar1;
  undefined8 *puVar2;
  undefined8 local_18;
  uint local_c;
  local_c = param_1;
  memset(&local_18,0,0xc);
  puVar2 = (undefined8 *)get_pt_chnk_by_index(local_c); // get pointer to bugger by specific index
  if ((puVar2 != (undefined8 *)0x0) && (cVar1 = decrypt_16_bytes(puVar2,&local_18), cVar1 != '\0'))//decrypt the buffer
  {
    printf("Enter \"%s\"\n",&local_18);
  }
  return;
}
```

This function print buffer by getting index and decrypt the values
lets see analyze the decryption 
```c
undefined decrypt_16_bytes(undefined8 *param_1,undefined8 *param_2)

{
  byte bVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined local_19;
  
  local_19 = 0;
  uVar2 = *param_1;
  uVar3 = param_1[1];
  bVar1 = *(byte *)((long)param_1 + 0xb);
  decrypt_bytes((long)param_1 + 0xc,4,bVar1);
  if ((((*(char *)((long)param_1 + 0xc) == -0x22) && (*(char *)((long)param_1 + 0xd) == -0x53)) &&
      (*(char *)((long)param_1 + 0xe) == -0x42)) && (*(char *)((long)param_1 + 0xf) == -0x11)) {
    decrypt_bytes((long)param_1,0xb,bVar1);
    local_19 = 1;
    *param_2 = *param_1;
    *(undefined2 *)(param_2 + 1) = *(undefined2 *)(param_1 + 1);
    *(undefined *)((long)param_2 + 10) = *(undefined *)((long)param_1 + 10);
    *param_1 = uVar2;
    param_1[1] = uVar3;
  }
  return local_19;
}
```
seem that it first decrypt the last 4 bytes C-F:
`decrypt_bytes((long)param_1 + 0xc,4,bVar1);`
0-B bytes:
`decrypt_bytes((long)param_1,0xb,bVar1);`

lets analyze decrypt_bytes:
```c
byte decrypt_bytes(long param_1,ulong param_2,byte param_3)

{
  ulong local_28;
  byte local_19;
  
  local_28 = 0;
  local_19 = param_3;
  while (local_28 < param_2) {
    *(byte *)(param_1 + local_28) = *(byte *)(param_1 + local_28) ^ local_19;
    local_19 = *(byte *)(param_1 + local_28);
    local_28 = local_28 + 1;
  }
  return local_19;
}
```
we can see that:
param_1 - address of buffer
param_2 - number of actions
param_3 - index

decrypt flow
```
buffer[0] = buffer[0] ^ buffer[-1]
buffer[1] = buffer[1] ^ buffer[0]
... as it goes as number of param_2
```
so now we know how to decrypt the buffer let simulate it:
1.dump the buffer from `&DAT_0040506b`
```c
undefined * get_pt_chnk_by_index(uint param_1)
{
...
    if (param_1 == (byte)(&DAT_0040506b)[local_20 * 0x10]) break; //&DAT_0040506b pointer to buffer
    local_20 = local_20 + 1;
  }
  return &DAT_00405060 + local_20 * 0x10;
}
```
2. build script in python to simulate the the decryption
```python
messgae_size=16
with open('buffer','rb') as f:
    for _ in range(6):
        data = bytearray(f.read(messgae_size))
        #decrypt first 12 
        data[0] ^= data[11]
        for i in range(10):
            data[i+1] ^= data[i]
        #decrypt last 4 bytes
        for i in range(11,15):
            data[i+1] ^= data[i]
        print(data)
```
first result:
```console
dMp|dAtA\x00()\x00\xde\xad\xbe\xef
do v3rifY\x00U\x01\xde\xad\xbe\xef
hinT\x00^26789\x02\xde\xad\xbe\xef
iD4Ur5ALF\x00/\x03\xde\xad\xbe\xef
P_tr01l\x00BC.\x04\xde\xad\xbe\xef
pRnTE\x00x_-W\\\x05\xde\xad\xbe\xef
```

we can see that every sentence has more data because \x00 stop the `printf` to print the rest of the data.
Every sentence can be split to 3 parts for example:
1. do v3rifY\x00
2. U\x01
3. \xde\xad\xbe\xef

what we should do with this information,for now anything. lets continue searching.
we see that when we export `WHERE_IS_THE_HATTER` we call to function FUN_00401760,beside print the line above  this function do some more things like copy data to buffers and run FUN_00401260((long)local_238):
```c
  memcpy(local_1b8,&DAT_00403210,0x28);
  memcpy(local_1b0,&DAT_00403240,0x38);
  memcpy(local_1a8,&DAT_00403280,0x40);
  memcpy(local_1a0,&DAT_004032c0,0x40);
  memcpy(local_198,&DAT_00403300,0x40);
  memcpy(local_190,&DAT_00403340,0x40);
  memcpy(local_238,&DAT_00403380,0x7a);
  memset(local_13,0xb,0xb);
  print_message_by_index(2);
  FUN_00401260((long)local_238); //-> break here and update the the parameter
  ```
as part of dynamic analysis we break on ` FUN_00401260((long)local_238);` and change the RDI register
```asm
        0040191d 48 8d bd        LEA        RDI=>local_238,[RBP + -0x230]
                 d0 fd ff ff
        00401924 e8 37 f9        CALL       FUN_00401260                                     undefined FUN_00401260(long para
                 ff ff
```
each time i change RDI to local_190,local_198 ,etc... every time it printed other sentence
Second result:
```console
.08....9... 00 ^__^
....5...C.. 01 (xx)\_______
...4....... 02 (__)\       )\/\
..6....2... 03  U  ||--WWW |   
.7...B...1. 04     ||     ||  
.A.....3... 05

Now that we have all the outputs lets assmeble it with the last result.
we need to take part 1and 2 of the first result and map it to the current result
```console
.08....9... 00 ^__^
dMp|dAtA0()
....5...C.. 01 (xx)\_______
do v3rifY0U
...4....... 02 (__)\       )\/\
hinT0^26789
..6....2... 03  U  ||--WWW |   
iD4Ur5ALF0/\
.7...B...1. 04     ||     ||  
P_tr01l0BC.
.A.....3... 05
pRnTE0x_-W\\
```
look like we assemble a mapping of the flag:
1. the numbers in the second result are indexes in the flag
2. the first result's len fit in to the second result

lets map the letters to the indexes and there is the flag:-)
 index  - 0123456789ABC
value   - MCL_T34_pAR1Y

  

