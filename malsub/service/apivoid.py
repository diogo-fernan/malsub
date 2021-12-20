from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request
from malsub.common import frmt


class APIVoid(Service):
    name = "APIVoid"
    sname = "av"
    api_keyl = 40

    desc = (
        f"{name} is a pay-as-you-go blacklist and reputation-based scanning engine\n"
        f"for URLs"
    )
    subs = "private"
    url = "https://www.apivoid.com/"

    api_dowf = APISpec()
    api_repf = APISpec()
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec(
        "GET",
        "https://endpoint.apivoid.com",
        "/domainbl/v1/pay-as-you-go/?key=%s&host=%s",
    )
    api_repi = APISpec(
        "GET",
        "https://endpoint.apivoid.com",
        "/domainbl/v1/pay-as-you-go/?key=%s&ip=%s",
    )

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec(
        "GET",
        "https://endpoint.apivoid.com",
        "/domainbl/v1/pay-as-you-go/?key=%s&stats",
    )

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

    def report_dom(self, dom: str):
        self.api_repd.fulluri = self.api_repd.fullurl % (self.get_apikey(key=True), dom)
        data, _ = request(self.api_repd)
        data = frmt.jsondump(data)
        return data

    def report_ip(self, ip: str):
        self.api_repi.fulluri = self.api_repd.fullurl % (self.get_apikey(key=True), ip)
        data, _ = request(self.api_repi)
        data = frmt.jsondump(data)
        return data

    @Service.unsupported
    def report_url(self, url: str):
        pass

    @Service.unsupported
    def submit_url(self, url: str):
        pass

    @Service.unsupported
    def search(self, srch: str):
        pass

    def quota(self):
        self.api_quot.fulluri = self.api_quot.fullurl % (self.get_apikey(key=True))
        data, _ = request(self.api_quot)
        data = frmt.jsondump(data)
        return data
