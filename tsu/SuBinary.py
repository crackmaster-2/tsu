from pathlib import Path


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
    abandoned : bool = None
    

    def lpath(self):
        if not self.multipath:
            return Path(self.path)
