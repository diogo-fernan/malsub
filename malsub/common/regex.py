from re import match, findall, fullmatch


def http_filename(string):
    return findall(r"filename=(\S+)", string)[0] if string else False


def ishex(string, base=2):
    from math import log
    # hex = '0123456789abcdefABCDEF'
    # return False if not string else \
    # 	all(c in hex for c in string) and \
    # 	not log(len(string), base) % 1 if base else True
    #  base ** log(len(string), base) // 1 == len(string)

    pat = r"\A" \
          r"[0-9a-fA-F]+" \
          r"\Z"
    # fr"[0-9a-f]{...}" \
    return False if not string else \
        True if fullmatch(pat, string) else \
            False and not log(len(string), base) % 1 if base else True


def isipaddr(string):
    pat = r"\A" \
          r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}" \
          r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" \
          r"\Z"
    return True if match(pat, string) else False


def isdomain(string):
    pat = r"\A" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"\Z"
    return False if not string else \
        True if fullmatch(pat, string) else False


def isfullurl(string):
    pat = r"\A" \
          r"(https?://)?" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"((/[0-9a-zA-Z?=_\-&%+.:]+)+)?" \
          r"/?" \
          r"\Z"
    return False if not string else \
        True if fullmatch(pat, string) else False


def isurl(string):
    pat = r"\A" \
          r"(https?://)?" \
          r"([0-9a-zA-Z-]+.)+[0-9a-zA-Z-]+" \
          r"\Z"
    return False if not string else \
        True if fullmatch(pat, string) else False


def isuri(string):
    pat = r"\A" \
          r"(/[0-9a-zA-Z?=_\-&%+.:]+)+" \
          r"/?" \
          r"\Z"
    return False if not string else \
        True if fullmatch(pat, string) else False
