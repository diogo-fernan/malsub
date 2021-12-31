from os import path, stat
from os.path import isfile

from malsub.common.rw import openf
from malsub.core.crypto import md5, sha256


class File:
    def __init__(self, file):
        # test for compression

        self.name = path.basename(file)
        self.pname = file
        self.fdl = []
        # try except ... for "stat"
        self.len = stat(file).st_size
        self.md5 = md5(file)
        self.sha256 = sha256(file)

    def fd(self):
        fd = openf(self.pname)
        self.fdl += [fd]
        return fd

    def __repr__(self):
        return f'<object {__name__}.{__class__.__name__} "{self.name}">'

    def __str__(self):
        return f"{self.name} ({self.md5})"


def new(*files):
    return [File(f) for f in files if isfile(f)]


def close(*files):
    for f in files:
        if type(f) is File:
            for fd in f.fdl:
                close(fd)
