from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class HybridAnalysis(Service):
    name = "Hybrid Analysis"
    sname = "ha"
    api_keyl = 25

    api_dowf = APISpec()
    api_repf = APISpec("GET", "https://www.hybrid-analysis.com", "/api/scan/%s")
    api_subf = APISpec("POST", "https://www.hybrid-analysis.com", "/api/submit")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec("GET", "https://www.hybrid-analysis.com", "/api/search")
    api_quot = APISpec("GET", "https://www.hybrid-analysis.com", "/api/quota")

    # https://www.hybrid-analysis.com/apikeys/info

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    def report_file(self, hash: Hash):
        self.api_repf.fulluri = self.api_repf.fullurl % hash.hash
        self.api_repf.param = self.get_apikey()
        data, _ = request(self.api_repf)
        return data

    @Service.unsupported
    def submit_file(self, file: File):
        self.api_subf.data = {"file": file.fd(), **self.get_apikey()}
        data, _ = request(self.api_subf)
        return data

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    @Service.unsupported
    def report_dom(self, dom: str):
        pass

    @Service.unsupported
    def report_ip(self, ip: str):
        pass

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    def search(self, srch: str):
        self.api_srch.param = {"query": srch, **self.get_apikey()}
        data, _ = request(self.api_srch)
        return data

    def quota(self):
        self.api_quot.param = self.get_apikey()
        data, _ = request(self.api_quot)
        return data
