from base64 import b64encode
from hashlib import new

from malsub.common import rw, regex

__buf = 2 ** 16  # 65536

__md5 = 128
__sha1 = 160
__sha256 = 256
__sha512 = 512

__hash = {__md5: "md5",
          __sha1: "sha1",
          __sha256: "sha256",
          __sha512: "sha512"}


class Hash:
    def __init__(self, string):
        self.hash = string
        self.alg = hashalg(string)

    def __str__(self):
        return f"{self.hash} ({self.alg})"


def base64(bytes):
    return b64encode(bytes)


def ishash(string):
    return regex.ishex(string, base=None) and len(string) / 2 * 8 in __hash


def hashalg(string):
    return __hash[len(string) / 2 * 8]  # if ishash(string) else "unknown"


def parse_hashl(*hash):
    hashl = []
    for h in hash:
        if ishash(h):
            # hashl += [h]
            hashl += [Hash(h)]
    return hashl


def hashf(alg, file):
    fd = rw.openf(file, debug=False)
    h = new(alg)
    while True:
        data = fd.read(__buf)
        if not data: break
        h.update(data)  # bytearray(data, 'utf-8')
    hex = h.hexdigest().lower()
    rw.closef(input)
    return hex


def md5(files):
    return hashf("md5", files)


def sha256(files):
    return hashf("sha256", files)
