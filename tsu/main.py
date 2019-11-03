# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import os
import sys

import os
import pwd
from pathlib import Path, PurePath

from docopt import docopt

import consolejs

import tsu
from tsu import consts
from tsu.su_apps import SuCall, SuExit, SuNotFound
from tsu.env_map import EnvMap

## Optimization strips docstring in build
USAGE = """
    tsu A su interface wrapper for Termux

    Usage:
        tsu
        tsu [ -s SHELL ]  [-pe] [USER]
        tsu --debug [ -s SHELL ]  [-pel] [USER]
        tsu -h | --help | --version


    Options:
    -s <shell>   Use an alternate specified shell.
    -l           Start a login shell.
    -p           Prepend system binaries to PATH
    -e           Start with a fresh environment.
    --debug      Output debugging information to stderr.
    -h --help    Show this screen.
    --version    Show version.

"""


def cli():

    args = docopt(USAGE)
    cur_uid = os.getuid()

    ### Debug handler
    debug_enabled = args["--debug"]

    # consolejs is a dynamic console logger for Python
    if debug_enabled:
        cjs = consolejs.create(tsu)

        cjs.level = consolejs.DEBUG
    else:
        cjs = consolejs.disabled()

    console = cjs.console
    console.dir(args)

    ### End Debug handler

    ### Setup Base Shell and Enviroment
    env_new = EnvMap(
        prepend=(args.get("-p")), clean=(args.get("-e")), usern=(args.get("USER"))
    )
    env_new.c_uid = cur_uid
    env_new.shell = args.get("-s")

    env = env_new.get_env()
    shell = env_new.get_shell()

    # Check `su` binaries:
    try:
        SuCall(args.get("USER"), shell, env)
    except SuExit as e:
        SystemExit(e.message)
    except SuNotFound:
        # At this point. there is no `su` binary
        print("No `su` binary not found.")
        print("Are you rooted? ")


## Handler for direct call
if __name__ == "__main__":
    cli()
