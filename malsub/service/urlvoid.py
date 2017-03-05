from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class URLVoid(Service):
    name = "URLVoid"
    sname = "uv"
    api_keyl = 40

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec("GET", "http://api.urlvoid.com", "/%s/%s/host/%s/")
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec("GET", "http://api.urlvoid.com", "/%s/%s/host/%s/scan/")
    # api_subu = APISpec("GET", "http://api.urlvoid.com", "/%s/%s/host/%s/rescan/")

    api_srch = APISpec()
    api_quot = APISpec("GET", "http://api.urlvoid.com", "/%s/%s/stats/remained/")

    # http://www.urlvoid.com/
    # http://www.urlvoid.com/api/
    # http://api.urlvoid.com/

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    @Service.unsupported
    def report_file(self, hash: Hash):
        pass

    @Service.unsupported
    def submit_file(self, file: File):
        pass

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    @Service.unsupported
    def report_dom(self, dom: str):
        self.api_repd.fulluri = self.api_repd.fullurl % \
                                (self.get_apikey()["identifier"],
                                 self.get_apikey()["apikey"], dom)
        data, _ = request(self.api_repd)
        return frmt.xmlparse(data)

    @Service.unsupported
    def report_ip(self, ip: str):
        pass

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        if url.startswith("http://"):
            url = url[7:]
        elif url.startswith("https://"):
            url = url[8:]
        self.api_subu.fulluri = self.api_subu.fullurl % \
                                (self.get_apikey()["identifier"],
                                 self.get_apikey()["apikey"], url)
        data, _ = request(self.api_subu)
        return frmt.xmlparse(data)

    @Service.unsupported
    def search(self, srch: str):
        pass

    def quota(self):
        self.api_quot.fulluri = self.api_quot.fullurl % (
        self.get_apikey()["identifier"], self.get_apikey()["apikey"])
        data, _ = request(self.api_quot)
        return frmt.xmlparse(data)
