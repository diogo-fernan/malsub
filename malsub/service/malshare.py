from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import frmt, rw


class MalShare(Service):
    name = "MalShare"
    sname = "ms"
    api_keyl = 64

    desc = f"{name} is a community-driven malware repository"
    subs = "public"
    url = "http://malshare.com/"

    api_dowf = APISpec("GET", "https://malshare.com", "/api.php", cert=True)
    api_repf = APISpec("GET", "https://malshare.com", "/api.php", cert=True)
    api_subf = APISpec(
        "POST", "https://malshare.com", "/api.php?action=upload&api_key=%s", cert=True
    )

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec(
        "GET",
        "https://malshare.com",
        "/api.php?api_key=%s&action=details&hash=%s",
        cert=True,
    )
    api_quot = APISpec()

    # https://malshare.com/doc.php

    def download_file(self, hash: Hash):
        self.api_dowf.param = {
            **self.get_apikey(),
            "action": "getfile",
            "hash": hash.hash,
        }
        data, filename = request(self.api_dowf, bin=True)
        if data.startswith(b"Sample not found by hash"):
            return f'sample "{hash}" not found'
        if not filename:
            filename = hash.hash
        rw.writef(filename, data)
        return f'downloaded "{filename}"'

    def report_file(self, hash: Hash):
        self.api_repf.param = {
            **self.get_apikey(),
            "action": "details",
            "hash": hash.hash,
        }
        data, _ = request(self.api_repf)
        data = frmt.jsondump(data)
        return data

    def submit_file(self, file: File):
        self.api_subf.fulluri = self.api_subf.fullurl % (self.get_apikey(key=True))
        self.api_subf.file = {"upload": file.fd()}
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
        self.api_srch.fulluri = self.api_srch.fullurl % (
            self.get_apikey(key=True),
            srch,
        )
        data, _ = request(self.api_srch)
        data = frmt.jsondump(data)
        return data

    @Service.unsupported
    def quota(self):
        pass
