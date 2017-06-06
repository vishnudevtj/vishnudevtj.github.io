---
title: Emacs Secracy
updated: 2017-06-07 01:12:52
---
- [Emacs Secracy !](#org919e458)


<a id="org919e458"></a>

# Emacs Secracy !

Making emacs secret keper : emacs have EasyPG which is a emacs interface for managing GnuPG .

```emacs-lisp
(require 'epa-file)
(epa-file-enable)
```

Now Emacs encrypt and decrypt all files with extention .gpg When you save the encrypted file it asks for the key , this can be avoided by setting a local variable for file

```emacs-lisp
-*- epa-file-encrypt-to: ("your@email.address") -*-
```

Now we just add this to our journal and change the journal.org to journal.org.gpg , That makes our jounal encrypted for good reasons. To encrypt a file add the above line and save the file as a .gpg and you are good to go We can also encrypt a region with `epa-encrypt-region`

    
    -----BEGIN PGP MESSAGE-----
    
    hQIMA+qb7jBQs/VOAQ/9GIOFm5levIZdvVyOlmFVFkqdr12vtdicFVc0gJax0RZf
    yxpUxnjb6on2P+geN+CXvkLqWq+Yw9Dd8xI5vYP1P5cSN0SmBzKp6AOObC+s8Ntx
    ISxPdjUUcE3io7fpGhW5vn8STnybl/bAaeBLoVuNRsPNpBM+1v7ilYv73iAL7cu0
    Rc4E/upd/rswvV7uBX8N8YW0XJKIvw4Ym5JUnsqJ1M+81KwkWwm1lk1SlstNjVk+
    0mBYT2CkUrAyPnpzD4oy50K6GVabN4Cg/BwYOPq5elKDQHI0/CNkTfQSetsbEH/H
    qc3GphUlwr+DMLXDYfUH2tlaX8ivmU/EJHrYE+M281j2KwiIM9lyOw7pMXxKCMwv
    BMAkHum5+dx6SdFXDMskoUiNTGuFTKABu/XFxMPyud1oot42Dahtl9BQls21OjK9
    tpvitNywo8HT1ItkInjrVGSOI9thO/NgZ54fiNKdBKR22135Ohi2TpdBzlBz0aNR
    rmYiN7in2M+H63h/HQUKAZlFOUeY12k7wv6lbRtsUxzyEGj+K8jYE6APpm1jQzfO
    VIENgC4gvjEMaip3R1dY6cjELIBf6RX+5vMGbjlMJojGJ99ksQxgV5QHXG3bBPkF
    NpwoXcOeiSUq6vCWdHjOr1lea/MoDOoXoxm5bW5ob798nv4R2CY6x/K7iifD6vbS
    RwGQGRXoD3VqzITsnzp/pDPxRjD4NNsR7vvlJo6gAMfBlFO6uqEHXCr2NIn11aPD
    /wj2OcmdUQCqWCuKbkhHkWSkJWcoI1QC
    =n4dU
    -----END PGP MESSAGE-----

to decrypt select the region and call `epa-decrypt-region` it replaces the plain text in there

Mark all the files in dired and call `epa-dired-do-encrypt` to encrypt all the files

There is also a Org-Crypt This enable to encrypt all the org having a specific tag such as `crypt` to automaticaly encrypt

```emacs-lisp
(require 'org-crypt)
(org-crypt-use-before-save-magic)
(setq org-tags-exclude-from-inheritance (quote ("crypt")))

(setq org-crypt-key nil)
  ;; GPG key to use for encryption
  ;; Either the Key ID or set to nil to use symmetric encryption.

(setq auto-save-default nil)
```

This sets up org-crypt with tag crypt This is very convinient if we only weant to encrypt only a section of a org file

Encrypt Eveything!! Emacs Rocks!!

