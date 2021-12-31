import sys, os


class asciic:
    soh = "\x01"
    sot = "\x02"
    esc = "\x1b"


class code:
    """
    styles and bright foreground colors
    """

    end = 0
    bold = 1
    underline = 4

    gray = 90
    red = 91
    green = 92
    yellow = 93
    blue = 94
    magenta = 95
    cyan = 96
    black = 97


def color(string, color, bold=False, underline=False):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return str(string)
    bu = ""
    if bold:
        bu = code.bold
    elif underline:
        bu = code.underline
    return f"{asciic.esc}" \
           f"[{bu};{color}m{string}{asciic.esc}" \
           f"[{code.end}m"  # fmt: skip


def bold(string):
    return color(string, code.bold)


def gray(string):
    return color(string, code.gray)


def grayb(string):
    return color(string, code.gray, bold=True)


def grayu(string):
    return color(string, code.gray, underline=True)


def red(string):
    return color(string, code.red)


def redb(string):
    return color(string, code.red, bold=True)


def redu(string):
    return color(string, code.red, underline=True)


def green(string):
    return color(string, code.green)


def greenb(string):
    return color(string, code.green, bold=True)


def greenu(string):
    return color(string, code.green, underline=True)


def yellow(string):
    return color(string, code.yellow)


def yellowb(string):
    return color(string, code.yellow, bold=True)


def yellowu(string):
    return color(string, code.yellow, underline=True)


def blue(string):
    return color(string, code.blue)


def blueb(string):
    return color(string, code.blue, bold=True)


def blueu(string):
    return color(string, code.blue, underline=True)


def magenta(string):
    return color(string, code.magenta)


def magentab(string):
    return color(string, code.magenta, bold=True)


def magentau(string):
    return color(string, code.magenta, underline=True)


def cyan(string):
    return color(string, code.cyan)


def cyanb(string):
    return color(string, code.cyan, bold=True)


def cyanu(string):
    return color(string, code.cyan, underline=True)


def black(string):
    return color(string, code.black)


def blackb(string):
    return color(string, code.black, bold=True)


def blacku(string):
    return color(string, code.black, underline=True)
