class Service:
    # http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    def __init__(self, cls):
        self.cls = cls
        self.obj = cls()
        self.name = cls.__name__
        self.namelo = cls.__name__.lower()
        self.sname = cls.sname
        self.snamelo = cls.sname.lower()
        self.fn = None
        self.fnname = None

    def setfn(self, fn):
        self.fn = getattr(self.obj, fn)
        self.fnname = self.fn.__name__

    def fnhasattr(self, attr):
        return hasattr(self.fn, attr)

    def __contains__(self, item):
        return item == self.namelo or item == self.snamelo

    def __gt__(self, other):
        return self.namelo > other

    def __lt__(self, other):
        return self.namelo < other

    def __eq__(self, other):
        return self.namelo == other or self.snamelo == other

    def __ne__(self, other):
        return self.namelo != other and self.snamelo != other

    def __repr__(self):
        return f"{self.cls} {self.name} {self.sname}"

    def __str__(self):
        return self.name


class ServiceList:
    def __init__(self, list=None):
        self.list = list if list is not None else []

    def setfn(self, fn):
        for s in self.list:
            s.setfn(fn)

    def __add__(self, other):
        # insert sort here
        # return ServiceList(self.list + [other])
        return ServiceList(sorted(self.list + [other]))

    def __iadd__(self, other):
        # insert sort here
        # self.list += [other]
        self.list = sorted(self.list + [other])
        return self

    def __bool__(self):
        return len(self.list) > 0

    def __contains__(self, item):
        return item in self.list

    def __getitem__(self, item):
        for s in self.list:
            if s == item:
                return s.obj

    def __setitem__(self, key, value):
        pass

    def __iter__(self):
        return iter(self.list)

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        # return repr(self.list)
        return self.list

    def __str__(self):
        return self.list
