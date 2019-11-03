# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import os
import sys


def linux_execve(path, argv, env=None):
    """ 
    Calls os.execve with the environent in *nix
    """
    ## Clean up stdout and close all files

    sys.stdout.flush()
    if env:
        os.execve(path, argv, env)
    else:
        os.execv(path, argv)
