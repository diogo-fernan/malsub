from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash, HASH_SHA256
from malsub.core.web import request, openurl
from malsub.common import rw


class VxStream(Service):
    name = "VxStream"
    sname = "vs"
    api_keyl = 25

    desc = (
        f"{name} features in-depth static and dynamic analysis techniques\n"
        f"within sanboxed environments and is a malware repository created by\n"
        f"Payload Security"
    )
    subs = "private"
    url = "https://www.vxstream-sandbox.com/"

    api_stat = APISpec("GET", "https://demo11.vxstream-sandbox.com", "/api/state/%s")

    api_dowf = APISpec("GET", "https://demo11.vxstream-sandbox.com", "/api/result/%s")
    api_repf = APISpec("GET", "https://demo11.vxstream-sandbox.com", "/api/scan/%s")
    api_subf = APISpec("POST", "https://demo11.vxstream-sandbox.com", "/api/submit")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec("GET", "https://demo12.vxstream-sandbox.com", "/api/result/%s")
    api_subu = APISpec("POST", "https://demo12.vxstream-sandbox.com", "/api/submiturl")

    api_srch = APISpec("GET", "https://demo12.vxstream-sandbox.com", "/api/search")
    api_quot = APISpec("GET", "https://demo12.vxstream-sandbox.com", "/api/quota")

    # https://www.vxstream-sandbox.com/apikeys/info

    #   1: Windows 7 32 bit - Usermode Monitor
    #   2: Windows 7 64 bit - Usermode Monitor
    #   3: Windows 8.1 32 bit - Usermode Monitor
    #   4: Windows 7 32 bit - Kernelmode Monitor
    #   5: unused
    #   6: Windows XP (Only PE/Scripts)
    #   7: Windows XP Kernelmode Monitor (Only PE/Scripts)
    #   8: unused
    #   9: Windows 8.1 32 bit - Kernelmode Monitor
    #  10: Android Static Analysis
    # 100: Windows 7 32 bit (Kernelmode Monitor)
    # 110: Windows 7 64 bit (Kernelmode Monitor, cloud service only)
    # 200: Android Static Analysis

    def state(self, hash: Hash):
        if hash.alg == HASH_SHA256:
            self.api_stat.fulluri = self.api_stat.fullurl % hash.hash
            self.api_stat.param = {
                "environmentId": 100,
                "type": "json",
                **self.get_apikey(),
            }
            data, _ = request(self.api_stat, json=True)
            if data["response_code"] == 0 and data["response"]["state"] == "SUCCESS":
                return data, True
            else:
                return data, False
        else:
            return False

    def download_file(self, hash: Hash):
        if hash.alg == HASH_SHA256:
            data, flag = self.state(hash)
            if flag:
                self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
                self.api_dowf.param = {
                    "environmentId": 100,
                    "type": "bin",
                    **self.get_apikey(),
                }
                filename = hash.hash + ".gz"
                data, _ = request(self.api_dowf, bin=True)
                rw.writef(filename, data)
                return f'downloaded "{filename}"'
            else:
                return f'sample "{hash}" private or not found'
        else:
            return f"{hash.alg} is not SHA-256"

    def report_file(self, hash: Hash):
        if hash.alg == HASH_SHA256:
            data, flag = self.state(hash)
            if flag:
                self.api_repf.fulluri = self.api_repf.fullurl % hash.hash
                self.api_repf.param = {
                    "environmentId": 100,
                    "type": "json",
                    **self.get_apikey(),
                }
                data, _ = request(self.api_repf)
            return data
        else:
            return f"{hash.alg} is not SHA-256"

    def submit_file(self, file: File):
        self.api_subf.auth = self.get_apikey(key=True, user=True)
        self.api_subf.data = {
            "environmentId": 100
            # "nosharevt": "true"
        }
        self.api_subf.file = {"file": file.fd()}
        data, _ = request(self.api_subf)
        return data

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
        # VxStream URL reports are based on the SHA256 values
        # provided upon submission
        hash = Hash(url)
        if hash.alg == HASH_SHA256:
            self.api_stat.fulluri = self.api_stat.fullurl % hash.hash
            self.api_stat.param = {
                "environmentId": 100,
                "type": "json",
                **self.get_apikey(),
            }
            data, _ = request(self.api_stat, json=True)
            if data["response_code"] == 0 and data["response"]["state"] == "SUCCESS":
                self.api_repu.fulluri = self.api_repu.fullurl % hash.hash
                self.api_repu.param = {
                    "environmentId": 100,
                    "type": "json",
                    **self.get_apikey(),
                }
                data, _ = request(self.api_repu)
            return data
        else:
            return f"{hash.alg} is not SHA-256"

    def submit_url(self, url: str):
        self.api_subu.auth = self.get_apikey(key=True, user=True)
        self.api_subu.data = {"analyzeurl": url, "environmentId": 100}
        self.api_subu.param = self.get_apikey()
        data, _ = request(self.api_subu)
        return data

    def search(self, srch: str):
        self.api_srch.param = {"query": srch, **self.get_apikey()}
        data, _ = request(self.api_srch)
        return data

    def quota(self):
        self.api_quot.param = self.get_apikey()
        data, _ = request(self.api_quot)
        return data
