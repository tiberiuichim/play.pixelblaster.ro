+++
Tags = ["Linux","ArchLinux", "Cookbook"]
date = "2017-04-27T20:15:15+03:00"
title = "How I broke my archlinux and fixed it"

+++
Today, new lesson learnt. I needed to test something with Internet Explorer and
Edge, so I've downloaded the test images from the Microsoft website, then
proceeded to install virtualbox, in my current KDE based ArchLinux desktop
(which I love a lot). A simple ``pacman -S virtualbox`` perhaps? Yes, except...

After installing virtualbox, it complained about some missing libssl2.0.0
lib... so I thought maybe I don't have that installed? I didn't really research
it, just installed openssl. Can't hurt, right? even if it's already installed.
And now ``sudo`` won't work anymore. I knew I f'ed up but then I proceeded to
reboot. All this while going through a lot of chaos: organising some work,
talking to product managers, etc. I really didn't need a machine down on its
knees.

Of course, it didn't boot. After several unsuccessful tries, I managed to fix
it. The problem was, as any ArchLinux user could tell you, that **You should
always run pacman -Syu before installing any package**. There was a problem
with running docker after a system upgrade (I think it may still be the case?)
so I generally avoided doing the upgrade dance. When I've installed openssl,
basically I've upgraded to a new major version and broke all software that
linked to it. May have been bad timing, it looks like.

The solution is to boot from the Antergos live disk and run, as root:

```
pacman --root /mnt/arch -Syu
```

Which should work, in theory, except that my upgrade size was too big and
didn't fit in the *live root* of the Antergos. After upgrading all the affected
libraries, I could then run a mount on proc, sys and dev, chroot to the mounted
hardisk and run pacman -Syu just like normal.
