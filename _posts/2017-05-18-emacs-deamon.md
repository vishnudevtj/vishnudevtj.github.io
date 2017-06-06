---
title: Emacs Deamon
updated: 2017-06-07 01:28:07
---
[Making Emacs Super Fast](#orgddba24d)
- [Footnote:](#org5a895e1)

<a id="orgddba24d"></a>

# Making Emacs Super Fast

Adding Large number of packages can make emacs load slowly . this can be frustrating . We can be brillient and fine tune the nifty details and make it fast load time , but i have not reached that level . This is emacs there is allways better way

We can run emacs as a deamon and open file in it because it is already loaded it is superfast Using Systemd to start a emacs deamon

create a systemd service file ~/.config/systemd/user/emacs.service

```conf
[Unit]
Description=Emacs Daemon

[Service]
Type=forking
ExecStart=/usr/bin/emacs --daemon
ExecStop=/usr/bin/emacsclient --eval "(progn (setq kill-emacs-hook 'nil) (kill-emacs))"
Restart=always

[Install]
WantedBy=default.target
```

starting and enabling this service

```shell
systemctl --user start emacs.service   # Start emacs for the current session
systemctl --user enable emacs.service  # Enable emacs to be started at login
```

Desktop entry for emacs client

```conf
[Desktop Entry]
Name=Emacs Client
GenericName=Text Editor
Comment=Edit text
MimeType=text/english;text/plain;text/x-makefile;text/x-c++hdr;text/x-c++src;text/x-chdr;text/x-csrc;text/x-java;text/x-moc;text/x-pascal;text/x-tcl;text/x-tex;application/x-shellscript;text/x-c;text/x-c++;
Exec=emacsclient -c %f
Icon=emacs
Type=Application
Terminal=false
Categories=Utility;TextEditor;
```


<a id="org5a895e1"></a>

## Footnote:

[1.Using emacsclient to Speed up Editing](https://taingram.org/2017/05/09/using-emacsclient-to-speed-up-editing)

[2.Running emacs as a daemon with systemd](http://blog.refu.co/?p=1296)

