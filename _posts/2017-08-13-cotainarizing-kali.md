---
title:  Cotainarizing Kali
updated: 2017-08-13 21:13:34
tags: [note,linux]
---


- [Kali Docker Image](#org23276a7)


<a id="org23276a7"></a>

# Kali Docker Image

I require all the tools in Kali but could not install Kali as my Default os , There are two option one is Virtual Box running Kali another is Docker , I Like Docker because it uses less CPU Usage and it is more fun

Kali has provided a Official Docker image which can be pulled from docker hub

```sh
docker pull kalilinux/kali-linux-docker
```

Creating a Docker container as follows

```sh

docker run -it  \
-v ~/Docker/KaliLinux:/root \
-v ~/.bashrc:/home/root/.bashrc \
-v /etc/localtime:/etc/localtime \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=unix$DISPLAY \
-h "kali" \
--net host \
--device /dev/snd \
--name Kali \
kalilinux/kali-linux-docker

```

This command Creates a Docker container with name Kali

-v is used to mount a file from host

&#x2013;net host it shares the network from host

&#x2013;device /dev/snd to get sound

-e DISPLAY=unix$DISPLAY to get the GUI Working

This creates the container .

Container can be started with

```sh
docker start -a Kali
```

To run another command in the running container

```sh
docker exec -it "Kali" /bin/bash
```

This gives you another shell

    No protocol specified
    Unable to init server: Could not connect: Connection refused
    Error: cannot open display: :0

If this error occurs add root to the Xserver Access Control List

```sh
xhost +SI:localuser:root
```

Reference

1.  [Jessie Frazelle's Blog: Docker Containers on the Desktop](https://blog.jessfraz.com/post/docker-containers-on-the-desktop/)
2.  [Granting access to X server with xhost – /dev/blog](http://possiblelossofprecision.net/?p=896)
