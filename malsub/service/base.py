from abc import ABCMeta, abstractmethod
from inspect import signature

from malsub.common import out, rw
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.meta import DATA_PATH, SAMPLE_PATH
from malsub.core import web


class Unsupported(Exception):
    pass


class Singleton:
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class MetaAbstract(ABCMeta):
    def __new__(cls, clsname, base, dict):
        for method_name in dict:
            method = dict[method_name]
            for cls_base in base:
                try:
                    method_base = getattr(cls_base, method_name)
                    if callable(method_base):
                        sigc, sigp = signature(method), signature(method_base)
                        if sigp != sigc:
                            out.error(f"class \"{clsname}\" has mismatching "
                                      f"method signatures for "
                                      f"\"{method_name}{sigc}\" "
                                      f"(should be \"{method_name}{sigp}\")")
                except AttributeError as a:
                    continue
        return super(MetaAbstract, cls).__new__(cls, clsname, base, dict)


MetaMix = type('MetaMix', (Singleton, MetaAbstract), {})


class Service(metaclass=MetaMix):
    __api_dowf = "api_dowf"
    __api_repf = "api_repf"
    __api_subf = "api_subf"

    __api_repa = "api_repa"
    __api_repd = "api_repd"
    __api_repi = "api_repi"

    __api_repu = "api_repu"
    __api_subu = "api_subu"

    __api_srch = "api_srch"
    __api_quot = "api_quot"

    __attr = ["api_keyl", "desc", "name", "sname", "subs", 'url']
    __apiattr = [__api_dowf, __api_subf, __api_repf,
                 __api_repa, __api_repd, __api_repi,
                 __api_subu, __api_repu,
                 __api_srch, __api_quot]

    __apikey = None

    def __init__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        from sys import modules
        from os.path import basename
        for api in cls.__apiattr + cls.__attr:
            serv = f"class \"{cls.__name__}\" " \
                   f"<class '{cls.__module__}.{cls.__name__}'> in " \
                   f"\"{basename(modules[cls.__module__].__file__)}\""
            if not hasattr(cls, api) or callable(getattr(cls, api)):
                out.error(f"{serv} has missing or callable attribute \"{api}\"")
            if api in cls.__apiattr:
                apispec = getattr(cls, api)
                if apispec.__class__ != APISpec:
                    out.error(f"{serv} has malformed attribute \"{api}\" "
                              f"of \"{apispec.__class__}\" "
                              f"(should be of \"{APISpec}\")")
        return super().__init_subclass__(**kwargs)

    def __repr__(self):
        return f"<object {__name__}.{__class__.__name__}>"

    def __subclasshook__(cls, C):
        return NotImplemented

    @abstractmethod
    def download_file(self, hash: Hash):
        pass

    @abstractmethod
    def report_file(self, hash: Hash):
        pass

    @abstractmethod
    def submit_file(self, file: File):
        pass

    @abstractmethod
    def report_app(self, hash: Hash):
        pass

    @abstractmethod
    def report_dom(self, dom: str):
        pass

    @abstractmethod
    def report_ip(self, ip: str):
        pass

    @abstractmethod
    def report_url(self, url: str):
        pass

    @abstractmethod
    def submit_url(self, url: str):
        pass

    @abstractmethod
    def search(self, srch: str):
        pass

    @abstractmethod
    def quota(self):
        pass

    @classmethod
    def set_apikey(cls, apikey: dict):
        # cls.__apikey = APIKey(**apikey)
        # if not (regex.ishex(cls.__apikey.key) and len(cls.__apikey.key) == cls.api_keyl):
        # 	out.error(f"class {cls} has an invalid API key \"{apikey}\"")
        cls.__apikey = APIKey(**apikey)

    @classmethod
    def get_apikey(cls, key=False, user=False):
        if cls.__apikey:
            if key and user:
                return cls.__apikey.key, cls.__apikey.user
            elif key:
                return cls.__apikey.key
            return cls.__apikey.apikey
        return {}

    @classmethod
    def get_apifn(cls):
        return [api for api in cls.__fnmap.keys()]

    @classmethod
    def test_api(cls, apifn: str):
        fn = getattr(cls(), apifn)
        if hasattr(fn, UNSUPPORTED):
            raise Unsupported
        if apifn == DOWNLOAD_FILE:
            # empty: d41d8cd98f00b204e9800998ecf8427e
            fn(Hash("e24b91383aa2547f23bfe2c500e2d2f4"))
        elif apifn == REPORT_FILE:
            fn(Hash("e24b91383aa2547f23bfe2c500e2d2f4"))
        elif apifn == SUBMIT_FILE:
            fn(File(SAMPLE_PATH))
        elif apifn == REPORT_APP:
            fn(Hash("9B6AEA1992775510CB9014AD6860D146"))
        elif apifn == REPORT_DOM:
            # ovh.de
            fn("myjino.ru")
        elif apifn == REPORT_IP:
            # AS16276, 213.186.33.0 - 213.186.33.255, OVH SAS
            fn("213.186.33.1")
        elif apifn == REPORT_URL:
            fn("http://muazymaur.tk/maurice/bot.exe")
        elif apifn == SUBMIT_URL:
            fn("http://muazymaur.tk/maurice/bot.exe")
        elif apifn == SEARCH:
            fn("plugx")
        elif apifn == QUOTA:
            fn()
        # get a symbolic return value from fn and print after success
        return f"\"{apifn}\" success"

    @classmethod
    def help(cls):
        fn = [fn for fn in cls.__fn if
              not hasattr(getattr(cls, fn), UNSUPPORTED)]
        return [cls.desc, cls.subs, cls.url, ",".join(fn)]

    @staticmethod
    def unsupported(fn):
        setattr(fn, UNSUPPORTED, True)
        return fn

    @staticmethod
    def unused(cls):
        setattr(cls, UNUSED, True)
        return cls

    __fn = [download_file.__name__,
            report_file.__name__,
            submit_file.__name__,
            report_app.__name__,
            report_dom.__name__,
            report_ip.__name__,
            report_url.__name__,
            submit_url.__name__,
            search.__name__,
            quota.__name__]

    __fnmap = dict(zip(__fn, __apiattr))
    # __fnmap = {download_file.__name__: __api_dowf,
    #            report_file.__name__: __api_repf,
    #            submit_file.__name__: __api_subf,
    #            report_app.__name__: __api_repa,
    #            report_dom.__name__: __api_repd,
    #            report_ip.__name__: __api_repi,
    #            report_url.__name__: __api_repu,
    #            submit_url.__name__: __api_subu,
    #            search.__name__: __api_srch,
    #            quota.__name__: __api_quot}


