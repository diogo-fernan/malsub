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
            s = f"class \"{cls.__name__}\" {cls} in " \
                f"\"{basename(getfile(cls))}\""
            try:
                cls()
            except Exception as e:
                out.error(s + f" does not implement all abstract methods: {e}")
            else:
                out.debug(s + " valid")
                serv += service.Service(cls)
            # serv[cls.__name__.lower()] = (cls.__name__.lower(), cls)
            # serv[cls.sname.lower()] = (cls.__name__.lower(), cls)

if not serv:
    out.error("no valid services implemented")

try:
    del cls, basename, dirname, getfile, \
        iter_modules, import_module, module_loader, modules, \
        name, ispkg, s
except:
    pass

# from os import listdir
# from os.path import dirname, isfile, join
#
# from malsub.service import base
#
# path = dirname(base.__file__)
#
# # __all__ = ["malwr", "virustotal", "base"]
# __all__ = [f[:-3] for f in listdir(path) if
# 		   isfile(join(path, f)) and f.endswith(".py") and not f.endswith("__init__.py")]
#
# from importlib import import_module
# import_module("malwr", "malsub.service")
#
# del path, dirname, isfile, join, listdir

# from glob import glob
# mod = glob(dirname("service/__init__.py") + "/*.py")
# __all__ = [basename(i)[:-3] for i in mod if isfile(i) and not i.endswith("__init__.py") and not i.endswith("base.py")]

# pkg = __import__("service", fromlist=["*"])
# print(pkg.__all__)
# for m in pkg.__all__:
# 	m = getattr(pkg, m)
# 	# print(m, type(m), dir(m))
# 	for i, j in [(n, c) for n, c in m.__dict__.items() if
# 				 isinstance(c, type) and not n == "Service" and issubclass(c, Service)]:
# 		__all__ += [n]


# def parse():
#	# http://stackoverflow.com/questions/22119850/get-all-class-names-in-a-python-package
# 	from importlib import import_module, invalidate_caches
# 	from inspect import getmembers, isclass
# 	import pprint
# 	invalidate_caches()
# 	pkg = import_module("malsub.service")
# 	invalidate_caches()
# 	pprint.pprint(pkg); print(dir(pkg))
# 	pprint.pprint([getattr(pkg, i) for i in pkg.__all__])
# 	pprint.pprint([getmembers(getattr(pkg, i), isclass) for i in pkg.__all__ if i != "service"])
#
# 	# pkg = __import__("malsub.service", fromlist=["*"])
# 	# mod = getattr(pkg, mod)
# 	mod = [mod for mod in pkg.__all__ if mod != "service"]
# 	clsignore = [ABC, abstractproperty, apiattr, absattr, Singleton]
# 	svc = []
#
# 	for m in mod:
# 		try:
# 			import_module(m, "malsub.service")
# 		except:
# 			pass
# 		else:
# 			pass
# 			for name, cls in [(n, c) for n, c in getmembers(getattr(pkg, m), isclass) if c not in clsignore]:
# 			# for name, cls in [(n, c) for n, c in m.__dict__.items() if isinstance(c, type) and c not in clsignore]:
# 				s = f"class \"{name}\" <class 'malsub.service.{cls.__module__}.{name}'> in \"{basename(m.__file__)}\""
# 				if name != Service.__name__ and issubclass(cls, Service):
# 					try:
# 						cls()
# 					except:
# 						out.warn(s + " does not implement all abstract methods")
# 					else:
# 						out.debug(s + " valid")
# 						if m.__name__ not in svc:
# 							svc += [m.__name__]
# 				else:
# 					if not cls == Service:
# 						out.debug(s + " not valid, ignoring")
# 	if not svc:
# 		out.error(f"package \"{pkg.__package__}\" has invalid classes")
# 	print(__import__("malsub.service", fromlist=svc))
# 	print(svc)
# 	return {}
