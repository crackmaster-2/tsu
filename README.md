## tsu tsudo

[![Build Status](https://travis-ci.org/cswl/tsu.png?branch=master)](https://travis-ci.org/cswl/tsu)

```
A su and sudo wrapper for Termux.
```

`tsu` (like tsu as in tsunami, you know ) is an su wrapper for the
terminal emulator and packages for Android, Termux.

`tsu` will focus only on dropping into root shell from termux.  
In order to run one off commands as root use `tsudo` command which acts like `sudo` .

### Installation

`tsu` is now available as a termux package. Install it like any other package with.

```
pkg install tsu
```

### Background

Termux relies on LD_LIBRARY_PATH enviroment variables to find it's libraries.
For security reasons some environent variables seem to be reset by su, unless
an --preserve-environent flag is passed.  
tsu handles this for you and also launches your preferred shell.  
su by default will use sh or mksh, depending upon how it is on your device.

### Contributing

Know something you wanna add/improve, you're more than welcome to open a issue or create a pull request.  
The README was written in a hurry, so some help here too.

### License

Licensed under the ISC license. See [LICENSE](https://github.com/cswl/tsu/blob/master/LICENSE.md).
