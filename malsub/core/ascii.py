from sys import modules

from malsub.common import color, out, util
from malsub.core import meta

try:
    from pyfiglet import figlet_format, Figlet
except:
    out.debug("\"pyfiglet\" import error, using ASCII art defaults")

_hline = f"   {meta.MALSUB_NAME} {meta.MALSUB_VERSION}\n"

# fmt: off
_default = [f"\n{_hline}\n  {util.asciibin(meta.MALSUB_NAME)}\n",
            f"""
                               _           _
                              | |         | |
               _ __ ___   __ _| |___ _   _| |__     +--+
              | '_ ` _ \ / _` | / __| | | | '_ \\   +--+|
              | | | | | | (_| | \__ \ |_| | |_) |  |  |+
              |_| |_| |_|\__,_|_|___/\__,_|_.__/   +--+
            """ + "\n" + _hline]

"""
    +------+
   /|     /|
  m------a |
  | u- ~ |-b
  |/     |/
  s------l

    +------+
   /|     /|
  +------+ |
  | +----|-+
  |/     |/
  +------+
""" 
# fmt: on


def banner():
    if "pyfiglet" in modules:
        f = Figlet().getFonts()
        bann = (
            "\n"
            + figlet_format(meta.MALSUB_NAME, font=f[util.randint(0, len(f))]).rstrip()
            + f"\n\n   {meta.MALSUB_NAME} {meta.MALSUB_VERSION}\n"
            f"   {meta.MALSUB_URL}\n"
        )
        bann = color.cyanb(bann)
    else:
        bann = color.cyanb(_default[util.randint(0, len(_default))])
    print(bann)
