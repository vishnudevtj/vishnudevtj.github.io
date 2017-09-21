---
title: Neatplaylist
updated: 2017-06-07 00:51:42
---

- [NeatPlayList](#orga6a3ae2)


<a id="orga6a3ae2"></a>

# NeatPlayList

Best thing about linux is that we are the true masters of our machine we can make it do what we want not what it offers . I listen to music with mplayer and i would like to remove music which i dislike . As we know everything in unix is file every process has a process id and information related to it is located in process id folder under proc

```shell
ls -la /proc/`pgrep mplayer`
```

    total 0
    dr-xr-xr-x   9 root root 0 Jun  6 22:53 .
    dr-xr-xr-x 224 root root 0 Jun  6 08:09 ..
    dr-xr-xr-x   2 root root 0 Jun  6 23:48 attr
    -rw-r--r--   1 root root 0 Jun  6 23:48 autogroup
    -r--------   1 root root 0 Jun  6 23:48 auxv
    -r--r--r--   1 root root 0 Jun  6 23:48 cgroup
    --w-------   1 root root 0 Jun  6 23:48 clear_refs
    -r--r--r--   1 root root 0 Jun  6 22:53 cmdline
    -rw-r--r--   1 root root 0 Jun  6 23:48 comm
    -rw-r--r--   1 root root 0 Jun  6 23:48 coredump_filter
    -r--r--r--   1 root root 0 Jun  6 23:48 cpuset
    lrwxrwxrwx   1 root root 0 Jun  6 23:48 cwd -> /media/root/74F7-1BFD/Music/English
    -r--------   1 root root 0 Jun  6 23:48 environ
    lrwxrwxrwx   1 root root 0 Jun  6 22:53 exe -> /usr/bin/mplayer
    dr-x------   2 root root 0 Jun  6 22:53 fd
    dr-x------   2 root root 0 Jun  6 23:48 fdinfo
    -rw-r--r--   1 root root 0 Jun  6 23:48 gid_map
    -r--------   1 root root 0 Jun  6 23:48 io
    -r--r--r--   1 root root 0 Jun  6 23:48 limits
    -rw-r--r--   1 root root 0 Jun  6 23:48 loginuid
    dr-x------   2 root root 0 Jun  6 23:48 map_files
    -r--r--r--   1 root root 0 Jun  6 23:48 maps
    -rw-------   1 root root 0 Jun  6 23:48 mem
    -r--r--r--   1 root root 0 Jun  6 23:48 mountinfo
    -r--r--r--   1 root root 0 Jun  6 23:48 mounts
    -r--------   1 root root 0 Jun  6 23:48 mountstats
    dr-xr-xr-x   5 root root 0 Jun  6 23:48 net
    dr-x--x--x   2 root root 0 Jun  6 23:48 ns
    -r--r--r--   1 root root 0 Jun  6 23:48 numa_maps
    -rw-r--r--   1 root root 0 Jun  6 23:48 oom_adj
    -r--r--r--   1 root root 0 Jun  6 23:48 oom_score
    -rw-r--r--   1 root root 0 Jun  6 23:48 oom_score_adj
    -r--------   1 root root 0 Jun  6 23:48 pagemap
    -r--------   1 root root 0 Jun  6 23:48 personality
    -rw-r--r--   1 root root 0 Jun  6 23:48 projid_map
    lrwxrwxrwx   1 root root 0 Jun  6 23:48 root -> /
    -rw-r--r--   1 root root 0 Jun  6 23:48 sched
    -r--r--r--   1 root root 0 Jun  6 23:48 schedstat
    -r--r--r--   1 root root 0 Jun  6 23:48 sessionid
    -rw-r--r--   1 root root 0 Jun  6 23:48 setgroups
    -r--r--r--   1 root root 0 Jun  6 23:48 smaps
    -r--------   1 root root 0 Jun  6 23:48 stack
    -r--r--r--   1 root root 0 Jun  6 23:30 stat
    -r--r--r--   1 root root 0 Jun  6 23:48 statm
    -r--r--r--   1 root root 0 Jun  6 22:53 status
    -r--------   1 root root 0 Jun  6 23:48 syscall
    dr-xr-xr-x   4 root root 0 Jun  6 23:48 task
    -r--r--r--   1 root root 0 Jun  6 23:48 timers
    -rw-rw-rw-   1 root root 0 Jun  6 23:48 timerslack_ns
    -rw-r--r--   1 root root 0 Jun  6 23:48 uid_map
    -r--r--r--   1 root root 0 Jun  6 23:48 wchan

pgrep is the grep for process returns the pid id of the process

top and other monitoring tool use this folder to get information about a process the fd folder contains the links to the file descriptors

```shell
ls -la /proc/`pgrep mplayer`/fd
```

    total 0
    dr-x------ 2 root root  0 Jun  6 22:53 .
    dr-xr-xr-x 9 root root  0 Jun  6 22:53 ..
    lrwx------ 1 root root 64 Jun  6 23:51 0 -> /dev/pts/3
    lrwx------ 1 root root 64 Jun  6 23:51 1 -> /dev/pts/3
    lrwx------ 1 root root 64 Jun  6 23:51 2 -> /dev/pts/3
    lrwx------ 1 root root 64 Jun  6 23:51 3 -> socket:[254239]
    lr-x------ 1 root root 64 Jun  6 22:53 4 -> /media/root/74F7-1BFD/Music/English/69 Ed Sheeran - Sing.mp3
    lr-x------ 1 root root 64 Jun  6 23:51 5 -> pipe:[301484]
    l-wx------ 1 root root 64 Jun  6 23:51 6 -> pipe:[301484]
    lrwx------ 1 root root 64 Jun  6 23:51 7 -> anon_inode:[eventfd]
    lrwx------ 1 root root 64 Jun  6 23:51 8 -> socket:[301487]
    lrwx------ 1 root root 64 Jun  6 23:51 9 -> anon_inode:[eventfd]

The 4 Th file descriptor contains the link to the current playing files

```shell
readlink /proc/`pgrep mplayer`/fd/4
```

    /media/root/74F7-1BFD/Music/English/69 Ed Sheeran - Sing.mp3

Now Just remove the file

```shell
rm "`readlink /proc/$(pgrep mplayer)/fd/4`"
```

We can put this code in a shell script file which is located in the PATH and assign a keyboard shortcut to remove the current music mplayer is is playing.

