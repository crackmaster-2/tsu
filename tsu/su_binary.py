from pathlib import Path, PosixPath

import attr
import typing
from . import consts


@attr.s(auto_attribs=True)
class SuBinary:
    name: str
    path: str
    verstring: str
    veropt: list
    argmap: dict
    multipath: typing.List[str] = None
    abandoned: bool = None

    def cpath(self):
        """
    Returns a string of path to a concrete path
        """
        if not self.multipath:
            return PosixPath(self.path)
