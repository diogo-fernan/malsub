from base64 import b64encode
from hashlib import new

from malsub.common import rw, regex

__buf = 2 ** 16  # 65536

HASH_MD5 = "md5"
HASH_SHA1 = "sha1"
HASH_SHA256 = "sha256"
HASH_SHA512 = "sha512"

__md5 = 128
__sha1 = 160
__sha256 = 256
__sha512 = 512

__hash = {__md5: HASH_MD5,
          __sha1: HASH_SHA1,
          __sha256: HASH_SHA256,
          __sha512: HASH_SHA512}


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
    return __hash.get(len(string) / 2 * 8)  # if ishash(string) else "unknown"


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


def md5(file):
    return hashf("md5", file)


def sha256(file):
    return hashf("sha256", file)
