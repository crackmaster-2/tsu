import consolejs
import subprocess
from collections import deque

import tsu
from tsu.exec import linux_execve
from tsu.su_binary import SuBinary
from tsu.su_defs import MagiskSU, LineageSU, ChainSU

# The order in which to check SuBinaries
SU_CHECK_ORDER = [MagiskSU, LineageSU, ChainSU]


# Custom named Exceptions
class SuExit(Exception):
    pass


class SuNotFound(Exception):
    pass


class SuExec:

    # Available states
    FOUND = 1
    NOT_FOUND = -10
    UNSUPPORTED = -20
    ABANDONED = -30
    NOT_EXSIST = -40

    def __init__(self, su_app):
        self.su_bin = su_app.binary
        self.su_path = su_app.binary.path
        self.su_cpath = su_app.binary.cpath()

    def argv_builder(self, su_path, shell, usern):
        """
        Builds argv for the exec function.
        
        su_path : passed in for tosting
        """
        su_bin = self.su_bin

        argv_dq = deque([su_path])

        init = su_bin.argmap.get("init", False)
        if init:
            argv_dq.append(init)

        if shell:
            argv_dq.append([su_bin.argmap["shell"], shell])

        if usern:
            argv_dq.append(usern)

        argv = list(argv_dq)
        return argv

    def call_su(self, argv, usern, shell, env=None):

        console = consolejs.get_console(tsu)
        su_bin = self.su_bin
        su_path = self.su_path

        argv = self.argv_builder(su_path, shell, usern)

        console.debug("Calling {su_path=} with {usern=} {argv=} and with enviroment")
        if env:
            console.dir(env)
        linux_execve(su_path, argv, env=env)
        return True

    def vercmp(self):
        console = consolejs.get_console(tsu)
        su_path = self.su_path
        su_cpath = self.su_cpath
        su_bin = self.su_bin
        su_name = su_bin.name

        checkver = [su_path] + su_bin.veropt
        if su_bin.abandoned:
            return SuExec.ABANDONED
        try:
            ver = subprocess.check_output(checkver).decode("utf-8")
            console.debug(r" {su_name=} {ver=}")
            found = SuExec.FOUND if su_bin.verstring in ver else SuExec.UNSUPPORTED
            return found
        # Both cases are when `su` isn't found
        except FileNotFoundError:
            return SuExec.NOT_FOUND
        except PermissionError:
            return SuExec.NOT_FOUND


# This is an aggreate function that tries all available SU Binaries
def SuCall(user, shell, env):
    # The caller should catch the exception
    # We just stop iterating when
    for su_app in SU_CHECK_ORDER:
        su_exec, reason = check_su(su_app)
        if su_exec:
            su_exec = SuExec(su_app)
            su_exec.call_su(user, shell, env)
        elif reason:
            raise SuExit(reason)

    # At this point, we have no su
    raise SuNotFound


def check_su(su_app):
    su_exec = SuExec(su_app)
    result = su_exec.vercmp()

    if result == SuExec.FOUND:
        return (su_exec, None)
    elif result == SuExec.UNSUPP:
        return (None, consts.MSG_UNSUPPSU)
    elif result == SuExec.ABANDONED:
        return (None, consts.MSG_CHSUWARN)
    else:
        return (None, None)
