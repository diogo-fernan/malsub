import json
from requests.exceptions import HTTPError
from requests.exceptions import HTTPError

from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import rw, frmt, out


class Triage(Service):
    name = "Triage"
    sname = "triage"
    api_keyl = 0

    desc = f"{name} is a commercial sandbox with extensive capabilities for "
    "identifying malwares and extracting configurations."
    subs = "public/private"
    url = "https://tria.ge"

    api_dowf = APISpec("GET", "https://api.tria.ge", "/v0/samples/%s/sample")
    api_repf = APISpec()
    api_subf = APISpec("POST", "https://api.tria.ge", "/v0/samples")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec("POST", "https://api.tria.ge", "/v0/samples")

    api_srch = APISpec("GET", "https://api.tria.ge", "/v0/search?query=%s")
    api_quot = APISpec()

    def download_file(self, hash: Hash):
        """
        We are doing two requests - one for searching,
        and another (if found) for downloading.
        The download query receives a proprietry triage id
        which we are fetching through the first query.
        """
        headers = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}

        self.api_srch.fulluri = self.api_srch.fullurl % f"{hash.alg}:{hash.hash}"
        self.api_srch.header = headers
        data, _ = request(self.api_srch)

        j = json.loads(data)
        if len(j["data"]) == 0:
            return f'sample "{hash}" not found'
        sample_id = j["data"][0]["id"]

        # Download query.
        self.api_dowf.fulluri = self.api_dowf.fullurl % sample_id
        self.api_dowf.header = headers

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

    @Service.unsupported
    def report_file(self, hash: Hash):
        pass

    def submit_file(self, file: File):
        self.api_subf.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        self.api_subf.file = {
            "file": (file.name, file.fd(), "application/octet-stream"),
            "_json": (None, json.dumps({"kind": "file"}), "application/json"),
        }
        data, _ = request(self.api_subf)
        data = frmt.jsontree(data)
        return out.pformat(data)

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
        self.api_subu.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        self.api_subu.json = {"kind": "url", "url": url}
        data, _ = request(self.api_subf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def search(self, srch: str):
        self.api_srch.fulluri = self.api_srch.fullurl % srch
        self.api_srch.header = {"Authorization": f"Bearer {self.get_apikey(key=True)}"}
        data, _ = request(self.api_srch)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
