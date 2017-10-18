---
title:  Scythe17 Optimize Me 350
updated: 2017-10-18 15:13:26
---


- [optimize-me scythe17 350](#orgeb128a2)


<a id="orgeb128a2"></a>

# optimize-me scythe17 350

> Death is knocking on your door. He will take your soul away unless you are able to quickly tell him the flag. But of course, he had employed f0xtr0t to slow down the speed at which you can see the flag. Can you tell him the flag quick enough and save yourself? Here's the [binary](http://hack.bckdr.in/OPTIMIZE-ME/optimize_me).

Let's get going

```sh
$ file optimize_me
optimize_me: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2,
for GNU/Linux 2.6.24, BuildID[sha1]=702db318aec446950b713581b5adb2995d2463d4, stripped
```

```sh
$ ./optimize_me
Welcome to f0xtr0t's extremely slow program
-------------------------------------------

In
```

The binary is taking long time to print characters waiting for it to finish is not an option , Let open it in radare2

```nasm
0x0804868c      c7442404308b.  mov dword [local_4h], str.Welcome_to_f0xtr0t_s_extremely_slow_program_n_____________________________________
0x08048694      c70424010000.  mov dword [esp], 1                                                                                          
0x0804869b      e8e0fcffff     call sym.imp.__printf_chk   ;[1]                                                                            
0x080486a0      c74424180000.  mov dword [count], 0                                                                                    
```

`sym.imp.__printf_chk` is used to print the string , After there is a loop with `0x4e52` number of iteration we can see that the print function is called with argument eax , this might be the place were the characters are printing

```nasm
|   0x0804879f      8b44242c       mov eax, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44                                                        
|   0x080487a3      c74424048c8b.  mov dword [local_4h], 0x8048b8c ; [0x8048b8c:4]=0x6325                                                      
|   0x080487ab      c70424010000.  mov dword [esp], 1                                                                                          
|   0x080487b2      2b44241c       sub eax, dword [local_1ch]                                                                                  
|   0x080487b6      31c8           xor eax, ecx                                                                                                
|   0x080487b8      31f0           xor eax, esi                                                                                                
|   0x080487ba      0fbec0         movsx eax, al                                                                                               
|   0x080487bd      89442408       mov dword [local_8h], eax                                                                                   
|   0x080487c1      e8bafbffff     call sym.imp.__printf_chk   ;[2]                                                                            
|   0x080487c6      8344241801     add dword [count], 1                                                                                        
|   0x080487cb      817c2418524e.  cmp dword [count], 0x4e52   ; [0x4e52:4]=-1                                                                 
`=< 0x080487d3      0f85cffeffff   jne 0x80486a8               ;[3]    
```

So we need to find why this binary is taking so much time to print one character and from were does this comes from , from debugging the binary by we can see that this is the loop which makes it this much slow

```nasm
[0x08048741]> pd 30 @ 0x8048741
!      ; JMP XREF from 0x0804872c (main)
|   0x08048741      8d1c09         lea ebx, [ecx + ecx]
|   0x08048744      89c8           mov eax, ecx
|   0x08048746      0fafc1         imul eax, ecx
|   0x08048749      29d0           sub eax, edx
|   0x0804874b      99             cdq
|   0x0804874c      f7fb           idiv ebx
|   0x0804874e      8b54242c       mov edx, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44
|   0x08048752      8b5c242c       mov ebx, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44
|   0x08048756      29c1           sub ecx, eax
|   0x08048758      89d0           mov eax, edx
|   0x0804875a      c1f81f         sar eax, 0x1f
|   0x0804875d      c1e81e         shr eax, 0x1e
|   0x08048760      01c2           add edx, eax
|   0x08048762      83e203         and edx, 3
|   0x08048765      29c2           sub edx, eax
|   0x08048767      89d8           mov eax, ebx
|   0x08048769      c1f81f         sar eax, 0x1f
|   0x0804876c      c1e81e         shr eax, 0x1e
|   0x0804876f      01c3           add ebx, eax
|   0x08048771      83e303         and ebx, 3
|   0x08048774      29c3           sub ebx, eax
|   0x08048776      8b0495008609.  mov eax, dword [edx*4 + 0x8098600] ; [0x8098600:4]=0
|   0x0804877d      2b049d40a004.  sub eax, dword [ebx*4 + 0x804a040]
|   0x08048784      31c1           xor ecx, eax
|   0x08048786      8b44242c       mov eax, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44
|   0x0804878a      83c001         add eax, 1
|   0x0804878d      8944242c       mov dword [local_2ch], eax
|   0x08048791      8b44242c       mov eax, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44
|   0x08048795      3944241c       cmp dword [local_1ch], eax  ; [0x13:4]=-1 ; 19
`=< 0x08048799      778d           ja 0x8048728
```

The loop is ran until `local_1ch` `local_2ch` are equal , and it turns out the `local_1ch` is huge number , now we have to know what is happening inside this loop , before that have i have to figure how the character is computer , it will give us some insight on the loop

```nasm
 |   0x0804879b      8b742414       mov esi, dword [local_14h]  ; [0x14:4]=-1 ; 20                                                              
 !      ; JMP XREF from 0x0804870d (main)                                                                                                       
 |   0x0804879f      8b44242c       mov eax, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44                                                        
 |   0x080487a3      c74424048c8b.  mov dword [local_4h], 0x8048b8c ; [0x8048b8c:4]=0x6325                                                      
 |   0x080487ab      c70424010000.  mov dword [esp], 1                                                                                          
 |   0x080487b2      2b44241c       sub eax, dword [local_1ch]                                                                                  
 |   0x080487b6      31c8           xor eax, ecx                                                                                                
 |   0x080487b8      31f0           xor eax, esi                                                                                                
 |   0x080487ba      0fbec0         movsx eax, al                                                                                               
 |   0x080487bd      89442408       mov dword [local_8h], eax                                                                                   
 |   0x080487c1      e8bafbffff     call sym.imp.__printf_chk   ;[2]                                                                            
```

We will work backwards here, value at EAX is printed , ESI contains value from the location `local_14h` and ECX contains some value we do not know were that value comes from , the difference from the `local_1ch` `local_2ch` is stored EAX it will be zero from last loop the value are xored , `xor eax, ecx` just copy the value from ecx to eax, then esi and eax is xored , and the last byte is printed

We have to figure out how ecx is set and the value of `local_14h`

We can see that the ECX is set on the above loop , but debugging that loop we can see that during first few iteration the ecx value is changing after that the ECX have the same value , We do not need to loop large number of time to figure out ecx's final value thus reduce the time needed

```nasm
0x080486a8 b    8b3504860908   mov esi, dword [0x8098604]  ; [0x8098604:4]=0                                                               
0x080486ae      c744242c0000.  mov dword [local_2ch], 0                                                                                    
0x080486b6      a100860908     mov eax, dword [0x8098600]  ; [0x8098600:4]=0                                                               
0x080486bb      8b7c2418       mov edi, dword [count]      ; [0x18:4]=-1 ; 24                                                              
0x080486bf      2b3544a00408   sub esi, dword [0x804a044]                                                                                  
0x080486c5      2b0540a00408   sub eax, dword [0x804a040]                                                                                  
0x080486cb      8b1cbd804c08.  mov ebx, dword [edi*4 + 0x8084c80] ; [0x8084c80:4]=0x175f9165                                               
0x080486d2      8b0cbd201307.  mov ecx, dword [edi*4 + 0x8071320] ; [0x8071320:4]=0x81af                                                   
0x080486d9      31c6           xor esi, eax                                                                                                
0x080486db      a108860908     mov eax, dword [0x8098608]  ; [0x8098608:4]=0                                                               
0x080486e0      895c241c       mov dword [local_1ch], ebx                                                                                  
0x080486e4      2b0548a00408   sub eax, dword [0x804a048]                                                                                  
0x080486ea      31c6           xor esi, eax                                                                                                
0x080486ec      a10c860908     mov eax, dword [0x809860c]  ; [0x809860c:4]=0                                                               
0x080486f1      2b054ca00408   sub eax, dword [0x804a04c]                                                                                  
0x080486f7      31c6           xor esi, eax                                                                                                
0x080486f9      8b44242c       mov eax, dword [local_2ch]  ; [0x2c:4]=-1 ; ',' ; 44                                                        
0x080486fd      3334bd60a004.  xor esi, dword [edi*4 + 0x804a060]                                                                          
0x08048704      39d8           cmp eax, ebx                                                                                                
0x08048706      8934bd60a004.  mov dword [edi*4 + 0x804a060], esi ; [0x804a060:4]=0x39e58d23                                               
0x0804870d      0f838c000000   jae 0x804879f               ;[2]                                                                            
0x08048713      8b04bdc0d905.  mov eax, dword [edi*4 + 0x805d9c0] ; [0x805d9c0:4]=0x308ade1d                                               
0x0804871a      89742414       mov dword [local_14h], esi                                                                                  
```

The value of `local_1ch` which is the number of time the loop should run is loaded from `0x8084c80` address and `local_14h` value is read from `0x804a060` the the value is not just read but xor value of previous esi and this location is read , for correct value to be loaded the value at esi should be zero ,

```nasm
[0x0804869b]> px 40 @ 0x804a060
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x0804a060  238d e539 2634 7107 911b c43b 0df0 245e  #..9&4q....;..$^
0x0804a070  8214 1435 bdda 4c28 00bc 501e 8dfc bc2b  ...5..L(..P....+
0x0804a080  9626 776e a28f d27c                      .&wn...|
```

```nasm
[0x0804869b]> px 40 @ 0x8084c80
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x08084c80  6591 5f17 c734 1e48 e76c a721 8aba 2456  e._..4.H.l.!..$V
0x08084c90  1fd4 2d37 5cd0 926f eb1e 327b b648 1a54  ..-7\..o..2{.H.T
0x08084ca0  58da 0767 1a51 9835                      X..g.Q.5
```

the first value at `0x8084c80` is

```nasm
[0x0804869b]> x/d  @ 0x8084c80
0x08084c80  0x175f9165 0x481e34c7                        e._..4.H
```

So the loop will run 0x175f9165 times we can reduce this number to save and very low number , I patched the numbers to 100

```nasm
[0x080487e3]> x/4d  @ 0x8084c80
0x08084c80  0x00000100 0x00000100 0x00000100 0x00000100  ................
0x08084c90  0x00000100 0x00000100 0x00000100 0x00000100  ................
```

Well running does not give the desirable output but first characters are printed faster

```sh
$ ./optimize_me
Welcome to f0xtr0t's extremely slow program
-------------------------------------------

oM@
```

What is happening over there , well it turns out that there is a check to find out if the binary is changed .

As i said before loading the value to `local_14h` it is xored with ESI and ESI's value is zero when `0x8098600` and `0x804a040` are equal , `0x0804a040` is inside the binary and `0x08098600` is calculated on runtime,

```nasm
[0x08048680]> axt 0x8098600
main 0x80486b6 (data) mov eax, dword [0x8098600]
main 0x8048776 (data) mov eax, dword [edx*4 + 0x8098600]
(nofunc) 0x804845f (data) mov dword [0x8098600], ecx
(nofunc) 0x8048a69 (data) mov eax, dword [edx*4 + 0x8098600]
```

`0x08048390` contains the code which calculate checksum we can run the binary and read the content at this address and patch the same value to the binary so the check will be true , so we open radare in debug mode and

```nasm
[0xf77d8a20]> db 0x080486a8
[0xf77d8a20]> dc
Welcome to f0xtr0t's extremely slow program
-------------------------------------------

hit breakpoint at: 80486a8
[0x080486a8]> px 20 @ 0x8098600
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x08098600  f66b 2a23 3768 7b2a ae4c 9735 dee5 3341  .k*#7h{*.L.5..3A
0x08098610  0000 0000                                ....
[0x080486a8]> px 20 @ 0x804a040
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x0804a040  652d 77b9 3768 7b2a ae4c 9735 dee5 3341  e-w.7h{*.L.5..3A
0x0804a050  0000 0000                                ....
```

Open radare in write mode

```nasm
[0x080487e3]> wex 0xf66b2a23 @ 0x0804a040
[0x080487e3]> px 20 @ 0x804a040
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x0804a040  f66b 2a23 3768 7b2a ae4c 9735 dee5 3341  .k*#7h{*.L.5..3A
0x0804a050  0000 0000                                ....
[0x080487e3]> q
```

But there is a problem there are around 0x4e52 values in location `0x08084c80` which we need to change to 100 , to reduce the runtime, doing it one by one is not an option we need to automate it , it turnout radare has the wright command to do this

```nasm
[0x08084c80]> !rax2 0x4e52*4
80200
[0x08084c80]> wex 0x00010000 @@s:$$ $$+80200 4
```

$$ means current seek `@@` is the iterator , it iterates command on specified locations ,

    [0x08084c80]> @@?
    |@@  # foreach iterator command:
    | Repeat a command over a list of offsets  
    | x @@ sym.*                               run 'x' over all flags matching 'sym.' in current flagspace
    | x @@dbt[abs]                             run 'x' command on every backtrace address, bp or sp
    | x @@.file                                run 'x' over the offsets specified in the file (one offset per line)
    | x @@=off1 off2 ..                        manual list of offsets
    | x @@/x 9090                              temporary set cmd.hit to run a command on each search result
    | x @@k sdbquery                           run 'x' on all offsets returned by that sdbquery
    | x @@t                                    run 'x' on all threads (see dp)
    | x @@b                                    run 'x' on all basic blocks of current function (see afb)
    | x @@i                                    run 'x' on all instructions of the current function (see pdr)
    | x @@f                                    run 'x' on all functions (see aflq)
    | x @@f:write                              run 'x' on all functions matching write in the name
    | x @@s:from to step                       run 'x' on all offsets from, to incrementing by step
    | x @@c:cmd                                the same as @@=`` without the backticks
    | x @@=`pdf~call[0]`                       run 'x' at every call offset of the current function

Running the Binary now gives the flag!

    $ ./optimize_me  | grep CTF
    CTF{n0w_w4snt_th4t_some_qu1ck_th1nking_eh}
