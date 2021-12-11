# from malsub.service.base import APISpec, Service
# from malsub.core.type import File, Hash
# from malsub.core.web import request
# from malsub.common import out, rw, frmt


# class AVCaesar(Service):
#     name = "AVCaesar"
#     sname = "avc"
#     api_keyl = 64

#     desc = f"{name} is an online sandbox and malware repository developed under\n" \
#            f"a project from European Commission and maintained by a CERT in\n" \
#            f"Luxembourg"
#     subs = "public"
#     url = "https://avcaesar.malware.lu/"

#     api_dowf = APISpec("GET", "https://avcaesar.malware.lu", "/api/v1/sample/%s/download")
#     api_repf = APISpec("GET", "https://avcaesar.malware.lu", "/api/v1/sample/")
#     api_subf = APISpec("POST", "https://avcaesar.malware.lu", "/api/v1/sample/upload")

#     api_repa = APISpec()
#     api_repi = APISpec()
#     api_repd = APISpec()

#     api_repu = APISpec()
#     api_subu = APISpec()

#     api_srch = APISpec()
#     api_quot = APISpec("GET", "https://avcaesar.malware.lu", "/api/v1/user/quota")

#     # https://avcaesar.malware.lu/docs/api

#     def download_file(self, hash: Hash):
#         self.api_dowf.fulluri = self.api_dowf.fullurl % hash.hash
#         self.api_dowf.cookie = self.get_apikey()
#         data, filename = request(self.api_dowf, bin=True)
#         # out.debug(util.hexdump(data))
#         if filename:
#             rw.writef(filename, data)
#             return f"downloaded \"{filename}\""
#         else:
#             return "unsuccess"

#     def report_file(self, hash: Hash):
#         # hash.hash + "?overview=false&section=pe"
#         self.api_repf.fulluri = self.api_repf.fullurl + hash.hash
#         self.api_repf.cookie = self.get_apikey()
#         data, _ = request(self.api_repf)
#         data = frmt.jsontree(data)
#         return out.pformat(data)

#     def submit_file(self, file: File):
#         self.api_subf.cookie = self.get_apikey()
#         self.api_subf.file = {"file": file.fd()}
#         data, _ = request(self.api_subf)
#         data = frmt.jsontree(data)
#         return out.pformat(data)

#     @Service.unsupported
#     def report_app(self, hash: Hash):
#         pass

#     @Service.unsupported
#     def report_dom(self, dom: str):
#         pass

#     @Service.unsupported
#     def report_ip(self, ip: str):
#         pass

#     @Service.unsupported
#     def report_url(self, url: str):
#         pass

#     @Service.unsupported
#     def submit_url(self, url: str):
#         pass

#     @Service.unsupported
#     def search(self, srch: str):
#         pass

#     def quota(self):
#         self.api_quot.cookie = self.get_apikey()
#         res, _ = request(self.api_quot)
#         res = frmt.jsontree(res)
#         return out.pformat(res)
