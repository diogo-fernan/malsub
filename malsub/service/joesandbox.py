from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import out


class JoeSandbox(Service):
    name = "Joe Sandbox"
    sname = "js"
    api_keyl = 64

    desc = f"{name} is an advanced sandbox for analyzing executables, files and URLs."
    subs = "private"
    url = "https://www.joesecurity.org/"

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec("POST", "https://jbxcloud.joesecurity.org", "/api/v2/analysis/submit")

    api_repa = APISpec("POST", "https://jbxcloud.joesecurity.org", "/api/v2/analysis/download")
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec("POST", "https://jbxcloud.joesecurity.org", "/api/v2/analysis/submit")

    api_srch = APISpec("POST", "https://jbxcloud.joesecurity.org", "/api/v2/analysis/search")
    api_quot = APISpec("POST", "https://jbxcloud.joesecurity.org", "/api/v2/account/info")

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    def report_file(self, hash: Hash):
        matches = self.search(hash.hash)

        if not matches:
            return None

        # pick one of the analyses
        webid = matches[-1]["webid"]

        self.api_repa.data = {
            "webid": webid,
            "type": "irjsonfixed",
            **self.get_apikey()
        }

        data, _ = request(self.api_repa, json=True)
        return out.pformat(data["analysis"])

    def submit_file(self, file: File):
        self.api_subf.data = {
            "accept-tac": "1" if self._accept_tac else "0",
            **self.get_apikey()
        }
        self.api_subf.file = {
            "sample": file.fd()
        }
        data, _ = request(self.api_subf, json=True)
        return data["data"]

    def submit_url(self, url: str):
        self.api_subu.data = {
            "url": url,
            "accept-tac": "1" if self._accept_tac else "0",
            **self.get_apikey()
        }
        data, _ = request(self.api_subu, json=True)
        return data["data"]

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

    def search(self, srch: str):
        self.api_srch.data = {
            "q": srch,
            **self.get_apikey()
        }
        data, _ = request(self.api_srch, json=True)
        return data["data"]

    def quota(self):
        self.api_quot.data = self.get_apikey()
        data, _ = request(self.api_quot, json=True)
        return data["data"]["quota"]

# It's currently not possible to overwrite classmethods in the class definition,
# thus we need to do it after the class is defined.
def _set_apikey(cls, apikey: dict):
    cls._accept_tac = apikey["apikey"]["accept-tac"]
    return Service.set_apikey(apikey)
JoeSandbox.set_apikey = classmethod(_set_apikey)
