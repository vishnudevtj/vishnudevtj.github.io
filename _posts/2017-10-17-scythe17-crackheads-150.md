---
title:  Scythe17 Crackheads 150
updated: 2017-10-17 19:03:06
---

- [crackheads scythe17 - 150](#org815fc38)


<a id="org815fc38"></a>

# crackheads scythe17 - 150

> feignix and nazgul were fighting over a tide. reverse [me](http://hack.bckdr.in/CRACKHEADS/rev).

I had fun solving this challenge and it improved my radare skill

```sh
file rev 
rev: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
for GNU/Linux 2.6.24, BuildID[sha1]=deeb187ed41eed710a81bad92c2a723ea925690f, stripped
```

running the binary prints a tempting message

    $ ./rev
    
    [↑] Launching stage 1
    [↑] Launching stage 2
    [*] Key x is incorrect
    [↑] Launching stage 3
    [*] Key x is incorrect
    [↑] Launching stage 4
    Enter password: hello
    [*] Key x is incorrect
    [*] Key says it is not for you
    Entering the last check:hello
    Don't leave me with the rest of your unsolved task :(

So challenge accepted !

There are totally 5 constrains ,we need to find to success Strings in the binary

    [0x00400f00]> izq
    0x4023bf 30 29 FATAL: Cannot allocate memory
    0x4023e0 61 60 \e[34mDon't try to fool me around by modifying the binary\e[0m
    0x40241d 13 12 \e[33m%s\e[0m\n
    0x40242a 8 7 ARCTYPE
    0x402438 41 40 \e[31m[*] Key says it is not for you\e[0m\n
    0x402461 6 5 amd64
    0x402468 31 30 \e[32m[*] Key x is correct\e[0m\n
    0x402488 33 32 \e[31m[*] Key x is incorrect\e[0m\n
    0x4024a9 6 5 psscr
    0x4024af 6 5 auwod
    0x4024b5 6 5 snoli
    0x4024bb 27 26 \e[35mEnter password: \e[33m
    0x4024da 5 4 %02x
    0x4024df 5 4 %lld
    0x4024e8 34 31 \e[36m[↑] Launching stage 1\e[0m\n
    0x40250a 17 16 creation failed\n
    0x402520 34 31 \e[36m[↑] Launching stage 2\e[0m\n
    0x402548 34 31 \e[36m[↑] Launching stage 3\e[0m\n
    0x402570 34 31 \e[36m[↑] Launching stage 4\e[0m\n
    0x402592 25 24 Entering the last check:
    0x4025b0 34 33 \n\e[33mIt is not the time yet\e[0m\n
    0x4025d8 61 60 \n\e[33mOnly way to get flag is to feed me a correct time\e[0m\n
    0x402618 46 45 \n\e[33mDo not hesitate to give time to me\e[0m\n
    0x402648 32 31 \n\e[32m[*] Key x is correct\e[0m\n
    0x402668 64 63 \e[34mDon't leave me with the rest of your unsolved task :(\e[0m\n

Looking into the main we can see that the binary uses multi threading and all the stages are started on different thread

```nasm
0x00402061      bfe8244000     mov edi, str._e_36m______Launching_stage_1_e_0m_n ; 0x4024e8
0x00402066      e882efffff     call sub.printf_fed         ; int printf(const char *format)
0x0040206b      bfa0316000     mov edi, 0x6031a0
0x00402070      e84beeffff     call sym.imp.pthread_mutex_unlock
0x00402075      488d75b0       lea rsi, [local_50h]
0x00402079      488d85e0feff.  lea rax, [local_120h]
0x00402080      b900000000     mov ecx, 0
0x00402085      ba161b4000     mov edx, 0x401b16
0x0040208a      4889c7         mov rdi, rax
0x0040208d      e83eedffff     call sym.imp.pthread_create
0x00402092      85c0           test eax, eax
```

`0x401b16` contains the code for the stage 1 radare did not identify this as a function and we can't see this region in graph view so we tell radare to analyse the region and mark it as function

```nasm
[0x00402044]> af @ 0x401b16
[0x00402044]> afl ~401b16
0x00401b16   10 1190         fcn.00401b16
[0x00402044]> s 0x401b16
[0x00401b16]> afn stage_1
```

Let's analyse this function here

```nasm
0x00401b1a]> pd 20 @ 0x00401b32
|           0x00401b32      488945e8       mov qword [local_18h], rax
|           0x00401b36      31c0           xor eax, eax
|           0x00401b38      e843f3ffff     call sym.imp.getuid         ; uid_t getuid(void)
|           0x00401b3d      898550ffffff   mov dword [uid], eax
|           0x00401b43      e858f2ffff     call sym.imp.geteuid        ; uid_t geteuid(void)
|           0x00401b48      898554ffffff   mov dword [euid], eax
|           0x00401b4e      48c745d00000.  mov qword [local_30h], 0
|           0x00401b56      48c745d80000.  mov qword [local_28h], 0
|           0x00401b5e      c745e0000000.  mov dword [local_20h], 0
|           0x00401b65      66c745e40000   mov word [local_1ch], 0
|           0x00401b6b      83bd50ffffff.  cmp dword [uid], 0xffffffffffffffff
|       ,=< 0x00401b72      0f85e0030000   jne 0x401f58
|       |   0x00401b78      83bd54ffffff.  cmp dword [euid], 0
|      ,==< 0x00401b7f      0f85d3030000   jne 0x401f58
|      ||   0x00401b85      c705b1152000.  mov dword [0x00603140], 0   ; [0x603140:4]=1
|      ||   0x00401b8f      b8aaf6ffff     mov eax, 0xfffff6aa         ; 4294964906
|      ||   0x00401b94      2b8550ffffff   sub eax, dword [uid]
|      ||   0x00401b9a      89c2           mov edx, eax
|      ||   0x00401b9c      8b8554ffffff   mov eax, dword [euid]
|      ||   0x00401ba2      01d0           add eax, edx

```

`getuid()` and `geteuid` functions are called and the return values are checked with -1 and 0 respectively , if true then Some calculation are done and the sting 'key is correct' is printed , else some values are set in memory and incorrect key error is printed

```nasm
 .---------------------------------------------------.
 |  0x401f58 ;[gc]                                   |
 |      ; JMP XREF from 0x00401b72 (stage_1)         |
 |      ; JMP XREF from 0x00401b7f (stage_1)         |
 |      ; [0x603140:4]=1                             |
 | mov dword [0x00603140], 1                         |
 |    ; [0x603144:4]=1                               |
 | mov dword [0x00603144], 1                         |
 |    ; [0x603148:4]=1                               |
 | mov dword [0x00603148], 1                         |
 |    ; [0x60314c:4]=1                               |
 | mov dword [0x0060314c], 1                         |
 | mov edi, 0x6031a0                                 |
 | call sym.imp.pthread_mutex_lock;[go]              |
 |    ; 0x402488                                     |
 | mov edi, str._e_31m____Key_x_is_incorrect_e_0m_n  |
 | call sub.printf_fed;[gp]                          |
 | mov edi, 0x6031a0                                 |
 | call sym.imp.pthread_mutex_unlock;[gq]            |
 `---------------------------------------------------'
     v
```

How can we satisfy this condition we can get uid and euid to be zero if it is running as root , can the uid value can be negative not in normal situation , so i created a evil shared object and tell to load this shared library first and our evil functions will be executed which returns the required value

```C
int getuid()
{
    return 0xffffffff;
}
int geteuid()
{
  return 0;
}
```

```shell
gcc -shared -fPIC -o uid_evil.so uid_evil.c
```

The file which `LD_PRELOAD` specify is loaded to before any other is loaded so we get our evil uid function

So One down and 4 to GO!

Stage 2 :

```nasm
| mov edi, str._e_36m______Launching_stage_2_e_0m_n  |
| call sub.printf_fed;[gg]                           |
| mov edi, 0x6031a0                                  |
| call sym.imp.pthread_mutex_unlock;[gh]             |
| mov rax, qword [local_140h]                        |
| mov rdx, qword [rax]                               |
| lea rax, [local_50h]                               |
| lea rcx, [local_120h]                              |
|    ; 8                                             |
| lea rdi, [rcx + 8]                                 |
| mov rcx, rdx                                       |
| mov edx, 0x401862                                  |
| mov rsi, rax                                       |
| call sym.imp.pthread_create;[gi]                   |
```

```nasm
[0x00401fbc]> af @ 0x401862
[0x00401fbc]> s 0x401862
[0x00401862]> afn stage_2
```

```nasm
|           0x004018c5      8d9540ffffff   lea edx, [local_c0h]
|           0x004018cb      488b85d8feff.  mov rax, qword [local_128h]
|           0x004018d2      4889d6         mov rsi, rdx
|           0x004018d5      4889c7         mov rdi, rax
|           0x004018d8      e813f5ffff     call sym.imp.statfs
|           0x004018dd      8985ccfeffff   mov dword [local_134h], eax
|           0x004018e3      83bdccfeffff.  cmp dword [local_134h], 0
|       ,=< 0x004018ea      7405           je 0x4018f1
|      ,==< 0x004018ec      e9c1010000     jmp 0x401ab2
|      ||      ; JMP XREF from 0x004018ea (stage_2)
|      |`-> 0x004018f1      488b8540ffff.  mov rax, qword [local_c0h]
|      |    0x004018f8      483185d0feff.  xor qword [local_130h], rax
|      |    0x004018ff      488b8540ffff.  mov rax, qword [local_c0h]
|      |    0x00401906      483d60960000   cmp rax, 0x9660
|      |,=< 0x0040190c      7405           je 0x401913
|     ,===< 0x0040190e      e99f010000     jmp 0x401ab2
|     |||      ; JMP XREF from 0x0040190c (stage_2)
|     ||`-> 0x00401913      488d9540ffff.  lea rdx, [local_c0h]
|     ||    0x0040191a      488b85d8feff.  mov rax, qword [local_128h]
|     ||    0x00401921      4889d6         mov rsi, rdx
|     ||    0x00401924      4889c7         mov rdi, rax
|     ||    0x00401927      e8c4f4ffff     call sym.imp.statfs
|     ||    0x0040192c      8985ccfeffff   mov dword [local_134h], eax
|     ||    0x00401932      83bdccfeffff.  cmp dword [local_134h], 0
|     ||,=< 0x00401939      7405           je 0x401940
|    ,====< 0x0040193b      e972010000     jmp 0x401ab2
|    ||||      ; JMP XREF from 0x00401939 (stage_2)
|    |||`-> 0x00401940      488b8540ffff.  mov rax, qword [local_c0h]
|    |||    0x00401947      483185d0feff.  xor qword [local_130h], rax
|    |||    0x0040194e      488b8540ffff.  mov rax, qword [local_c0h]
|    |||    0x00401955      483dea1dad0b   cmp rax, 0xbad1dea
|    |||,=< 0x0040195b      7405           je 0x401962
|   ,=====< 0x0040195d      e950010000     jmp 0x401ab2
|   |||||      ; JMP XREF from 0x0040195b (stage_2)
|   ||||`-> 0x00401962      488d9540ffff.  lea rdx, [local_c0h]
|   ||||    0x00401969      488b85d8feff.  mov rax, qword [local_128h]
|   ||||    0x00401970      4889d6         mov rsi, rdx
|   ||||    0x00401973      4889c7         mov rdi, rax
|   ||||    0x00401976      e875f4ffff     call sym.imp.statfs
|   ||||    0x0040197b      8985ccfeffff   mov dword [local_134h], eax
|   ||||    0x00401981      83bdccfeffff.  cmp dword [local_134h], 0
|   ||||,=< 0x00401988      7405           je 0x40198f
|  ,======< 0x0040198a      e923010000     jmp 0x401ab2
|  ||||||      ; JMP XREF from 0x00401988 (stage_2)
|  |||||`-> 0x0040198f      488b8540ffff.  mov rax, qword [local_c0h]
|  |||||    0x00401996      4883c001       add rax, 1
|  |||||    0x0040199a      483185d0feff.  xor qword [local_130h], rax
|  |||||    0x004019a1      488b9540ffff.  mov rdx, qword [local_c0h]
|  |||||    0x004019a8      b8114afeca     mov eax, 0xcafe4a11
|  |||||    0x004019ad      4839c2         cmp rdx, rax
|  |||||,=< 0x004019b0      0f85fc000000   jne 0x401ab2
|  ||||||   0x004019b6      bf21000000     mov edi, 0x21               ; '!' ; 33
|  ||||||   0x004019bb      e860f6ffff     call sub.malloc_20          ;  void *malloc(size_t size)
|  ||||||   0x004019c0      488905b11720.  mov qword [0x00603178], rax ; [0x603178:8]=0
|  ||||||   0x004019c7      c70573172000.  mov dword [0x00603144], 0   ; [0x603144:4]=1
```

Well `statfs` is a function which gets the statistics of the file system , from man

    SYNOPSIS
           #include <sys/vfs.h>    /* or <sys/statfs.h> */
    
           int statfs(const char *path, struct statfs *buf);
           int fstatfs(int fd, struct statfs *buf);
    
    DESCRIPTION
           The  statfs()  system  call returns information about a mounted filesystem.  path is the pathname of any file within the mounted filesystem.
           buf is a pointer to a statfs structure defined approximately as follows:

On every call of the `statfs` same argument are passed and the return of every should satisfy the uniq condition ,

The return this is xor with a `local_130h` , actually the return is the file system type , all file system contains a uniq magic number

    BPF_FS_MAGIC          0xcafe4a11
    HOSTFS_SUPER_MAGIC    0x00c0ffee
    ISOFS_SUPER_MAGIC     0x9660

To bypass this stage, i set the RIP from the first comparison to the last and set the `local_130h` with appropriate value after all the xor of the return value , I not sure this is the right method , but it does the trick

Next !

```nasm
 .----------------------------------------------.
 |  0x40211d ;[gm]                              |
 |      ; JMP XREF from 0x004020fd (main)       |
 | mov edi, 0x6031a0                            |
 | call sym.imp.pthread_mutex_lock;[gf]         |
 |    ; 0x402548                                |
 | mov edi, str._e_36m______Launching_stage_3_e |
 | call sub.printf_fed;[gg]                     |
 | mov edi, 0x6031a0                            |
 | call sym.imp.pthread_mutex_unlock;[gh]       |
 | lea rax, [local_50h]                         |
 | lea rdx, [local_120h]                        |
 |    ; 16                                      |
 | lea rdi, [rdx + 0x10]                        |
 | mov ecx, 0                                   |
 | mov edx, 0x4015db                            |
 | ...                                          |
 `----------------------------------------------'
```

Here we have to input a Password ,

Fist some strings are loaded to the stack

```nasm
 mov qword [local_20h], str.psscr
 mov qword [local_18h], str.auwod
 mov qword [local_10h], str.snoli
```

There is a string length is compared with 0xf

```nasm
mov rax, qword [input]   
add rax, 0xf             
mov byte [rax], 0        
mov rax, qword [input]   
mov rdi, rax             
call sym.imp.strlen;[gj] 
```

after there is a loop which check the input with strings on the stack , the three stings are selected according to the index of the input and is checked , well i did it in the long way of using gdb extracting characters from the comparison , I need to learn to script in gdb ! .

```nasm
|           0x00401678      c745dc000000.  mov dword [count], 0
|       ,=< 0x0040167f      e952010000     jmp 0x4017d6
|       |      ; JMP XREF from 0x004017da (fcn.004015db)
|      .--> 0x00401684      8b4ddc         mov ecx, dword [count]
|      ||   0x00401687      ba56555555     mov edx, 0x55555556
|      ||   0x0040168c      89c8           mov eax, ecx
|      ||   0x0040168e      f7ea           imul edx
|      ||   0x00401690      89c8           mov eax, ecx
|      ||   0x00401692      c1f81f         sar eax, 0x1f
|      ||   0x00401695      29c2           sub edx, eax
|      ||   0x00401697      89d0           mov eax, edx
|      ||   0x00401699      89c2           mov edx, eax
|      ||   0x0040169b      01d2           add edx, edx
|      ||   0x0040169d      01c2           add edx, eax
|      ||   0x0040169f      89c8           mov eax, ecx
|      ||   0x004016a1      29d0           sub eax, edx
|      ||   0x004016a3      83f801         cmp eax, 1                  ; 1
|     ,===< 0x004016a6      7472           je 0x40171a
|     |||   0x004016a8      83f802         cmp eax, 2                  ; 2
|    ,====< 0x004016ab      0f84c7000000   je 0x401778
|    ||||   0x004016b1      85c0           test eax, eax
|   ,=====< 0x004016b3      0f8519010000   jne 0x4017d2
|   |||||   0x004016b9      8b45dc         mov eax, dword [count]
|   |||||   0x004016bc      4863d0         movsxd rdx, eax
|   |||||   0x004016bf      488b45f8       mov rax, qword [input]
|   |||||   0x004016c3      4801d0         add rax, rdx                ; '('
|   |||||   0x004016c6      0fb630         movzx esi, byte [rax]
|   |||||   0x004016c9      8b4ddc         mov ecx, dword [count]
|   |||||   0x004016cc      ba56555555     mov edx, 0x55555556
|   |||||   0x004016d1      89c8           mov eax, ecx
|   |||||   0x004016d3      f7ea           imul edx
|   |||||   0x004016d5      89c8           mov eax, ecx
|   |||||   0x004016d7      c1f81f         sar eax, 0x1f
|   |||||   0x004016da      29c2           sub edx, eax
|   |||||   0x004016dc      89d0           mov eax, edx
|   |||||   0x004016de      8d0c00         lea ecx, [rax + rax]
|   |||||   0x004016e1      ba67666666     mov edx, 0x66666667
|   |||||   0x004016e6      89c8           mov eax, ecx
|   |||||   0x004016e8      f7ea           imul edx
|   |||||   0x004016ea      d1fa           sar edx, 1
|   |||||   0x004016ec      89c8           mov eax, ecx
|   |||||   0x004016ee      c1f81f         sar eax, 0x1f
|   |||||   0x004016f1      29c2           sub edx, eax
|   |||||   0x004016f3      89d0           mov eax, edx
|   |||||   0x004016f5      c1e002         shl eax, 2
|   |||||   0x004016f8      01d0           add eax, edx
|   |||||   0x004016fa      29c1           sub ecx, eax
|   |||||   0x004016fc      89ca           mov edx, ecx
|   |||||   0x004016fe      4863d2         movsxd rdx, edx
|   |||||   0x00401701      488b45e0       mov rax, qword [psscr]
|   |||||   0x00401705      4801d0         add rax, rdx                ; '('
|   |||||   0x00401708      0fb600         movzx eax, byte [rax]
|   |||||   0x0040170b      4038c6         cmp sil, al
|  ,======< 0x0040170e      7405           je 0x401715
| ,=======< 0x00401710      e905010000     jmp 0x40181a
| |||||!|      ; JMP XREF from 0x0040170e (fcn.004015db)
| =`------> 0x00401715      e9b8000000     jmp 0x4017d2
| | |||!|      ; JMP XREF from 0x004016a6 (fcn.004015db)
| | ||`---> 0x0040171a      8b45dc         mov eax, dword [count]
| | || ||   0x0040171d      4863d0         movsxd rdx, eax
| | || ||   0x00401720      488b45f8       mov rax, qword [input]
| | || ||   0x00401724      4801d0         add rax, rdx                ; '('
| | || ||   0x00401727      0fb630         movzx esi, byte [rax]
| | || ||   0x0040172a      8b4ddc         mov ecx, dword [count]
| | || ||   0x0040172d      ba56555555     mov edx, 0x55555556
| | || ||   0x00401732      89c8           mov eax, ecx
| | || ||   0x00401734      f7ea           imul edx
| | || ||   0x00401736      89c8           mov eax, ecx
| | || ||   0x00401738      c1f81f         sar eax, 0x1f
| | || ||   0x0040173b      29c2           sub edx, eax
| | || ||   0x0040173d      89d0           mov eax, edx
| | || ||   0x0040173f      8d0c00         lea ecx, [rax + rax]
| | || ||   0x00401742      ba67666666     mov edx, 0x66666667
| | || ||   0x00401747      89c8           mov eax, ecx
| | || ||   0x00401749      f7ea           imul edx
| | || ||   0x0040174b      d1fa           sar edx, 1
| | || ||   0x0040174d      89c8           mov eax, ecx
| | || ||   0x0040174f      c1f81f         sar eax, 0x1f
| | || ||   0x00401752      29c2           sub edx, eax
| | || ||   0x00401754      89d0           mov eax, edx
| | || ||   0x00401756      c1e002         shl eax, 2
| | || ||   0x00401759      01d0           add eax, edx
| | || ||   0x0040175b      29c1           sub ecx, eax
| | || ||   0x0040175d      89ca           mov edx, ecx
| | || ||   0x0040175f      4863d2         movsxd rdx, edx
| | || ||   0x00401762      488b45e8       mov rax, qword [auwod]
| | || ||   0x00401766      4801d0         add rax, rdx                ; '('
| | || ||   0x00401769      0fb600         movzx eax, byte [rax]
| | || ||   0x0040176c      4038c6         cmp sil, al
| | ||,===< 0x0040176f      7405           je 0x401776
| |,======< 0x00401771      e9a4000000     jmp 0x40181a
| |||||!|      ; JMP XREF from 0x0040176f (fcn.004015db)
| ====`---> 0x00401776      eb5a           jmp 0x4017d2
| |||| !|      ; JMP XREF from 0x004016ab (fcn.004015db)
| |||`----> 0x00401778      8b45dc         mov eax, dword [count]
| |||  ||   0x0040177b      4863d0         movsxd rdx, eax
| |||  ||   0x0040177e      488b45f8       mov rax, qword [input]
| |||  ||   0x00401782      4801d0         add rax, rdx                ; '('
| |||  ||   0x00401785      0fb630         movzx esi, byte [rax]
| |||  ||   0x00401788      8b4ddc         mov ecx, dword [count]
| |||  ||   0x0040178b      ba56555555     mov edx, 0x55555556
| |||  ||   0x00401790      89c8           mov eax, ecx
| |||  ||   0x00401792      f7ea           imul edx
| |||  ||   0x00401794      89c8           mov eax, ecx
| |||  ||   0x00401796      c1f81f         sar eax, 0x1f
| |||  ||   0x00401799      29c2           sub edx, eax
| |||  ||   0x0040179b      89d0           mov eax, edx
| |||  ||   0x0040179d      8d0c00         lea ecx, [rax + rax]
| |||  ||   0x004017a0      ba67666666     mov edx, 0x66666667
| |||  ||   0x004017a5      89c8           mov eax, ecx
| |||  ||   0x004017a7      f7ea           imul edx
| |||  ||   0x004017a9      d1fa           sar edx, 1
| |||  ||   0x004017ab      89c8           mov eax, ecx
| |||  ||   0x004017ad      c1f81f         sar eax, 0x1f
| |||  ||   0x004017b0      29c2           sub edx, eax
| |||  ||   0x004017b2      89d0           mov eax, edx
| |||  ||   0x004017b4      c1e002         shl eax, 2
| |||  ||   0x004017b7      01d0           add eax, edx
| |||  ||   0x004017b9      29c1           sub ecx, eax
| |||  ||   0x004017bb      89ca           mov edx, ecx
| |||  ||   0x004017bd      4863d2         movsxd rdx, edx
| |||  ||   0x004017c0      488b45f0       mov rax, qword [snoli]
| |||  ||   0x004017c4      4801d0         add rax, rdx                ; '('
| |||  ||   0x004017c7      0fb600         movzx eax, byte [rax]
| |||  ||   0x004017ca      4038c6         cmp sil, al
| ||| ,===< 0x004017cd      7402           je 0x4017d1
| |||,====< 0x004017cf      eb49           jmp 0x40181a
| |||||!|      ; JMP XREF from 0x004017cd (fcn.004015db)
| ||||`---> 0x004017d1      90             nop
| |||| !|      ; JMP XREF from 0x004016b3 (fcn.004015db)
| |||| !|      ; JMP XREF from 0x00401715 (fcn.004015db)
| |||| !|      ; JMP XREF from 0x00401776 (fcn.004015db)
| --`-----> 0x004017d2      8345dc01       add dword [count], 1
| || | !|      ; JMP XREF from 0x0040167f (fcn.004015db)
| || | |`-> 0x004017d6      837ddc0e       cmp dword [count], 0xe      ; [0xe:4]=-1 ; 14
| || | `==< 0x004017da      0f8ea4feffff   jle 0x401684
| || |      0x004017e0      c7055e192000.  mov dword [0x00603148], 0   ; [0x603148:4]=1
| || |      0x004017ea      488b45f8       mov rax, qword [input]
| || |      0x004017ee      4889058b1920.  mov qword [0x00603180], rax ; [0x603180:8]=0
| || |      0x004017f5      bfa0316000     mov edi, 0x6031a0
| || |      0x004017fa      e8a1f6ffff     call sym.imp.pthread_mutex_lock
| || |      0x004017ff      bf68244000     mov edi, str._e_32m____Key_x_is_correct_e_0m_n ; 0x402468
| || |      0x00401804      e8e4f7ffff     call sub.printf_fed         ; int printf(const char *format)
| || |      0x00401809      bfa0316000     mov edi, 0x6031a0
| || |      0x0040180e      e8adf6ffff     call sym.imp.pthread_mutex_unlock
| || |      0x00401813      b800000000     mov eax, 0
| || |  ,=< 0x00401818      eb46           jmp 0x401860
| || |  |      ; JMP XREF from 0x00401651 (fcn.004015db)
| || |  |      ; JMP XREF from 0x00401673 (fcn.004015db)
| || |  |      ; JMP XREF from 0x00401710 (fcn.004015db)
| || |  |      ; JMP XREF from 0x00401771 (fcn.004015db)
| || |  |      ; JMP XREF from 0x004017cf (fcn.004015db)
| ``-`----> 0x0040181a      c7051c192000.  mov dword [0x00603140], 1   ; [0x603140:4]=1
|       |   0x00401824      c70516192000.  mov dword [0x00603144], 1   ; [0x603144:4]=1
|       |   0x0040182e      c70510192000.  mov dword [0x00603148], 1   ; [0x603148:4]=1
|       |   0x00401838      c7050a192000.  mov dword [0x0060314c], 1   ; [0x60314c:4]=1
|       |   0x00401842      bfa0316000     mov edi, 0x6031a0
|       |   0x00401847      e854f6ffff     call sym.imp.pthread_mutex_lock
|       |   0x0040184c      bf88244000     mov edi, str._e_31m____Key_x_is_incorrect_e_0m_n ; 0x402488
|       |   0x00401851      e897f7ffff     call sub.printf_fed         ; int printf(const char *format)
|       |   0x00401856      bfa0316000     mov edi, 0x6031a0
|       |   0x0040185b      e860f6ffff     call sym.imp.pthread_mutex_unlock
|       |      ; JMP XREF from 0x00401818 (fcn.004015db)
|       `-> 0x00401860      c9             leave
\           0x00401861      c3             ret
```

Password is : passwordisuncolo

Stage 4 Here I Come !

```nasm
mov byte [local_20h], 8   
   ; '^'                  
mov byte [local_1fh], 0x5e
   ; '\'                  
mov byte [local_1eh], 0x5c
mov byte [local_1dh], 0   
mov byte [local_1ch], 0x14
mov byte [local_1bh], 0   
   ; 0x40242a             
   ; "ARCTYPE"            
mov edi, str.ARCTYPE      
call sym.imp.getenv;[ga]  
mov qword [local_28h], rax
cmp qword [local_28h], 0  
je 0x401479;[gb]          
```

Here a environmental variable named ARCTYPE is read , then the len is checked if it is 5 , after that the input is xor with a predefined key which is pushed onto the stack on the beginning and it is checked with amd64 , it turn's out the input should be "i386 "

```python
key = [8,0x5e,0x5c,0,0x14]
flag = "amd64"
result = ""

for i in range(0,len(key)):
    for j in range(0,256):
        if key[i] ^ j == ord(flag[i]):
            result+=chr(j)
            break
```

So we have to set this variable before executing

For the last Check the a value at the memory address `0x00603150` is checked and i patched this location in binary using radare , to 0 which is the required condition

    (gdb) set environment export ARCTYPE="i386 "
    (gdb) set environment LD_PRELOAD=./uid_evil.so
    (gdb) b * 0x004018ea
    Breakpoint 1 at 0x4018ea
    (gdb) r
    Starting program: /home/nemesis/Downloads/rev 
    /bin/bash: cannot set uid to -1: effective uid 0: Invalid argument
    [Thread debugging using libthread_db enabled]
    Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
    [↑] Launching stage 1
    [New Thread 0x7ffff701a700 (LWP 15633)]
    [↑] Launching stage 2
    [*] Key x is correct
    [New Thread 0x7fffee819700 (LWP 15634)]
    [Thread 0x7ffff701a700 (LWP 15633) exited]
    [↑] Launching stage 3
    [New Thread 0x7ffff6819700 (LWP 15635)]
    Enter password: [Switching to Thread 0x7fffee819700 (LWP 15634)]
    
    Thread 3 "rev" hit Breakpoint 1, 0x00000000004018ea in ?? ()
    (gdb) x/10i $rip
    => 0x4018ea:	je     0x4018f1
       0x4018ec:	jmp    0x401ab2
       0x4018f1:	mov    rax,QWORD PTR [rbp-0xc0]
       0x4018f8:	xor    QWORD PTR [rbp-0x130],rax
       0x4018ff:	mov    rax,QWORD PTR [rbp-0xc0]
       0x401906:	cmp    rax,0x9660
       0x40190c:	je     0x401913
       0x40190e:	jmp    0x401ab2
       0x401913:	lea    rdx,[rbp-0xc0]
       0x40191a:	mov    rax,QWORD PTR [rbp-0x128]
    (gdb) set $rip=0x004019b6
    (gdb) x/x $rbp-0x130
    0x7fffee818e20:	0x00000000
    (gdb) set {int} 0x7fffee818e20 = 0xc153c198
    (gdb) c
    Continuing.
    passwordisuncolo
    [*] Key x is correct
    [*] Key x is correct
    [↑] Launching stage 4
    [New Thread 0x7ffff6018700 (LWP 21142)]
    [Thread 0x7ffff6819700 (LWP 15635) exited]
    [Thread 0x7fffee819700 (LWP 15634) exited]
    [*] Key x is correct
    [Thread 0x7ffff6018700 (LWP 21142) exited]
    Entering the last check:
    [*] Key x is correct
    flag{...}
    [Inferior 1 (process 15580) exited normally]
    (gdb) 

and there goes the flag

