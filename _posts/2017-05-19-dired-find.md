---
title: Dired Find
updated: 2017-06-07 01:22:50
tags: emacs
---
- [find dired](#org14f9434)


<a id="org14f9434"></a>

# find dired

we can run a find command in dired and get the list in a dired buffer with `find-dired` . it can be useful sometimes to make find specific files and preform dired magic on it . while running it it turns out that the the command takes argument from us and run

```shell
find . \(arg\) -ls
```

the `-ls` arg prints the result in ls format but the spaces and `` `unusaul` `` things are escaped and while running wdired it did not recognized those escapes and failed the documentation of find-dired `c-h f ret find-dired` says that there is a find-ls-option variable that specifies the find options going to customization and setting the ls option to `-print0 | xargs -0 ls -la` prints the find in better format and now we can use wdired
