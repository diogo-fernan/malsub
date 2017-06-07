from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class Metadefender(Service):
    name = "Metadefender"
    sname = "md"
    api_keyl = 32

    desc = f"{name} is a proprietary multi-scanning engine for malware,\n" \
           f"applications and IP addresses belonging to OPSWAT"
    subs = "public/private"
    url = "https://www.metadefender.com/"

    api_dowf = APISpec()
    # api_repf = APISpec("GET", "https://api.metadefender.com", "/v2/file/")
    api_repf = APISpec("GET", "https://api.metadefender.com", "/v2/hash/")
    api_subf = APISpec("POST", "https://scan.metadefender.com", "/v2/file")

    api_repa = APISpec("GET", "https://api.metadefender.com", "/v3/appinfo/")
    api_repd = APISpec()
    api_repi = APISpec("GET", "https://api.metadefender.com", "/v3/ip/")

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://www.metadefender.com/public-api

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    def report_file(self, hash: Hash):
        self.api_repf.header = self.get_apikey()
        self.api_repf.fulluri = self.api_repf.fullurl + hash.hash
        data, _ = request(self.api_repf)
        # data = frmt.jsontree(data)
        return out.pformat(data)

    def submit_file(self, file: File):
        self.api_subf.header = self.get_apikey()
        self.api_subf.file = {"file": file.fd()}
        data, _ = request(self.api_subf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_app(self, hash: Hash):
        self.api_repa.header = \
            {"Authorization":
                 " ".join(f"{kn} {k}" for kn, k in self.get_apikey().items())}
        self.api_repa.fulluri = self.api_repa.fullurl + hash.hash
        data, _ = request(self.api_repa)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_dom(self, dom: str):
        pass

    def report_ip(self, ip: str):
        self.api_repi.header = {
            "Authorization":
                " ".join(f"{kn} {k}" for kn, k in self.get_apikey().items())}
        self.api_repi.fulluri = self.api_repi.fullurl + ip
        data, _ = request(self.api_repi)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    @Service.unsupported
    def quota(self):
        pass
