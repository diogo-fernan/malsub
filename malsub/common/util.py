from shutil import get_terminal_size

__termwidth = get_terminal_size().columns


def trunc(string, width=None, sep=" (...) "):
    string = str(string)
    if not width:
        width = int(__termwidth * 0.60)
    if len(string) <= width:
        return string
    if width == len(sep):
        return sep
    dif = width - len(sep)
    dif1 = -(-dif // 2)  # ceil
    dif2 = dif - dif1
    return string[:dif1] + sep + ("", string[-dif2:])[dif2 > 0]


def hexdump(byte, offset=0x00, sep=".", width=16):
    from string import printable

    byte = bytearray(byte)
    dmp = ""
    for x in [byte[i : i + width] for i in range(len(byte)) if i % 16 == 0]:
        txt = ""
        dmp += "{:#08x}  ".format(offset)
        for i, j in enumerate(x):
            dmp += "{:02x} ".format(j)
            txt += (sep, chr(j))[chr(j) in printable[:-5]]
            if i == int(width / 2) - 1:
                dmp += " "
        dmp += " " * 3 * (width - i - 1) + " " + txt + "\n"
        offset += width
    return dmp


def asciibin(string):
    return " ".join("{:08b}".format(ord(i), "b") for i in string)


def rand01():
    return rand(0, 1)


def rand(min, max):
    from random import random, uniform

    return min + random() * (max - min)


def randc(min, max):
    from struct import Struct
    from random import randint

    imax = 2 ** (Struct("i").size * 8 - 1) - 1
    return min + randint(0, imax) % (max - min + 1)


def randint(min, max):
    return int(rand(min, max) // 1)
