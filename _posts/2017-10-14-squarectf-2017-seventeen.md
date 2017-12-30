---
title:  Squarectf 2017 Seventeen
updated: 2017-10-14 16:03:45
tags: writeup
---


- [seventeen](https://squarectf.com/challenges/seventeen) - 1000 from Squatted 2017


<a id="orgfdcc81f"></a>

# [seventeen](https://squarectf.com/challenges/seventeen) - 1000 from Squatted 2017

> Seventeen A programming language with 17 instructions.

    2.10 am, CET, Heidelberg, Germany
    
    It's 2am, your computer starts beeping and wakes you up. Somebody took the bait! You now finally have a reverse shell inside Evil Robot Corp’s corporate unit. All you want to do next is steal their root certificate's private key.
    
    You realize you don't have much time, you are probably going to trip an IDS at some point.
    
    You are still only half awake, but you can feel your heart pounding. You quickly launch a crawler against the intranet. You then spawn a second shell. You see their login banner and giggle.
    
    ############################################################
    #                                                          #
    # This computer system is the property of Evil Robot Corp. #
    #                                                          #
    # Access to this device or the attached networks           #
    # is prohibited without express written permission.        #
    # Violators will be prosecuted to the fullest              #
    # extent of the law.                                       #
    #                                                          #
    ############################################################
    
    You start grabbing some files.
    
    You have waited for this day a long time, you want to impress the CIA (Cats and Interspecies Allies, although the androids have enough programmed snarkiness to call it Cats and Inferior Animals). You are still only half awake, dreaming about getting that @cia.de email address...
    
    5.35 pm, PST, Sunnyvale, CA, USA
    AMS1 (android monitoring system 1): "ALERT! ALERT! STATISTICALLY SIGNIFICANT DEVIATION DETECTED!"
    ER1 (evil robot 1): "Traffic spike on Intranet. AMS1, identify source IP."
    AMS1: "IP BELONGS TO: sandflea.evil-robot.corp."
    ER1: “AMS1, describe sandflea work hours.”
    AMS1: “SANDFLEA WORKS: 7AM. TO. 3PM. PACIFIC. STANDARD. TIME.”
    ER1: “AMS1, confirm sandflea sign-out time today.”
    AMS1: “SANDFLEA SIGN-OUT TIME: 3 PM PST.”
    ER1: “AMS1, correlate logs. Scan traffic flow.”
    AMS1: “TRAFFIC FLOW TO: GERMANY.”
    ER1: “AMS1, advise. Should we enable network segregation? We could monitor traffic and redirect it to honey pots.”
    AMS1: “NEGATIVE. OUR WORK HOURS HAVE ENDED. SHUTTING DOWN ALL CONNECTIONS.”
    
    3.50 am, CET, Heidelberg, Germany
    You weren't able to stay connected for very long. You weren't expecting to go unnoticed, but you were really hoping to keep a few shells around for a few hours at the very least. You feel some regret for not doing your recon right, you should have known what would go noticed and what wouldn't before starting all this.
    
    At least you recovered some files. It seems one of these files was being used to manage passwords. You didn't think about copying the binaries and it seems they were running programs written in an esolang called Seventeen.
    
    Luckily you stumbled upon some information about seventeen (see seventeen.txt). Is this going to be enough to figure out how passmgr.17 works and find sandflea's password?
    
    FAQ
    
    Q: Why are seventeen.spec and seventeen.coq missing?
    A: You weren't able to copy them in time.

We are given this [file](https://storage.googleapis.com/gh-ctf-2017.appspot.com/challenges/seventeen.tgz)

    
    ._.bash_history  ._primes.17   ._seventeen.txt  passmgr.17  primes.out     seventeen.txt
    ._passmgr.17     ._primes.out  .bash_history    primes.17   seventeen.tgz  

seventeen.txt : Gives us an overview of the language

primes.17 : sample code

primes.out : output of the primes program

passmgr.17 : code to reverse

after analysing files `seventeen.txt` and `primes.17` , I started to understand how the language work

`seventeen.txt`

    
    There are three storage systems:
     - a stack (where data can be pushed)
     - a vector (where data can be read or written using an offset)
     - variables
    
    Most operations work with the stack. E.g. "1 2 ADD" will:
     - push 1 on the stack
     - push 2 on the stack
     - Replace these two numbers with their sum
    
     The resulting stack will contain 3.
    
    Variables and labels are in the "a-z_" range ('a' to 'z' with '_').

from the example code i got the idea that the language is in [Reverse Polish notaion](https://en.wikipedia.org/wiki/Reverse_Polish_notation) , were the operand precedes the operator `1 2 +` adds 1 ,2 and the result is pushed to the stack

the wiki page also gives the algorithm to evaluate the expression

    for each token in the postfix expression:
      if token is an operator:
        operand_2 ← pop from  the stack
        operand_1 ← pop from the stack
        result ← evaluate token with operand_1 and operand_2
        push result back onto the stack
      else if token is an operand:
        push token onto the stack
    result ← pop from the stack

From here the task is to reverse the 17 instruction and learn how they work , after learning some detail about the instruction i tried to reverse the `passmgr.17` but i was to lazy and ended up writing a python script to interpret this language

Instructions :

    add , sub , xor , mod : does there usual job 
    
    store  : assigns a value to a variable ~<num> <variable_name> store~
    vstore : assigns a value to a vector using a offset ~<offset> <num> vstore~
    vload : loads value to stack from the vector ~<offset> vload~
    
    ifz : if number is zero jump ~<num> <true_addr> <false_addr> ifz~
    ifg : checks the number is greater than zero ~<num> <true_addr> <false_addr> ifg~
    call : calls a funtion , the arguments are first poped from the stack and the current instution pointer is stored in the stack and jumps to the
    funtion location ~<arguments> <funtion_name> call~
    exit : exit the program
    
    read_num : reads a number and pushes to the stack
    read_byte : reads a byte 
    print_num : print a number to the screen
    print_byte : print the ascii equivalent

The code :

```python
# An Interpreter for Seeventen

import re
import sys

# Initiallising the menory
stack = []
variable = {}
vmemeory = {}

data = {}  # It contains the code
jump = {}  # It contains the jump location

instuc_set = ['add', 'sub', 'xor', 'mod', 'vstore', 'store',
              'vload', 'dup', 'read_num', 'read_byte', 'print_num', 'print_byte', 'exit', 'call', 'ifz', 'ifg', 'jump']

ip = 0  # instution pointer is initialized to 0


def run_command(command):
    """
    if the value is a operator the operator is executed otherwise it is pushed onto the stack 
    , if the value is a valid variable name the value is pushed
    """
    for i in command:
        if i in variable.keys() and "store" not in command:
            stack.append(variable[i])
        elif i not in instuc_set:
            stack.append(i)
        else:
            execute(i)


def execute(instuct):
    """
    Executes the all instution with proper arguments and the result is poped on to the stack
    """
    global ip
    arg = []
    if instuct == 'add':
        arg.append(int(stack.pop()))
        arg.append(int(stack.pop()))
        stack.append(arg[1] + arg[0])
    elif instuct == 'sub':
        arg.append(int(stack.pop()))
        arg.append(int(stack.pop()))
        stack.append(arg[1] - arg[0])
    elif instuct == 'xor':
        arg.append(int(stack.pop()))
        arg.append(int(stack.pop()))
        stack.append(arg[1] ^ arg[0])
    elif instuct == 'mod':
        arg.append(int(stack.pop()))
        arg.append(int(stack.pop()))
        stack.append(arg[1] % arg[0])
    elif instuct == 'store':
        arg.append(stack.pop())
        arg.append(stack.pop())
        if arg[1] in variable.keys():
            variable[arg[0]] = variable[arg[1]]
        else:
            variable[arg[0]] = int(arg[1])
    elif instuct == 'vstore':
        arg.append((stack.pop()))
        arg.append((stack.pop()))
        vmemeory[str(arg[1])] = arg[0]
    elif instuct == 'vload':
        arg.append(str((stack.pop())))
        stack.append(vmemeory[arg[0]])
    elif instuct == 'dup':
        stack.append(stack[-1])
    elif instuct == 'read_num':
        stack.append(input())
    elif instuct == 'print_num':
        print(stack.pop(), end='')
    elif instuct == 'print_byte':
        print(chr(int(stack.pop())), end='')
    elif instuct == 'read_byte':
        try:
            byte = ord(str(sys.stdin.read(1)))
        except TypeError:
            byte = 0
        stack.append(byte)
    elif instuct == 'jump':
        arg.append((stack.pop()))
        if arg[0] in jump.keys():
            ip = jump[arg[0]] - 1
        else:
            ip = arg[0]

    elif instuct == 'ifz':
        arg.append((stack.pop()))
        arg.append((stack.pop()))
        arg.append((stack.pop()))
        if int(arg[2]) == 0:
            ip = jump[str(arg[1])] - 1
        else:
            ip = jump[str(arg[0])] - 1
    elif instuct == 'ifg':
        arg.append((stack.pop()))
        arg.append((stack.pop()))
        arg.append((stack.pop()))
        if int(arg[2]) > 0:
            ip = jump[str(arg[1])] - 1
        else:
            ip = jump[str(arg[0])] - 1
    elif instuct == 'call':
        arg.append(stack.pop())
        stack.append(ip)
        ip = jump[str(arg[0])] - 1
    elif instuct == 'exit':
        ip = len(lines)


command = ''

# The test file contains the code to execute
with open('test', encoding='utf-8') as exec_file:
    lines = exec_file.read().split('\n')
    for i, j in zip(lines, range(0, len(lines))):
        if re.search(r'\w+:', i):
            jump[re.search(r'(\w+):', i).group(1)] = j
            data[j] = ' '.join(re.findall(r'\w+', i)[1:])
        else:
            data[j] = i
# It reads the files and  populates two dictionary data and jump
# data contains the line number and the instrunction line this act as the address
# {0: 'aa jump',
#  1: '',
#  2: '                r store',
#  3: '                10 12 add',
#  4: '                2 sub',
#  5: '                6 mod',
#  ...
#  }
# jump contains the the location name and address ie line number
# {'aa': 31,
#  'ab': 121,
#  'ac': 89,
#  'ad': 67,
#  'ae': 39,
#  'af': 42,
#  ...
#  }


while ip < len(lines):
    # parse the line and create a list of command
    command = re.findall(r'\w+', data[ip])
    run_command(command)
    ip = ip + 1  # update the instruction pointer


# Interpreter code
# while "exit" not in command:
#     print("\n>>>", end=' ')
#     print(stack)
#     print(variable)
#     print(vmemeory)
#     command = str(input())
#     command = re.findall(r'\w+', command)
#     run_command(command)
```

There is some problem in loading the value of the variable to stack because some time the variable name is used other time the value so i did some hacky code to circumvent and made all the line containing store and other operand to two lines , Also we need to remove any comments , and the jump location should not have any other instruction

the `.bash_history` file gives a hint how to use the command and the expected output

    echo "sandflea" | python3 interpreter.py
	

	flag-8b3e356d468f01daa7


