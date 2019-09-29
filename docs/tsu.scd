tsu(1)

# NAME                                                 

tsu - A su wrapper for Termux.                                                        
# SYNOPSIS

*tsu* [  -s SHELL | -p | -e ]

tsu by default will try to launch an interactive shell.
The interactive shell is searched as follows:

- User's chosen shell in *$HOME/.termux/shell*
- The *bash* shell if installed
- The default installed *sh* shell from termux


If you need to start another shell. See the -s option

# OPTIONS

*-s [</path/to/shell>]*
   Use an alternate specified shell.  `//usr` is expanded to $PREFIX.
   For convience, if the path starts by `//usr` it will be expaned to Termux's $PREFIX,
   which is the usr directory of Termux.
   So -s '//usr/bin/bash' will be, "/data/data/com.termux/files/usr/bin/bash"

*-p*
    Prepend /system/bin and /system/xbin to PATH.
    So that binaries in /system/bin and /system/xbin/bash will be
    prefrred over the ones provided by termux.
    Sometimes you may want to run the system binaries as root from Termux.
    Or for cases, where some scripts might expect behavior from the
    default Android toolbox, busybox.

*-e*
    Setup up some enviroment variables as when in Termux.
    This adds some default Termux variables, when you wanna run Termux commands from other places like
    adb shell.
    Currently it sets HOME to Termux's home, and adds Termux's bin to PATH, following the -p option.


