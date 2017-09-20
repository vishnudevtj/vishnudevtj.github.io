---
title:  Assembly In Emacs
updated: 2017-09-20 14:41:10
---

- [Assembly in Emacs](#org64830af)


<a id="org64830af"></a>

# Assembly in Emacs

Learning Assembly is esseential to Reverse Enginner among other stuffs , Well I write my code in Emacs and emacs defaultly contans a asm mode which helps in Assemlby programming , But i need documentaion in my finger tip , someting like company mode which is really helpfull while coding . This is emacs isn't the might be some code lieing in the internet which will help , So i Searched the internet and with no surprice there is a package for x86 Documents called [x86-lookup](https://github.com/skeeto/x86-lookup) , it opens the intel developer manual in a document viewer or in emacs's pdf viewer . It basically works by first converting the pdf to text and indexing it and later seaces the index and opens up the correct page . Same author have made a [nasm mode](https://github.com/skeeto/nasm-mode) for nasm programming .

```emacs-lisp
(use-package x86-lookup
  :ensure t
  :config
  (setq  x86-lookup-pdf "~/Dropbox/Books/Hacking/64-iA32-Instruction-set-reference-vol2.pdf")
  )
(use-package nasm-mode
  :ensure t
  :config
  (add-hook 'asm-mode-hook 'nasm-mode)
  )
```

Dependencies :

```sh
sudo apt install poppler-utils
```

![img](/assets/img/Assembly in Emacs/screenshot_2017-09-20_14-51-12.png)

Footnote :

[1. x86lookup](https://github.com/skeeto/x86-lookup)

[2. Author's Blog](http://nullprogram.com/blog/2015/11/21/)

[3. Nasm Mode Autho's Blog](http://nullprogram.com/blog/2015/04/19/)

[4. Intel® 64 and IA-32 Architectures Software Developer Manuals](https://software.intel.com/en-us/articles/intel-sdm)
