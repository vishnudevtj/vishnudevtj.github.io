---
title:  Emacs Spelling
updated: 2017-09-21 14:42:59
---


- [Spell check in Emacs](#orge6d34dd)


<a id="orge6d34dd"></a>

# Spell check in Emacs

Writing blogs and other documents i make spelling mistakes , one thing i am not that good at spelling and other they are due to my typing , to rectify this i use emacs flyspell mode with flyspell-correct-ivy . flyspell underlines all the wrong entries and i use the ivy to correct it . It is a smooth workflow

```emacs-lisp
(use-package flyspell-correct-ivy
  :ensure t
  :config
  (define-key flyspell-mode-map (kbd "C-c C-;") 'flyspell-correct-previous-word-generic)
  )
```

