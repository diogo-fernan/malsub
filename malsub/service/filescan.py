from requests.exceptions import HTTPError

from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash, HASH_SHA256
from malsub.core.web import request
from malsub.common import frmt, rw
from malsub.core import meta


class FileScan(Service):
    name = "FileScan"
    sname = "fs"
    api_keyl = 40

    desc = (
        f"{name} features in-depth file assessments, threat intelligence\n"
        f"and extraction of Indicators of Compromise (IOCs) for a wide range\n"
        f"of scripts, documents and executable files"
    )
    subs = "public/private"
    url = "https://www.filescan.io"

    api_dowf = APISpec("GET", url, "/api/files/%s")
    api_repf = APISpec("GET", url, "/api/reports/search")
    api_subf = APISpec("POST", url, "/api/scan/file")

    api_repa = APISpec()
    api_repd = APISpec("GET", url, "/api/reports/search")
    api_repi = APISpec("GET", url, "/api/reports/search")

    api_repu = APISpec("GET", url, "/api/reports/search")
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec("GET", url, "/api/users/me")

    def download_file(self, hash: Hash):
        if hash.alg == HASH_SHA256:
            self.api_dowf.header = {"X-Api-Key": self.get_apikey(key=True)}
            self.api_dowf.param = {
                "password": "infected",
                "type": "raw",
            }
            self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
            try:
                data, _ = request(self.api_dowf, bin=True)
                filename = f"{hash.hash}.zip"
                rw.writef(filename, data)
                return f'downloaded "{filename}"'
            except HTTPError as e:
                if e.response.status_code == 404:
                    return f'sample "{hash.hash}" private or not found'
        else:
            return f"{hash.alg} is not SHA-256"

    def report_file(self, hash: Hash):
        self.api_repf.header = {"X-Api-Key": self.get_apikey(key=True)}
        self.api_repf.param = {"sha256": hash.hash}
        data, _ = request(self.api_repf)
        data = frmt.jsondump(data)
        return data

    def submit_file(self, file: File):
        self.api_subf.header = {"X-Api-Key": self.get_apikey(key=True)}
        self.api_subf.data = {
            "description": f"submitted by {meta.MALSUB_NAME} {meta.MALSUB_VERSION}"
        }
        self.api_subf.file = {"file": file.fd()}
        data, _ = request(self.api_subf)
        return data

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.header = {"X-Api-Key": self.get_apikey(key=True)}
        self.api_repd.param = {"domain": dom}
        data, _ = request(self.api_repd)
        data = frmt.jsondump(data)
        return data

    def report_ip(self, ip: str):
        self.api_repi.header = {"X-Api-Key": self.get_apikey(key=True)}
        self.api_repi.param = {"ip": ip}
        data, _ = request(self.api_repi)
        data = frmt.jsondump(data)
        return data

    def report_url(self, url: str):
        self.api_repu.header = {"X-Api-Key": self.get_apikey(key=True)}
        self.api_repu.param = {"url": url}
        data, _ = request(self.api_repu)
        data = frmt.jsondump(data)
        return data

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    def quota(self):
        self.api_quot.header = {"X-Api-Key": self.get_apikey(key=True)}
        data, _ = request(self.api_quot)
        data = frmt.jsondump(data)
        return data
