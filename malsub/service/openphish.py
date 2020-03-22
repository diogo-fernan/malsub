from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, rw, frmt


class OpenPhish(Service):
    name = "OpenPhish"
    sname = "op"
    api_keyl = 0

    desc = f"{name} is a proprietary phishing threat intelligence source that\n" \
           f"uses artificial intelligence for automated classification"
    subs = "public/private"
    url = "https://openphish.com/"

    # api_dowf = APISpec("GET", "https://openphish.com", "/prvt-intell/")
    api_dowf = APISpec("GET", "https://openphish.com", "/feed.txt")
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://openphish.com/

    def download_file(self, hash: Hash, directory: str = None):
        # self.api_dowf.fulluri = self.api_dowf.url + "/feed.txt"
        data, filename = request(self.api_dowf)
        rw.writef("openphish-community.txt", data)
        return "downloaded \"openphish-community.txt\""

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
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    @Service.unsupported
    def quota(self):
        pass
