# /etc/bashrc

# System wide functions and aliases
# Environment stuff goes in /etc/profile

# It's NOT a good idea to change this file unless you know what you
# are doing. It's much better to create a custom.sh shell script in
# /etc/profile.d/ to make custom changes to your environment, as this
# will prevent the need for merging in future updates.

# Prevent doublesourcing
STIME=$(date +%H-%M-%S)
#echo $PATH | tr ':' '\n' | sort  | cat -n > /tmp/${STIME}-start-etc-bashrc
if [ -z "$BASHRCSOURCED" ]; then
  BASHRCSOURCED="Y"

SHELL_NAME=$(printf $SHELL | awk -F'/' '{print $NF}')
    # Turn on parallel history
    shopt -s histappend
    history -a
    # Turn on checkwinsize
    shopt -s checkwinsize
    [ "$PS1" = "\\s-\\v\\\$ " ] && PS1="[\u@\h \w]\\$ "
    # You might want to have e.g. tty in prompt (e.g. more virtual machines)
    # and console windows
    # If you want to do so, just add e.g.
    # if [ "$PS1" ]; then
    #   PS1="[\u@\h:\l \W]\\$ "
    # fi
    # to your custom modification shell script in /etc/profile.d/ directory

  if ! shopt -q login_shell ; then # We're not a login shell
    # Need to redefine pathmunge, it gets undefined at the end of /etc/profile
    pathmunge () {
        case ":${PATH}:" in
            *:"$1":*)
                ;;
            *)
                if [ "$2" = "after" ] ; then
                    PATH=$PATH:$1
                else
                    PATH=$1:$PATH
                fi
        esac
    }

    # By default, we want umask to get set. This sets it for non-login shell.
    # Current threshold for system reserved uid/gids is 200
    # You could check uidgid reservation validity in
    # /usr/share/doc/setup-*/uidgid file
    if [ $UID -gt 199 ] && [ "`id -gn`" = "`id -un`" ]; then
       umask 002
    else
       umask 022
    fi

    SHELL=/bin/bash
    # dash is the default sh 
    # no need to bother with interactive or not
    for i in /etc/profile.d/*.sh; do
	    . "$i"
    done

    unset i
    unset -f pathmunge
  fi

fi

# no duplication
HISTCONTROL=ignoreboth
shopt -s histappend
export HISTSIZE=5000
export HISTFILESIZE=5000
#echo $PATH | tr ':' '\n' | sort  | cat -n > /tmp/${STIME}-end-etc-bashrc

# vim:ts=4:sw=4
