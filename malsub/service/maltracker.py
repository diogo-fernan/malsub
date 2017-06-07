from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, frmt, rw


class Maltracker(Service):
    name = "maltracker"
    sname = "mt"
    api_keyl = 64

    desc = f"{name} is a proprietary sanboxed environment created by\n" \
           f"AnubisNetworks for dynamic analysis incorporating threat\n" \
           f"intelligence"
    subs = "public"
    url = "https://maltracker.net/"

    api_dowf = APISpec("GET", "http://api.maltracker.net:4700", "/sample/get/")
    # /report/min/get/ # /sample/info/
    api_repf = APISpec("GET", "http://api.maltracker.net:4700", "/report/get/")
    api_subf = APISpec("POST", "http://api.maltracker.net:4700", "/task/submit/file/")

    api_repa = APISpec()
    api_repd = APISpec("GET", "http://api.maltracker.net:4700", "/c2/domain/")
    api_repi = APISpec("GET", "http://api.maltracker.net:4700", "/c2/ip/")

    api_repu = APISpec("GET", "http://api.maltracker.net:4700", "/report/get/")
    api_subu = APISpec("POST", "http://api.maltracker.net:4700", "/task/submit/url/")

    api_srch = APISpec()
    api_quot = APISpec()

    # https://maltracker.net/static/docs/usage/api.html

    def download_file(self, hash: Hash):
        self.api_dowf.fulluri = self.api_dowf.fullurl + hash.hash
        self.api_dowf.param = self.get_apikey()
        try:
            data, filename = request(self.api_dowf, bin=True)
            # out.debug(util.hexdump(data))
            if not filename:
                filename = hash.hash
            rw.writef(filename, data)
            return f"downloaded \"{filename}\""
        except Exception as e:
            return f"sample not found: {e}"


    def report_file(self, hash: Hash):
        self.api_repf.fulluri = self.api_repf.fullurl + hash.hash
        self.api_repf.param = self.get_apikey()
        data, _ = request(self.api_repf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def submit_file(self, file: File):
        self.api_subf.data = self.get_apikey()
        self.api_subf.file = {"file": (file.name, file.fd())}
        data, _ = request(self.api_subf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.fulluri = self.api_repd.fullurl + dom
        self.api_repd.param = self.get_apikey()
        data, _ = request(self.api_repd)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        return out.pformat(data)

    def report_ip(self, ip: str):
        self.api_repi.fulluri = self.api_repi.fullurl + ip
        self.api_repi.param = self.get_apikey()
        data, _ = request(self.api_repi)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        return out.pformat(data)

    @Service.unsupported
    def report_url(self, url: str):
        # URL report works with hash values
        # use 'report_file'
        # or... compute the hash value of the URL here
        # and make the request
        pass

    def submit_url(self, url: str):
        self.api_subu.data = {"url": url, **self.get_apikey()}
        data, _ = request(self.api_subu)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        return out.pformat(data)

    @Service.unsupported
    def search(self, srch: str):
        pass

    @Service.unsupported
    def quota(self):
        pass
