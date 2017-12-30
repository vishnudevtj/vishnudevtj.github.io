---
title:  Web Browsing In Emacs
updated: 2017-09-18 15:54:21
tags: emacs
---



- [Compiling Emacs With Xwidget Support](#orgcfb084f)


<a id="orgcfb084f"></a>

# Compiling Emacs With Xwidget Support

Only time i need to get away from my Emacs is to browse , and now Emacs support to render Web page with GTK Webkit ! , For that we need to compile emacs from source with this feature enabled

Download the source and Unzip

Dependencies :

> 
> 
> libgif-devel libtiff-devel libjpeg-devel libxpm-devel libgnutls-devel libpng-devel libncurses-devel libgtk3-drivel libwebkitgtk3.0-devel

```sh
./configure --with-xwidgets
make
make install
```

This will Install emacs

![img](/assets/img/emacs-webbrowsing/screenshot_2017-09-18_15-49-01.png)

![img](/assets/img/emacs-webbrowsing/screenshot_2017-09-18_15-49-59.png)


Happy Browsing in Emacs !!

