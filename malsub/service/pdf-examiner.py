from malsub.service.base import APISpec, Service
from malsub.core.type import File, Hash
from malsub.core.web import request, openurl
from malsub.common import out, frmt


class PDFExaminer(Service):
    name = "PDF Examiner"
    sname = "pe"
    api_keyl = 32

    desc = f"{name} is an in-depth, automated PDF analysis service with\n" \
           f"obfuscation, encryption and stream analysis and exploit detection"
    subs = "public/private"
    url = "https://www.pdfexaminer.com/"

    api_dowf = APISpec()
    api_repf = APISpec("POST", "https://www.pdfexaminer.com", "/pdfapirep.php")
    api_subf = APISpec("POST", "https://www.pdfexaminer.com", "/pdfapi.php")

    api_repa = APISpec()
    api_repd = APISpec()
    api_repi = APISpec()

    api_repu = APISpec()
    api_subu = APISpec()

    api_srch = APISpec()
    api_quot = APISpec()

    # https://www.pdfexaminer.com/
    # https://github.com/mwtracker/pdfexaminer_tools

    @Service.unsupported
    def download_file(self, hash: Hash, directory: str = None):
        pass

    def report_file(self, hash: Hash):
        self.api_repf.data = {"type": "json", hash.alg: hash.hash}
        data, _ = request(self.api_repf)
        data = frmt.jsontree(data)
        return out.pformat(data)

    def submit_file(self, file: File):
        self.api_subf.file = {"sample[]": file.fd()}
        self.api_subf.data = {"type": "json", "message": "", "email": ""}
        data, _ = request(self.api_subf)
        if " is not a PDF file. Not processed." in data:
            return f"{file} is not a PDF file"
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