class APIKey:
    kt = "apikey"
    ut = "user"

    def __init__(self, **kwargs):
        self.apikey = {}
        if kwargs.get(APIKey.kt):
            self.keyt = next(iter(kwargs.get(APIKey.kt)))
            self.key = kwargs[APIKey.kt][self.keyt]
            self.apikey[self.keyt] = self.key
        if kwargs.get(APIKey.ut):
            self.usert = next(iter(kwargs.get(APIKey.ut)))
            self.user = kwargs[APIKey.ut][self.usert]
            self.apikey[self.usert] = self.user


class APISpec:
    def __init__(self, method="", url="", uri="", cert=None):
        self.method = web.parse_method(method) if method else method
        self.url = web.parse_url(url) if url else url
        self.uri = web.parse_uri(uri) if uri else uri
        self.fullurl = self.url + self.uri
        self.fulluri = self.fullurl
        if cert:
            self.verify = DATA_PATH + cert \
                if type(cert) is str and rw.tryf(DATA_PATH + cert) else True
        else:
            self.verify = False if cert == False else True
        self.auth = None
        self.cookie = None
        self.data = None
        self.file = None
        self.header = None
        self.json = None
        self.param = None

    def __str__(self):
        return f"{self.method} {self.fulluri} {self.verify} \n" \
               f"{self.auth} {self.cookie} {self.data} {self.file} {self.header} " \
               f"{self.param}"


UNUSED = "_unused"
UNSUPPORTED = "_unsupported"

DOWNLOAD_FILE = Service.download_file.__name__
REPORT_FILE = Service.report_file.__name__
SUBMIT_FILE = Service.submit_file.__name__
REPORT_APP = Service.report_app.__name__
REPORT_DOM = Service.report_dom.__name__
REPORT_IP = Service.report_ip.__name__
REPORT_URL = Service.report_url.__name__
SUBMIT_URL = Service.submit_url.__name__
SEARCH = Service.search.__name__
QUOTA = Service.quota.__name__
TEST_API = Service.test_api.__name__
