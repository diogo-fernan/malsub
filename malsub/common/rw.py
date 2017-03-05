from malsub.common import out
from malsub.core.meta import DOWNL_PATH


def tryf(file):
    try:
        with open(file, 'rb') as fd:
            out.debug(f"file \"{file}\" valid")
    except:
        out.error(f"cannot open file \"{file}\"")
    return True


def openf(file, mode='rb', debug=True):
    try:
        fd = open(file, mode)
        if debug:
            out.debug(f"file \"{file}\" valid")
        return fd
    except:
        out.error(f"cannot open file \"{file}\"")


def closef(fd):
    try:
        fd.close()
    except:
        pass


def writef(file, data, path=DOWNL_PATH):
    if type(data) is str:
        data = data.encode('utf-8')
    with openf(path + file, mode='wb') as fd:
        fd.write(data)


def yn(message):
    true = ["", "y", "yes"]
    false = ["n", "no"]
    c = None
    while c not in true and c not in false:
        out.inquest(message + ", continue? [y/n]: ")
        c = input().lower()
    if c in false:
        exit(0)
