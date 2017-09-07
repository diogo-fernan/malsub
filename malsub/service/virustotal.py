# from .service import service
from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, frmt, rw


class VirusTotal(Service):
    name = "VirusTotal"
    sname = "vt"
    api_keyl = [32, 48, 64]

    desc = f"{name} is a well-known online repository by Google of malware and\n" \
           f"malicious URLs with on-demand scanning features using a number of\n" \
           f"selected antivirus engines"
    subs = "public/private"
    # frmt = "closed"
    url = "https://www.virustotal.com"


    api_dowf = APISpec("GET", "https://www.virustotal.com", "/vtapi/v2/file/download")
    api_repf = APISpec("POST", "https://www.virustotal.com", "/vtapi/v2/file/report")
    api_subf = APISpec("POST", "https://www.virustotal.com", "/vtapi/v2/file/scan")

    api_repa = APISpec()
    api_repd = APISpec("GET", "https://www.virustotal.com", "/vtapi/v2/domain/report")
    api_repi = APISpec("GET", "https://www.virustotal.com", "/vtapi/v2/ip-address/report")

    api_repu = APISpec("POST", "https://www.virustotal.com", "/vtapi/v2/url/report")
    api_subu = APISpec("POST", "https://www.virustotal.com", "/vtapi/v2/url/scan")

    api_srch = APISpec("GET", "https://www.virustotal.com", "/vtapi/v2/file/search")
    api_quot = APISpec()

    # https://www.virustotal.com/en/documentation/public-api/
    # https://www.virustotal.com/en/documentation/private-api/


    def download_file(self, hash: Hash):
        from requests.exceptions import HTTPError
        self.api_dowf.param = {**self.get_apikey(), "hash": hash.hash}
        try:
            data, filename = request(self.api_dowf, bin=True)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f"sample \"{hash}\" not found"
            raise HTTPError(e)
        if not filename:
            filename = hash.hash
        rw.writef(filename, data)
        return f"downloaded \"{filename}\""

    def report_file(self, hash: Hash):
        self.api_repf.data = {**self.get_apikey(), "resource": hash.hash}
        data, _ = request(self.api_repf)
        data = frmt.jsontree(data, depth=1)
        # data = frmt.jsonvert(data["scans"])
        # openurl(data["permalink"])
        return out.pformat(data)

    def submit_file(self, file: File):
        self.api_subf.data = self.get_apikey()
        self.api_subf.file = {"file": (file.name, file.fd())}
        if file.len > 32 * 1024 * 1024:
            api_subfl = APISpec("GET", "https://www.virustotal.com",
                "/vtapi/v2/file/scan/upload_url")
            api_subfl.param = {**self.get_apikey()}

            data, _ = request(api_subfl)
            data = frmt.jsontree(data)
            self.api_subf.fulluri = data["upload_url"]
            self.api_subf.data = None
        else:
            self.api_subf.default()

        data, _ = request(self.api_subf)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        data = frmt.jsonvert(data)
        # return out.pformat(data)
        return data

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.param = {**self.get_apikey(), "domain": dom}
        data, _ = request(self.api_repd)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_ip(self, ip: str):
        self.api_repi.param = {**self.get_apikey(), "ip": ip}
        data, _ = request(self.api_repi)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_url(self, url: str):
        self.api_repu.data = {**self.get_apikey(), "resource": url}
        data, _ = request(self.api_repu)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        return out.pformat(data)

    def submit_url(self, url: str):
        self.api_subu.data = {**self.get_apikey(), "url": url}
        data, _ = request(self.api_subu)
        data = frmt.jsontree(data)
        # web.openurl(data["permalink"])
        return out.pformat(data)

    def search(self, srch: str):
        self.api_srch.param = {**self.get_apikey(), "query": srch}
        data, _ = request(self.api_srch)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
