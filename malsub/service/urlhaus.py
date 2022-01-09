import io
import json
from requests.exceptions import HTTPError
from zipfile import ZipFile

from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import out, frmt, rw


class MalwareBazaar(Service):
    name = "URLhaus"
    sname = "urlhaus"
    api_keyl = 0

    desc = f"{name} is a public repository for malicious URLs, and their payloads."
    subs = "public"
    url = "https://urlhaus.abuse.ch/"

    api_dowf = APISpec("GET", "https://urlhaus-api.abuse.ch", "/v1/download/%s")
    api_repf = APISpec("POST", "https://urlhaus-api.abuse.ch", "/v1/payload")
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec("POST", "https://urlhaus-api.abuse.ch", "/v1/host")
    api_repi = APISpec()

    api_repu = APISpec("POST", "https://urlhaus-api.abuse.ch", "/v1/url")
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    def download_file(self, hash: Hash):
        if hash.alg != "sha256":
            return f"wrong params. should be given sha256"
        self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
        try:
            data, filename = request(self.api_dowf, bin=True)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f'sample "{hash}" not found'
            raise HTTPError(e)
        if not filename:
            filename = hash.hash

        # If the response is json, so some error occured (contains 'sample not found' error)
        try:
            j = json.loads(data)
            return f'error {j["query_status"]}'
        except:
            pass

        try:
            input_zip = ZipFile(io.BytesIO(data))
            data = input_zip.read(input_zip.namelist()[0])
        except:
            return f'failed unzipping "{hash.hash}"'

        rw.writef(filename, data)
        return f'downloaded "{filename}"'

    def report_file(self, hash: Hash):
        if hash.alg not in ["sha256", "md5"]:
            return f"wrong params. should be sha256/sha1/md5"
        self.api_repf.data = {f"{hash.alg}_hash": hash.hash}
        data, _ = request(self.api_repf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def submit_file(self, file: File):
        pass

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.data = {"host": dom}
        data, _ = request(self.api_repd)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_ip(self, ip: str):
        # Urlhaus treats IPs and domains the same.
        return self.report_dom(ip)

    def report_url(self, url: str):
        self.api_repu.data = {"url": url}
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
