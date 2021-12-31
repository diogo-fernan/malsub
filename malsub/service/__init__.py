from os.path import basename, dirname
from sys import modules
from pkgutil import iter_modules
from importlib import import_module
from inspect import getfile

from malsub.common import out
from malsub.core import serv as service
from malsub.service import base

for module_loader, name, ispkg in iter_modules([dirname(__file__)]):
    import_module("." + name, __package__)

serv = service.ServiceList()
out.debug("base.Service.__subclasses__", obj=base.Service.__subclasses__())
for cls in base.Service.__subclasses__():
    if cls.__module__ in modules:
        if not hasattr(cls, base.UNUSED):
            s = f'class "{cls.__name__}" {cls} in ' f'"{basename(getfile(cls))}"'
            try:
                cls()
            except Exception as e:
                out.error(s + f" does not implement all abstract methods: {e}")
            else:
                out.debug(s + " valid")
                serv += service.Service(cls)

if not serv:
    out.error("no valid services implemented")

try:
    del (
        cls,
        basename,
        dirname,
        getfile,
        iter_modules,
        import_module,
        module_loader,
        modules,
        name,
        ispkg,
        s,
    )
except:
    pass
