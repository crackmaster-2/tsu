# Copyright (c) 2019, Cswl Coldwind <cswl1337@gmail.com
# This software is licensed under the MIT Liscense.
# https://github.com/cswl/tsu/blob/v3.x/LICENSE-MIT

import subprocess
import re

from pathlib import Path
from collections import deque

from . import consts

import consolejs
import tsu

class SuExec:
    FOUND = 1
    NONEXIST = -10
    UNSUPP = -20
    ABANDONED = -50
    
    def __init__(self, su):
        self.su = su

    
    def argv_builder(self, su_path, shell, usern):
        su = self.su
        
        argv = deque([su.argmap["shell"], shell])

        init = su.argmap.get("init", False)
        if init:
            argv.appendleft(init)
        if usern:
            argv.append(usern)

        argv.appendleft(su_path)
        
        to_list = list(argv)
        return to_list

    def call_su(self, usern, shell, env=None):

        console =  consolejs.get_console(tsu)
        su = self.su
        su_path = su.lpath()
        
        argv = self.argv_builder(su_path, shell, usern)
    
        console.debug("Calling {su_path=} with {usern=} {argv=} and with enviroment")
        if env:
            console.dir(env)
        linux_execve(argv, env=env)
        return True

    def vercmp(self):
        console =  consolejs.get_console(tsu)
        su = self.su 
        name = su.name
        su_path = su.lpath()
        checkver = [su_path] + su.veropt
        if self.su.abandoned:
            return False
        try:
            ver = subprocess.check_output(checkver).decode("utf-8")
            console.debug(r" {name=} {ver=}")
            found = SuExec.FOUND if su.verstring in ver else SuExec.UNSUPP
            return found
        except FileNotFoundError:
            return SuExec.NONEXIST
        except PermissionError:
            return SuExec.NONEXIST 


def linux_execve(args, env=None):
    subprocess.run(args, env=env)
