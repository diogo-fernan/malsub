from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt, rw


@Service.unused
class Deepviz(Service):
    name = "deepviz"
    sname = "dv"
    api_keyl = 64

    api_dowf = APISpec("POST", "https://api.deepviz.com", "/sandbox/sample")
    api_repf = APISpec("POST", "https://api.deepviz.com", "/general/report")
    api_subf = APISpec("POST", "https://api.deepviz.com", "/sandbox/submit")

    api_repa = APISpec()
    api_repd = APISpec("POST", "https://api.deepviz.com", "/intel/network/domain")
    api_repi = APISpec("POST", "https://api.deepviz.com", "/intel/network/ip")

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec("POST", "https://api.deepviz.com", "/intel/search")
    api_quot = APISpec()

    # https://api.deepviz.com/
    # https://www.deepviz.com/apidocs
    # https://github.com/saferbytes/python-deepviz

    def download_file(self, hash: Hash):
        self.api_dowf.data = {hash.alg: hash.hash, **self.get_apikey()}
        data, filename = request(self.api_dowf, bin=True)
        # out.debug(util.hexdump(data))
        if filename:
            rw.writef(filename, data)
            return f"downloaded \"{filename}\""
        else:
            return "unsuccess"

    def report_file(self, hash: Hash):
        self.api_repf.data = {hash.alg: hash.hash, **self.get_apikey()}
        data, _ = request(self.api_repf)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def submit_file(self, file: File):
        self.api_subf.data = self.get_apikey()
        self.api_subf.file = {"file": file.fd()}
        data, _ = request(self.api_repf)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.data = {"domain": dom, **self.get_apikey()}
        data, _ = request(self.api_repd)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    def report_ip(self, ip: str):
        self.api_repd.data = {"ip": ip, **self.get_apikey()}
        data, _ = request(self.api_repd)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    def search(self, srch: str):
        self.api_repd.data = {"string": srch, **self.get_apikey()}
        data, _ = request(self.api_repd)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
