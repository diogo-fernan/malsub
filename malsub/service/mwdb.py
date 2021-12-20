import json
from requests.exceptions import HTTPError

from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import frmt, rw


class MWDB(Service):
    name = "MWDB"
    sname = "mwdb"
    api_keyl = 0

    desc = (
        f"{name} is a repository component for automated malware collection/analysis systems\n"
        f"created and maintained by CERT-PL\n"
    )
    subs = "public/private"
    url = "https://mwdb.cert.pl"

    api_dowf = APISpec("POST", url, "/api/file/%s/download")
    api_repf = APISpec("GET", url, "/api/file/%s")
    api_subf = APISpec("POST", url, "/api/file")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec("GET", url, "/api/file")
    api_quot = APISpec()

    def download_file(self, hash: Hash):
        self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
        self.api_dowf.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}

        try:
            data, _ = request(self.api_dowf)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f'sample "{hash}" not found'
            raise HTTPError(e)

        # The first request returns JWT token.
        # Now we can fetch the file the file.
        token = json.loads(data)["token"]
        del self.api_dowf.header["Authorization"]
        self.api_dowf.param = {"token": token}
        self.api_dowf.method = "GET"

        # Initiating a second request.
        try:
            data, filename = request(self.api_dowf, bin=True)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f'sample "{hash}" not found'
            raise HTTPError(e)
        if not filename:
            filename = hash.hash
        rw.writef(filename, data)
        return f'downloaded "{filename}"'

    def report_file(self, hash: Hash):
        self.api_repf.fulluri = self.api_repf.fullurl % hash.hash
        self.api_repf.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        data, _ = request(self.api_repf)
        return frmt.jsondump(data)

    def submit_file(self, file: File):
        self.api_subf.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        self.api_subf.file = {"file": file.fd()}
        data, _ = request(self.api_subf)
        return frmt.jsondump(data)

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
        self.api_srch.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        self.api_srch.param = {"query": srch}
        data, _ = request(self.api_srch)
        return frmt.jsondump(data)

    @Service.unsupported
    def quota(self):
        pass
