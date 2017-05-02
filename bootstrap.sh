#!/bin/sh
HUGO="https://github.com/spf13/hugo/releases/download/v0.20.2/hugo_0.20.2_Linux-64bit.tar.gz"
curl -L $HUGO > /tmp/hugo.tgz
tar xzf /tmp/hugo.tgz
mkdir -p bin/
mv hugo_0.20.2_linux_amd64/hugo_0.20.2_linux_amd64 bin/hugo
