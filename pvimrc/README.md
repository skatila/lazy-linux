# vimrc set up specifically for my programming needs

VIM is perhaps the most extensible, customizable editor ever. It is my default go to when it comes to code. But, writing code is only a small subset of what I use for `vim`. I use it for everything - editing config files, viewing logs etc. It means that loading multiple plugins (generally meant for programming) everytime I run vim is a waste of time. So, it is only logical to have multiple vimrc.

A default, light weight vimrc that lives as `~/.vimrc`, barebones, limited.

And, a detailed, heavy weight vimrc that lives somewhere else.

Something like:

```
~/.pvim/pvimrc
```

And, alias declaration in my `.bashrc` with `alias pvim='vim -u ~/.pvim/pvimrc'`

This pvimrc can be your starter. Do as you will.

## TODO: add more mappings
