from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class QuickSand(Service):
    name = "QuickSand"
    sname = "qs"
    api_keyl = 32

    api_dowf = APISpec()
    api_repf = APISpec("POST", "https://www.quicksand.io", "/api.php")
    api_subf = APISpec("POST", "https://www.quicksand.io", "/upload.php")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://www.quicksand.io/
    # https://github.com/tylabs/quicksand_tools

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    def report_file(self, hash: Hash):
        self.api_repf.data = {**self.get_apikey(), "query": hash.hash}
        data, _ = request(self.api_repf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def submit_file(self, file: File):
        self.api_subf.file = {"file[]": file.fd()}
        self.api_subf.data = {**self.get_apikey(), "QUICKSAND_RERUN": 1}
        # {"QUICKSAND_BRUTE": 1, "QUICKSAND_LOOKAHEAD": 1}
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
