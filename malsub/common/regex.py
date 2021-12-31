from re import match, findall, fullmatch


def http_filename(string):
    return findall(r"filename=(\S+)", string)[0] if string else False


def ishex(string, base=2):
    from math import log

    pat = r"\A" \
          r"[0-9a-fA-F]+" \
          r"\Z"  # fmt: skip
    return False if not string else \
        True if fullmatch(pat, string) else \
            False and not log(len(string), base) % 1 if base else True  # fmt: skip


def isipaddr(string):
    pat = r"\A" \
          r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}" \
          r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" \
          r"\Z"  # fmt: skip
    return True if match(pat, string) else False


def isdomain(string):
    pat = r"\A" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"\Z"  # fmt: skip
    return False if not string else \
        True if fullmatch(pat, string) else False  # fmt: skip


def isfullurl(string):
    pat = r"\A" \
          r"(https?://)?" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"((/[0-9a-zA-Z?=_\-&%+.:]+)+)?" \
          r"/?" \
          r"\Z"  # fmt: skip
    return False if not string else \
        True if fullmatch(pat, string) else False  # fmt: skip


def isurl(string):
    pat = r"\A" \
          r"(https?://)?" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"\Z"  # fmt: skip
    return False if not string else \
        True if fullmatch(pat, string) else False  # fmt: skip


def isuri(string):
    pat = r"\A" \
          r"(/[0-9a-zA-Z?=_\-&%+.:]+)+" \
          r"/?" \
          r"\Z"  # fmt: skip
    return False if not string else \
        True if fullmatch(pat, string) else False  # fmt: skip
