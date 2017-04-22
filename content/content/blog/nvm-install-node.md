+++
Tags = ["nodejs","npm", "cookbook"]
date = "2017-02-23T18:58:08+01:00"
title = "Installing node with NVM"

+++

This is more of a recipe for myself, as I always have problems with npm. I'm
usually stuborn and refuse to use a globally installed nodejs, and can't be
really bothered to properly install a nodejs tarball distribution, with setting
up PATH and all. They're usually throw-away and not portable between my
machines.

So, a simple recipe to install nodejs on my own setup, an ArchLinux
machine using fish as default shell.

First, install nvm using instructions from the NVM page: https://github.com/creationix/nvm

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
```

This plugs NVM into .bashrc and makes it available for bash, but I use fish. In
bash I ran ``nvm install 6.10.0``, which is the latest LTS release.

Next, in fish I run ``omf install nvm``. This installs the nvm fish plugin
(assumes OMF is installed) and now it is possible to run npm commands (in a new
fish shell). For example, ``npm install http-server``. Notice this is a local
install, it will create a ``node_modules`` folder in the current location and
will install the executable scripts as, for example,
``node_modules/.bin/http-server``.

Installing with -g (globally) will make the executable script available from
``.nvm/versions/6.10.0/bin/http-server``. NVM takes care of setting up proper
$PATH, so ``http-server`` will be available from any location.
