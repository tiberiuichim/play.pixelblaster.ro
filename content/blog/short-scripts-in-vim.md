+++
Description = "A short review of how I edit scripts"
date = "2017-01-18T18:30:18+01:00"
title = "Editing Short python scripts with vim"
Tags = ["vim","programming","cookbook"]

+++
Being that I usually find interesting to know about other people's workflow,
here's a short description of my working environment that I typically use when
developing in Python:

## tmux

In the beginning I've used Yakuake tabs to split servers and files in separate
tabs. As the number grew, I've started naming the tabs (and even had a short
stint [extending](https://github.com/tiberiuichim/customkuake)
[Yakuake](https://github.com/tiberiuichim/atomic-hidpi) to fit this use case),
but as the number of projects and environments that I have to juggle kept
growing, I've resorted to splitting each separate tab into "subtabs", using
tmux.

I start `tmux -2` in each Yakuake tab (the `-2` switch is to enhance the color
support) and I've mapped the Alt+\ as the escape combination.
Why this? Backslash as the leader key comes from vim and I don't like the ctrl
key, I'd have to use my pinky finger and I don't like it. This is how to
achieve that:

```ini
 unbind C-b
 set -g prefix M-'\'
 bind M-'\' send-prefix
```

Next, to make it easier to switch tabs, I've mapped alt+<number> to switch to
the coresponding tab number.

```ini
 bind-key -n M-1 select-window -t:1
 bind-key -n M-2 select-window -t:2
 bind-key -n M-3 select-window -t:3
 bind-key -n M-4 select-window -t:4
 bind-key -n M-5 select-window -t:5
 bind-key -n M-6 select-window -t:6
 bind-key -n M-7 select-window -t:7
 bind-key -n M-8 select-window -t:8
 bind-key -n M-9 select-window -t:9
```

But one problem: the 0 key is far away. So I want to start tab numbering at 1:

```ini
 set -g base-index 1
 setw -g pane-base-index 1
```

## (Neo)Vim

Vim is the perfect editor for quick scripts: it is fast to start, very fast to
edit, easy to configure, etc. There's plenty of material on the web for this,
but two short tricks that are worth mentioning: ctrl+z is the easiest way to
escape from vim to the terminal (followed by fg to bring it back to the foreground)
and I sometimes type this (maybe I should even include it in my vimrc) to
execute the current file with the python from my virtualenv:

```viml
:map <f5> !python ./%<cr>
```
