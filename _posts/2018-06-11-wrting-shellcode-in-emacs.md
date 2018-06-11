---
title:  Wrting Shellcode In Emacs
updated: 2018-06-11 21:12:45
tags: [emacs,binary]
---

- [Org babel interface for rasm2](#org5127c4e)


<a id="org5127c4e"></a>

# Org babel interface for rasm2

rasm2 comes with the r2 and is used as assembler and disassembler . It support many architecture and provided a simple api . While developing exploit and writing shellcode a tool to assemble instruction is very use full . There are many online tools which provide a interface to assemble instruction but we need a offline solution . We can use rasm2 directly but there is no fun in it . It would be awesome if we can interface with the tool within emacs .

Org mode have a feature called [babel](https://orgmode.org/worg/org-contrib/babel/intro.html) , using this feature we can embed code blocks in org files . It is very power full feature and is used to write literate programs . Since this is emacs we can make it do anything we want .

examining ob-sed.el file which contains all the function used for the execution of `sed` source block gives .

```emacs-lisp
(defun org-babel-execute:sed (body params)
  "Execute a block of sed code with Org Babel.
BODY is the source inside a sed source block and PARAMS is an
association list over the source block configurations.  This
function is called by `org-babel-execute-src-block'."

```

The above function will be called when `org-babel-execute-src-block` function is executed over the sed source block , the first argument contains the body of the source block and the second is a association list over the configuration option . The result of this function will be printed on the org file . So we just need to write a function to call rasm2 shell command with correct argument .

```emacs-lisp
(require 'ob)

(defconst org-babel-header-args:rasm2
  '((:arch . :any)
    (:bits  . :any)
    (:disasm . :any)
    )
  "Rasm2 specific header arguments.")


(defun org-babel-execute:rasm2 (body params)
  "Execute a block code with Org Babel.
BODY is the source inside the source block and PARAMS is an
association list over the source block configurations.  This
function is called by `org-babel-execute-src-block'."

  (let* ((arch (cdr (assq :arch params)))
	 (bits (cdr (assq :bits params))))
    (if  (assq :disasm params)
	(shell-command-to-string
	 (concat "rasm2 -a  " arch " -b " (number-to-string bits) " -d \"" body "\"" ))
      (with-temp-buffer
	(insert (shell-command-to-string
		 (concat "rasm2 -C -a " arch " -b " (number-to-string bits) " \"" body "\"" )))
	(goto-char (point-min))
	(while (re-search-forward "\"" nil t )
	  (replace-match ""))
	(goto-char (point-min))
	(while (re-search-forward "\n" nil t )
	  (replace-match ""))
	(buffer-string)
	)))
  )
```

When rasm2 source block is evaluated this function will be called . Which then parses the configuration option and calls rasm2 with correct argument , the output is return to org file . We have added three header arguments which specifies the architecture , bits and whether to disassemble or not .

    
    #+BEGIN_SRC rasm2 :arch arm :bits 32
    add r1,r1,r2
    #+END_SRC
    
    #+RESULTS:
    : \x02\x10\x81\xe0
    
    #+BEGIN_SRC rasm2 :arch x86 :bits 32 :disasm
    9090
    #+END_SRC
    
    #+RESULTS:
    : nop
    : nop
