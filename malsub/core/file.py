from os import path, stat

from malsub.common.rw import openf, tryf
from malsub.core.crypto import md5, sha256


class File():
    def __init__(self, file):
        # test for compression

        self.name = path.basename(file)
        self.pname = file
        self.fdl = []
        # try except ... for "stat"
        self.len = stat(file).st_size
        self.md5 = md5(file)
        self.sha256 = sha256(file)
        # self.type = [pe, pdf, apk, ...]

    def fd(self):
        fd = openf(self.pname)
        self.fdl += [fd]
        return fd

    def __repr__(self):
        return f"<object {__name__}.{__class__.__name__} \"{self.name}\">"

    def __str__(self):
        return f"{self.name} ({self.md5})"


def new(*files):
    # return [File(f) for f in rw.filterff(*files)]
    # filel = []
    # for f in files:
    # 	if tryf(f):
    # 		filel += [File(f)]
    # return filel
    return [File(f) for f in files]


def close(*files):
    # return rw.closeff(*[f.fd for f in files if type(f) is File])
    for f in files:
        if type(f) is File:
            for fd in f.fdl:
                close(fd)
