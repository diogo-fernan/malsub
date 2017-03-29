from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class ThreatCrowd(Service):
    name = "Threat Crowd"
    sname = "tc"
    api_keyl = 32

    desc = f"{name} is an open-source threat intelligence for malware maintained\n" \
           f"by AlienVault"
    subs = "public"
    url = "https://www.threatcrowd.org/"

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec("GET", "http://www.threatcrowd.org", "/searchApi/v2/domain/report/")
    api_repi = APISpec("GET", "http://www.threatcrowd.org", "/searchApi/v2/ip/report/")

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec("GET", "http://www.threatcrowd.org",  "/searchApi/v2/antivirus/report/")
    api_quot = APISpec()

    # https://www.threatcrowd.org/
    # https://github.com/AlienVault-OTX/ApiV2

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

    def report_dom(self, dom: str):
        self.api_repd.param = {"domain": dom}
        data, _ = request(self.api_repd)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_ip(self, ip: str):
        self.api_repi.param = {"ip": ip}
        data, _ = request(self.api_repi)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    def search(self, srch: str):
        self.api_srch.param = {"antivirus": srch}
        data, _ = request(self.api_srch)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
