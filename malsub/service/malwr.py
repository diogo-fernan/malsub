from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request
from malsub.common import out, frmt


@Service.unused
class Malwr(Service):
    name = "malwr"
    sname = "mw"
    api_keyl = 32

    desc = f"{name} is a community-based online sandbox for dynamic analysis\n" \
           f"and is a malware repository"
    subs = "public"
    url = "https://malwr.com/"

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec("POST", "https://malwr.com", "/api/analysis/add")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://malwr.com/
    # https://www.malwareviz.com/

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    @Service.unsupported
    def report_file(self, hash: Hash):
        pass

    @Service.unsupported
    def submit_file(self, file: File):
        # HTTP 405 Method Not Allowed
        self.api_subf.data = {**self.get_apikey(), "shared": "yes"}
        self.api_subf.file = {"file": (file.name, file.fd())}
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

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    @Service.unsupported
    def quota(self):
        pass
