import json, gzip
from requests.exceptions import HTTPError

from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import frmt, rw


class HybridAnalysis(Service):
    name = "Hybrid Analysis"
    sname = "ha"
    api_keyl = 25

    desc = (
        f"{name} features in-depth static and dynamic analysis techniques\n"
        f"within sandboxed environments and is a malware repository created by\n"
        f"Payload Security"
    )
    subs = "public/private"
    url = "https://www.hybrid-analysis.com"

    api_dowf = APISpec("GET", url, "/api/v2/overview/%s/sample")
    api_repf = APISpec("GET", url, "/api/v2/overview/%s")
    api_subf = APISpec("POST", url, "/api/v2/submit/file")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec("POST", url, "/api/v2/submit/url")

    api_srch = APISpec()
    api_quot = APISpec("GET", url, "/api/v2/key/submission-quota")

    def download_file(self, hash: Hash):
        if hash.alg != "sha256":
            return f"wrong params. should be given sha256"
        self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
        self.api_dowf.header = {
            **self.get_apikey(),
        }
        try:
            data, _ = request(self.api_dowf, bin=True)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f'sample "{hash}" not found'
            raise HTTPError(e)

        # The returned filename contains bin.sample.gz suffix, so we are not using it.
        filename = hash.hash

        # If the response is json, so some error occured (contains 'sample not found' error)
        try:
            j = json.loads(data)
            return f'error {j["message"]}'
        except:
            pass

        try:
            data = gzip.decompress(data)
        except:
            return f'failed unzipping "{hash.hash}"'

        rw.writef(filename, data)
        return f'downloaded "{filename}"'

    def report_file(self, hash: Hash):
        if hash.alg != "sha256":
            return f"wrong params. should be given sha256"
        self.api_repf.fulluri = self.api_repf.fullurl % hash.hash
        self.api_repf.header = {
            **self.get_apikey(),
        }
        data, _ = request(self.api_repf)
        data = frmt.jsondump(data)
        return data

    def submit_file(self, file: File):
        # Defaullt environment for Windows 7 64bit
        self.api_subf.data = {"environment_id": 120}
        self.api_subf.file = {"file": file.fd()}
        self.api_subf.header = {
            **self.get_apikey(),
        }
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

    def submit_url(self, url: str):
        # Defaullt environment for Windows 7 64bit
        self.api_subu.data = {"url": url, "environment_id": 120}
        self.api_subu.header = {
            **self.get_apikey(),
        }
        data, _ = request(self.api_subu)
        return data

    @Service.unsupported
    def search(self, srch: str):
        pass

    def quota(self):
        self.api_quot.header = {
            **self.get_apikey(),
        }
        data, _ = request(self.api_quot)
        data = frmt.jsondump(data)
        return data
