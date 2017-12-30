---
title: Org Search Engine
updated: 2017-06-08 23:29:03
tags: [emacs, org-mode]
---

- [Org Search Engine](#org34fa60d)


<a id="org34fa60d"></a>

# Org Search Engine

Trying find a way to rapidly search my org notes and find what i want , i found out that org agenda can be used as a search engine. setting `org-agenda-file` to a directory it searches thought the directory to find all the org file and adds them , But my notes are scatters in different folders , found this piece of code which works wonderfully

```emacs-lisp
(add-hook 'org-agenda-mode-hook (lambda ()
                                  (setq org-agenda-files
                                        (mapcar 'abbreviate-file-name
                                                (split-string
                                                 (shell-command-to-string "find ~/Dropbox/org -name \"*.org\"")
                                                 "\n")))))
```

1.[Org agenda as search engine](http://orgmode.org/worg/org-tutorials/advanced-searching.html) 

2.[Multiple Direcory agenda ](https://lists.gnu.org/archive/html/emacs-orgmode/2014-04/msg00465.html) 
