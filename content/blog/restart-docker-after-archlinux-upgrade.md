+++
Description = ""
Tags = ["cookbook","Linux"]
date = "2017-05-08T09:35:54+03:00"
title = "Restart docker after archlinux upgrade"

+++

My main reason for avoiding ArchLinux upgrades (``sudo pacman -Syu``) was
because I always needed to reboot my computer, to allow starting docker
services after the upgrade. Today, I found the solution is a simple:

```
systemctl daemon-reload
systemctl restart docker
```
