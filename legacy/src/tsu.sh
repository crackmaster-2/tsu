#!/data/data/com.termux/files/usr/bin/sh

# Copyright (c) 2016, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the ISC Liscense.
# https://github.com/cswl/tsu/blob/master/LICENSE.md

show_usage() { 
  cat << EOF
  #SHOW_USAGE_BLOCK
EOF
}

# Defaults in Termux and Android
TERMUX_FS="/data/data/com.termux/files/"
TERMUX_PREFIX="$TERMUX_FS/usr"
TERMUX_PATHS="$TERMUX_PREFIX/bin:$TERMUX_PREFIX=/bin/applets"
ROOT_HOME="/data/data/com.termux/files/root"
ANDROIDSYSTEM_PATHS="/system/bin:/system/xbin"

# Long options
IOPTS="$1"
if [ "$IOPTS" = "--help" ]; then
  show_usage
  exit 0
fi;

# Short command options
# TODO: Validate command line arguments
while getopts ':apeush' opt; do
  case $opt in
    a)
      shift $((OPTIND - 1))
      APPEND_SYSTEM_PATH=1
      ;;
    p)
      shift $((OPTIND - 1))
      PREPEND_SYSTEM_PATH=1
      ;;
    e)
      shift $((OPTIND - 1))
      SETUP_ENV=1
      ;;
    u)
      shift $((OPTIND - 1))
      TSU_USER_MODE=1
      ;;
    s)
      shift $((OPTIND - 1))
      ALT_SHELL="$OPTARG"
      ;;
    h)
      show_usage
      exit
      ;;
    *)
      echo "Unknown option -$OPTARG" 2>&1
      exit 1
      ;;
  esac
done

env_path_helper() {
  if [ "x$APPEND_SYSTEM_PATH" = "x1" ] && [ "x$PREPEND_SYSTEM_PATH" = "x1" ]; then
    printf -- "-a and -p can't be both specifice at once.! \n"
    printf -- "Run 'tsu -h' or 'tsu --help' for help \n"
    exit 1
  elif [ "x$APPEND_SYSTEM_PATH"  = "x1" ] ; then
    # Append path
    PATH="$PATH:$ANDROIDSYSTEM_PATH"
    # Prepend path
  elif [ "x$PREPEND_SYSTEM_PATH" = "x1" ]; then
    PATH="$ANDROIDSYSTEM_PATH:$PATH"
  fi
}

root_shell_helper() {
  # Select shell
if [ -n "$USER_SHELL" ]; then
   # Expand //usr/ to /usr/
    USER_SHELL_EXPANDED=$(echo "$USER_SHELL" | sed "s|^//usr/|$TERMUX_PREFIX/|")
    ROOT_SHELL="$USER_SHELL_EXPANDED"
elif [ "$USER_SHELL" = "system" ]; then
    ROOT_SHELL="/system/bin/sh"
  # Check if user has set a login shell
elif test -x "$HOME/.termux/shell"; then
    ROOT_SHELL="$(readlink -f -- "$HOME/.termux/shell")"
    # Or at least installed bash
elif test -x "$PREFIX/bin/bash"; then
    ROOT_SHELL="$PREFIX/bin/bash"
    # Oh well fallback to 
else
    ROOT_SHELL="$PREFIX/bin/ash"
fi
}

env_path_helper
root_shell_helper

if [ -e "/sbin/magisk" ]; then
  # Handle F**kin Magisk
  # Tested on Magisk Version 18.0
    unset LD_LIBRARY_PATH
    unset LD_PRELOAD
    exec /sbin/magisk.bin "su" "$PREFIX/usr/lib/libtsu-magisk.sh" 
else
  # Using the -c option of su allows to pass enviroment variables
  for SU_BINARY in '/su/bin/su' '/sbin/su' '/system/xbin/su' '/system/bin/su'; do
    if [ -e "$s" ]; then
      exec "$SU_BINARY" --preserve-environment -c "LD_LIBRARY_PATH=$LD_LIBRARY_PATH PATH=$PATH $ROOT_SHELL"
    fi
  done
fi
 
  # We didnt find any su binary
  printf -- "No superuser binary detected. \n"
  printf -- "Are you rooted? \n"
  exit 1
