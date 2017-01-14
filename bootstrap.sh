#!/bin/sh
type virtualenv >/dev/null 2>&1 || { echo >&2 "Needs virtualenv in PATH."; exit 1; }
virtualenv .
bin/pip install -r requirements.txt
curl https://github.com/spf13/hugo/releases/download/v0.18.1/hugo_0.18.1_Linux-64bit.tar.gz > /tmp/hugo.tgz
tar xzf /tmp/hugo.tgz
