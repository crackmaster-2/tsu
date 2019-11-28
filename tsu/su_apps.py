import subprocess
import os
from collections import deque
from string import Template

import consolejs
from ruamel.yaml import YAML

import tsu
from tsu import consts
from tsu.execve import linux_execve
from tsu.su_binary import SuBinary
from tsu.su_defs import MagiskSU, LineageSU, ChainSU
from tsu.user_utils import is_other_user

# The order in which to check SuBinaries
SU_CHECK_ORDER = [MagiskSU, LineageSU, ChainSU]


yaml=YAML()   # default, if not specfied, is 'rt' (round-trip)

class EnvVars:  
    
    # Merges environment
    ENV_VARS = """
base: 
    copy: [EXTERNAL_STORAGE, LANG ,TERM, ANDROID_DATA, ANDROID_ROOT ]

other:
    rewrite: 
            HOME: "/"
            PATH: $syspath
    unset: [LD_PRELOAD, TMPDIR] 
"""
    
    def __init__(self, env_build, is_other):
        self.is_other = is_other
        self.prepend = env_build.get("prepend")
        self.clean = env_build.get("clean")
   
    @classmethod
    def merge_env(cls):
        """ Merges all new environment """
        console = consolejs.get_console(tsu)
        ts = Template(cls.ENV_VARS)
        s = ts.substitute(syspath= consts.ANDROIDSYSTEM_PATHS )

        ev = yaml.load(s)
        console.debug("{ev=}") 
        
        ## We get a new environemnt regardless of clean
        bcopy = ev.get("base").get("copy")
        built_env = { e : os.environ[e] for e in bcopy}

        orewrite = ev.get("other").get("rewrite")
        for k, v in orewrite.items():
            built_env[k] = v
        console.debug("{built_env=}")
        return built_env
        
    def make_env(self, prefix):
        console = consolejs.get_console(tsu)
        console.debug("{self.is_other=} {self.prepend=} {self.clean=}" )
        
        if self.is_other:
            new_env = self.merge_env()

        NEW_PATH = f"{prefix}/bin:${prefix}/bin/applets"
        # consts.ANDROIDSYSTEM_PATHS
        ENV_CLEAN_ROOT = {
            "HOME": "/data/data/com.termux/files/home/.root",
            "PATH": NEW_PATH,
            "PREFIX": f"{prefix}",
            "TMPDIR": f"{prefix}/root/.tmp",
        }
        return  new_env


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

    def set_user(self, usern, cur_uid):
        self.is_other = is_other_user(usern, cur_uid)
        self.usern = usern

    def call_su(self, usern, shell, env_build):

        console = consolejs.get_console(tsu)
        su_bin = self.su_bin
        su_path = str(self.su_path)
        
        argv = self.argv_builder(su_path, shell, usern)
        env_vars = EnvVars(env_build, self.is_other)
        env = env_vars.make_env(consts.TERMUX_PREFIX)

        console.debug("Calling {su_path=} with {usern=} {argv=} and with enviroment")
        if env:
            console.dir(env)
        linux_execve(su_path, argv, env)
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
    
    @classmethod
    def check(cls, su_app):
        su_exec = cls(su_app)
        result = su_exec.vercmp()
    
        if result == SuExec.FOUND:
            return (su_exec, None)
        elif result == SuExec.UNSUPP:
            return (None, consts.MSG_UNSUPPSU)
        elif result == SuExec.ABANDONED:
            return (None, consts.MSG_CHSUWARN)
        else:
            return (None, None)
    

# This is an aggreate function that tries all available SU Binaries
def SuCall(cur_uid, user, shell, env):
    # The caller should catch the exception
    # We just stop iterating when
    
    for su_app in SU_CHECK_ORDER:
        su_exec, reason = SuExec.check(su_app)
        if su_exec:
            su_exec.set_user(cur_uid, user)
            su_exec.call_su(user, shell, env)
        elif reason:
            raise SuExit(reason)

    # At this point, we have no su
    raise SuNotFound


