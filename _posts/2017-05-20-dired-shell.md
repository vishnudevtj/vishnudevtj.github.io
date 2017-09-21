---
title: Dired shell Wizadry 
updated: 2017-06-07 01:19:17
---

- [Dired Shell Command Wizadry](#org705d59e)


<a id="org705d59e"></a>

# Dired Shell Command Wizadry

Once again Dired , `dired-do-shell-command` ! Runs shell COMMAND on all the marked files parallel , if no marked file current file is used To run the COMMAND Asynchronously we can do `dired-do-async-shell-command` & or end the ! prompt with & If there is a ‘\*’ in COMMAND, surrounded by whitespace, this runs COMMAND just once with the entire file list substituted there.

If there is no ‘\*’, but there is a ‘?’ in COMMAND, surrounded by whitespace, this runs COMMAND on each file individually with the file name substituted for ‘?’.

when COMMAND ends in ‘;’ or ‘;&’ then COMMANDs are executed in the background on each file sequentially waiting for each COMMAND to terminate before running the next COMMAND.

So to Compress many files just mark the file and fire ! with `tar cvgf <archive name> *`

[1.Emacs Manual](https://www.gnu.org/software/emacs/manual/html_node/emacs/Shell-Commands-in-Dired.html)
