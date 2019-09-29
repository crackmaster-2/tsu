# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

from pathlib import Path
from collections import OrderedDict


# Defaults in Termux and Android
TERMUX_FS = "/data/data/com.termux/files/"
TERMUX_PREFIX = f"{TERMUX_FS}/usr"
TERMUX_PATHS = f"{TERMUX_PREFIX}/bin:{TERMUX_PREFIX}/bin/applets"
ROOT_HOME = "/data/data/com.termux/files/root"
SYS_SHELL = "/system/bin/sh"
ANDROIDSYSTEM_PATHS = "/system/bin:/system/xbin"

## Location of su binaries.
ROOT_UID = 0


### Help texts
CHSU_WARN = "SuperSU is abandonware. Consider upgrading your SuperUser Application."
