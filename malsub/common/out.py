from sys import stdout, stderr
from pprint import PrettyPrinter

from malsub.core import color


class log:
    ast = "[*]"
    plus = "[+]"
    minus = "[-]"
    excl = "[!]"
    quest = "[?]"

    input = "input"

    debug = "debug"
    verb = "verbose"
    info = "info"
    warn = "warning"
    error = "error"


LEVEL = log.info

__pp = PrettyPrinter(indent=2)


def time():
    """
    formats the current time down to microsecond resolution with timezone information
    """
    # from time import localtime, strftime
    from datetime import datetime
    # + strftime("%z %Z", localtime())
    return datetime.utcnow().strftime("%a %d %b %Y %H:%M:%S.%f +0000 UTC")


def msg(m, symb, lvl, c, cbu, file=stdout, trail="", end="\n"):
    """
    prints the current time and a colored message
    """
    if trail: trail = ", " + trail
    # n = 55
    print(f"{c(symb)} {cbu(lvl):>18} {time()}{cbu(':')} {m}{trail}", file=file,
          end=end)


def pformat(obj):
    return __pp.pformat(obj)


def input(m):
    """
    prints a gray-colored input message
    """
    msg(m, log.minus, log.input, color.gray, color.grayb, end="")


def inquest(m):
    """
    prints a gray-colored input message
    """
    msg(m, log.quest, log.input, color.gray, color.grayb, end="")


def debug(m, obj=None):
    """
    prints a blue-colored debug message
    :return: int
    """

    def wrap(obj):
        # if type(obj.__repr__()) is str:
        if isinstance(obj.__repr__(), str):
            return obj
        else:
            return wrap(obj.__repr__())

    if LEVEL == log.debug:
        if obj:
            m = f"{m} --\n{pformat(wrap(obj))}"
        msg(m, log.ast, log.debug, color.blue, color.blueb)


def verb(m):
    """
    prints a blue-colored verbose message
    """
    if LEVEL == log.verb or LEVEL == log.debug:
        msg(m, log.ast, log.verb, color.blue, color.blueb)


def info(m):
    """
    prints a green-colored informational message
    """
    msg(m, log.plus, log.info, color.green, color.greenb)


def warn(m):
    """
    prints a yellow-colored warning message
    """
    msg(m, log.excl, log.warn, color.yellow, color.yellowb)


def error(m):
    """
    prints a red-colored error message and exits
    """
    msg(m, log.excl, log.error, color.red, color.redb, file=stdout, trail="")
    # print("\n" + printable_usage(__doc__))
    exit(1)
