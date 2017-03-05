from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, quoteurl, openurl
from malsub.common import out, rw, frmt


class PhishTank(Service):
    name = "PhishTank"
    sname = "pt"
    api_keyl = 64

    api_dowf = APISpec("GET", "http://data.phishtank.com", "/data/%s/online-valid.json.gz")
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec("POST", "http://checkurl.phishtank.com", "/checkurl/")
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # http://www.phishtank.com/developer_info.php

    def download_file(self, hash: Hash):
        self.api_dowf.fulluri = self.api_dowf.fullurl % self.get_apikey(
            key=True)
        data, filename = request(self.api_dowf, bin=True)
        if filename:
            rw.writef("phishtank-" + filename, data)
            return f"downloaded \"phishtank-{filename}\""
        else:
            return "unsuccess"

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
        pass

    @Service.unsupported
    def report_ip(self, ip: str):
        pass

    def report_url(self, url: str):
        self.api_repu.data = {"url": quoteurl(url), "format": "json",
                              **self.get_apikey()}
        data, _ = request(self.api_repu)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    @Service.unsupported
    def quota(self):
        pass
