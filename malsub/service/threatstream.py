from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash, HASH_MD5, HASH_SHA1
from malsub.core.web import request
from malsub.common import out, frmt


class ThreatStream(Service):
    name = "ThreatStream"
    sname = "ts"
    api_keyl = 40

    desc = (
        f"Anomali {name} is a threat intelligence platform that aggregates\n"
        f"several threat feeds"
    )
    subs = "private"
    url = "https://www.anomali.com/platform/threatstream"

    api_stat = APISpec()

    api_dowf = APISpec()
    api_repf = APISpec("GET", "https://api.threatstream.com", "/api/v2/intelligence")
    api_subf = APISpec()

    api_repa = APISpec()
    api_repd = APISpec("GET", "https://api.threatstream.com", "/api/v2/intelligence")
    api_repi = APISpec("GET", "https://api.threatstream.com", "/api/v2/intelligence")

    api_repu = APISpec("GET", "https://api.threatstream.com", "/api/v2/intelligence")
    api_subu = APISpec()

    api_srch = APISpec("GET", "https://api.threatstream.com", "/api/v2/intelligence")
    api_quot = APISpec()

    # https://github.com/threatstream/threatstream-api

    limit = 0  # '0' means 1000

    @Service.unsupported
    def download_file(self, hash: Hash):
        pass

    @Service.unsupported
    def report_file(self, hash: Hash):
        if hash.alg == HASH_MD5 or hash.alg == HASH_SHA1:
            self.api_repf.param = {
                **self.get_apikey(),
                "type": "md5",  # MD5 or SHA-1
                "value": hash.hash,
                "limit": self.limit,
            }
            data, _ = request(self.api_repf)
            data = frmt.jsontree(data)
            return out.pformat(data)
        else:
            return f"{hash.alg} is not MD5 or SHA1"

    @Service.unsupported
    def submit_file(self, file: File):
        pass

    @Service.unsupported
    def report_app(self, hash: Hash):
        pass

    def report_dom(self, dom: str):
        self.api_repd.param = {
            **self.get_apikey(),
            "limit": self.limit,
            "type": "domain",
            "value": dom,
        }
        data, _ = request(self.api_repd)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_ip(self, ip: str):
        self.api_repi.param = {**self.get_apikey(), "ip": ip, "limit": self.limit}
        data, _ = request(self.api_repi)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def report_url(self, url: str):
        self.api_repu.param = {
            **self.get_apikey(),
            "limit": self.limit,
            "type": "url",
            "value": url,
        }
        data, _ = request(self.api_repu)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def submit_url(self, url: str):
        self.api_subu.data = {
            **self.get_apikey(),
            "report_radio-platform": "WINDOWS7",
            "report_radio-url": url,
        }
        data, _ = request(self.api_subu)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def search(self, srch: str):
        from re import escape

        srch = escape(srch)
        self.api_srch.param = {
            **self.get_apikey(),
            "limit": self.limit,
            "value__regexp": f".*{srch}.*",
        }
        data, _ = request(self.api_srch)
        data = frmt.jsontree(data)
        return out.pformat(data)

    @Service.unsupported
    def quota(self):
        pass
