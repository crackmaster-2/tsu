from tsu.su_binary import SuBinary


class MagiskSU:
    binary = SuBinary(
        name="MAGISK",
        argmap={"init": "su", "shell": "-s"},
        verstring=r"MAGISKSU",
        veropt=["su", "--version"],
        path="/sbin/magisk",
    )

    @classmethod
    def get_env(cls, p):
        pass


class LineageSU:

    binary = SuBinary(
        name="MAGISK",
        argmap={"shell": "-s"},
        verstring=r"cm-su",
        veropt=["--version"],
        path="/system/xbin/su",
    )


class ChainSU:
    binary = SuBinary(
        name="CHSU",
        argmap={"shell": "-s"},
        verstring=r"SUPERSU",
        veropt=["--version"],
        multipath=["/su/bin/su", ("/sbin/su"), ("/system/xbin/su")],
        path="",
    )
