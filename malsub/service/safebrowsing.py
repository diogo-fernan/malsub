from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.meta import MALSUB_NAME, MALSUB_VERSION
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class SafeBrowsing(Service):
    name = "Safe Browsing"
    sname = "sb"
    api_keyl = 39

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec("POST", "https://safebrowsing.googleapis.com", "/v4/threatMatches:find")
    api_subu = APISpec()

    api_srch = APISpec("GET", "https://safebrowsing.googleapis.com", "/v4/threatLists")
    api_quot = APISpec()

    # https://developers.google.com/safe-browsing/

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

    @Service.unsupported
    def report_dom(self, dom: str):
        pass

    @Service.unsupported
    def report_ip(self, ip: str):
        pass

    def report_url(self, url: str):
        self.api_repu.param = self.get_apikey()
        self.api_repu.header = {'Content-Type': 'application/json'}
        self.api_repu.json = {
            "client": {
                "clientId": MALSUB_NAME,
                "clientVersion": MALSUB_VERSION
            },
            "threatInfo": {
                # "POTENTIALLY_HARMFUL_APPLICATION"
                # "THREAT_TYPE_UNSPECIFIED"
                # "UNWANTED_SOFTWARE"
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ALL_PLATFORMS"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }
        data, _ = request(self.api_repu)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    def search(self, srch: str):
        self.api_srch.param = self.get_apikey()
        self.api_srch.header = {'Content-Type': 'application/json'}
        data, _ = request(self.api_srch)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
