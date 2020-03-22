from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class HaveIbeenpwned(Service):
    name = "Have I been pwned?"
    sname = "pwn"
    api_keyl = 0

    desc = f"{name} is a repository of database dumps created by Troy Hunt"
    subs = "public"
    url = "https://haveibeenpwned.com/"

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec("GET", "https://haveibeenpwned.com", "/api/v2/breaches")
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec("GET", "https://haveibeenpwned.com", "/api/v2/%s/%s")
    api_quot = APISpec()

    # https://haveibeenpwned.com/API/v2
    # ?truncateResponse=true

    @Service.unsupported
    def download_file(self, hash: Hash, directory: str = None):
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
        if data == []:
            return f"domain \"{dom}\" not found"
        return out.pformat(data)

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
        from requests.exceptions import HTTPError
        self.api_srch.fulluri = self.api_srch.fullurl % \
                                ("breachedaccount", srch)
        try:
            data, _ = request(self.api_srch)
        except HTTPError as e:
            if e.response.status_code == 404:
                return f"account \"{srch}\" not found"
            raise HTTPError(e)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
