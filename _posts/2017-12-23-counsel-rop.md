---
title:  Counsel Rop
updated: 2017-12-23 23:11:45
---




# Counsel rop

ROP chain in Binary Exploitation is a technique to bypass NX/DEP
security patch , what these protection do is that the make the memory
either writable or executable but not both . so injecting shellcode to
stack does not work . ROP Return Oriented Programming is a technique by
which we reuse the code which are there in the binary to exploit it , a
collection of assembly instruction which are there in the binary ending
with ret is called gadget , chaining these gadget that called the other
with ret we can recreate what the shellcode does and pwn it .

There are many tools to find these gadget , but we need to find a way to
integrate that to emacs because that is what we do .

With the help of the awesome package from abo-abo ie counsel and ivy we
can create an interface for ROPgadget which is a python program to find
gadget .

```emacs-lisp

(defun counsel-rop (arg)
  "ROP gadget Search for a bianry"
  (interactive "file name : ")
  (progn
    (setq buffer-name (concat (file-name-base arg ) "_gadgets"))
    (if (get-buffer buffer-name) ()
      (progn
    (shell-command (concat "ROPgadget " " --binary " arg) buffer-name)
    (with-current-buffer buffer-name 
      (bury-buffer))))
    (with-current-buffer buffer-name
      (setq cantidates (split-string (buffer-string) "\n" t))
      ))
  (ivy-read " Gadget : " cantidates
        :re-builder #'ivy--regex-fuzzy
        :action #'insert
        :caller 'counsel-rop
        ))
```

What the above code does is that it runs the program ROPgadget and
collects the output and writes it to a buffer with the name of the
binary then using ivy we search this buffer to find the required gadget
.

The ivy-read takes the given collection of strings and gives us a prompt
to select from that collection after the selection the function
specified in the action is called here it just inserted to buffer .

Before running the command it is checked that if the buffer exist if it
exist that is used otherwise a new buffer is created , this is help full
when dealing with large binary , we need not run the program every time
.

```emacs-lisp

(ivy-set-actions
 'counsel-rop
 '(("a" (lambda (x) (insert (car (split-string x "\:")))) "Insert Address")
   ("r" (lambda (x) (insert (cdr (split-string x "\:")))) "Insert Gadget"))
 )
```

ivy set action is special action that we can called with the selected
item , here we are using it to just insert the address if the gadget or
the code . this might be handy while documentation .




![img](/assets/img/rop-counsel/rop.gif)
