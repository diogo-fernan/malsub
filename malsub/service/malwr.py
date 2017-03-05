from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt


@Service.unused
class Malwr(Service):
    name = "malwr"
    sname = "mw"
    api_keyl = 32

    api_dowf = APISpec()
    api_repf = APISpec("POST", "https://malwr.com", "/api/analysis/status")
    api_subf = APISpec("POST", "https://malwr.com", "/api/analysis/add")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://malwr.com/
    # waiting to come back from maintenance

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    @Service.unsupported
    def report_file(self, hash: Hash):
        pass

    @Service.unsupported
    def submit_file(self, file: File):
        # https://www.malwareviz.com/
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

    @Service.unsupported
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
