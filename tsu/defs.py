from .SuBinary import SuBinary

magisk = SuBinary(
    name="MAGISK",
    argmap={"init": "su", "shell": "-s"},
    verstring=r"MAGISKSU",
    veropt=["su", "--version"],
    path="/sbin/magisk",
)

losu = SuBinary(
    name="MAGISK",
    argmap={"shell": "-s"},
    verstring=r"cm-su",
    veropt=["--version"],
    path="/system/xbin/su",
)


chsu = SuBinary(
    name="CHSU",
    argmap={"shell": "-s"},
    verstring=r"SUPERSU",
    veropt=["--version"],
    multipath=["/su/bin/su", ("/sbin/su"), ("/system/xbin/su")],
    path="",
)
