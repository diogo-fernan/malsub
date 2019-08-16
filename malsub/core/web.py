from requests import get as requests_get, post as requests_post
# from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus, urlencode

from malsub.common import out, regex
from malsub.core import meta

GET = "GET"
POST = "POST"
METHOD = [GET, POST]

__timeout = 120

__header = {"Accept": "*/*",
            "User-Agent": f"{meta.MALSUB_NAME}{meta.MALSUB_VERSION} "
                          f"({meta.MALSUB_URL})",
            "Connection": "close"}


# class NoContentException(Exception):
#     def __init__(self):
#         self.msg = "HTTP 20x without content"
#         super(NoContentException, self).__init__(self.msg)


def _request(fn, uri, auth=None, cookie=None, data=None, file=None, header=None,
             json_req=None, param=None, verify=True, bin=False, json=False):
    # Quicksand.io has a broken cert
    if 'quicksand' in uri:
        verify = False
    elif header and type(header) is dict:
        header.update(__header)
    else:
        header = __header
    # try:
    res = fn(uri,
             auth=auth,  # HTTPBasicAuth
             cookies=cookie,
             data=data,
             files=file,
             headers=header,  # {**header, **__header},
             json=json_req,
             params=param,
             verify=verify,
             timeout=__timeout,
             stream=False)
    out.debug("res.headers", obj=dict(res.headers))
    out.debug("res.text", obj=res.text)
    res.raise_for_status()
    # except ConnectionError as e:
    # 	# out.warn(f"HTTP connection error to \"{uri}\": {e}")
    # 	raise ConnectionError(e)
    # except HTTPError as e:
    # 	# out.warn(f"HTTP response error to \"{uri}\": {e}")
    # 	raise HTTPError(e)
    # except Timeout as e:
    # 	# out.warn(f"HTTP request time out to \"{uri}\": {e}")
    # 	raise Timeout(e)
    # except TooManyRedirects as e:
    # 	# out.warn(f"too many HTTP redirects to \"{uri}\": {e}")
    # 	raise TooManyRedirects(e)
    # else:
    out.debug(f"HTTP {res.status_code} \"{res.reason}\" -- \"{uri}\"")

    if res.status_code == 204 or res.headers.get("Content-Length") == 0:
        raise Exception(f"HTTP {res.status_code} \"{res.reason}\""
                        f" -- \"{uri}\": no content")

    filename = regex.http_filename(res.headers.get("Content-Disposition"))
    if bin:
        return res.content, filename
    if json:
        return res.json(), filename
    return res.text, filename


def post(uri, auth=None, cookie=None, data=None, file=None, header=None,
         json_req=None, param=None, verify=True, bin=False, json=False):
    return _request(requests_post, uri, auth, cookie, data, file, header,
                    json_req, param, verify, bin, json)


def get(uri, auth=None, cookie=None, data=None, file=None, header=None,
        json_req=None, param=None, verify=True, bin=False, json=False):
    return _request(requests_get, uri, auth, cookie, data, file, header,
                    json_req, param, verify, bin, json)


def request(apispec, bin=False, json=False):
    if apispec.method == POST:
        fn = post
    else:  # apisec.method == GET:
        fn = get
    return fn(apispec.fulluri,
              apispec.auth, apispec.cookie, apispec.data, apispec.file,
              apispec.header, apispec.json, apispec.param,
              apispec.verify, bin, json)


def test(apispec):
    if apispec.method == POST:
        fn = requests_post
    else:
        fn = requests_get
    # try:
    if apispec.header and type(apispec.header) is dict:
        apispec.header.update(__header)
    else:
        apispec.header = __header
    res = fn(apispec.fulluri,
             auth=apispec.auth,
             cookies=apispec.cookie,
             data=apispec.data,
             headers=apispec.header,  # {**apispec.header, **__header},
             json=apispec.json,
             params=apispec.param,
             verify=apispec.verify,
             timeout=__timeout,
             stream=False)
    res.raise_for_status()
    # except Exception as e:
    #  	out.warn(f"unsuccessful test HTTP {apisec.method} to "
    # 			 f"\"{apisec.fulluri}\": {e}")
    # else:
    out.debug(f"successful test HTTP {apispec.method} to \"{apispec.fulluri}\"")
    res.close()
    del res
    return


def openurl(url):
    from webbrowser import open as webopen
    url = parse_fullurl(url)
    webopen(url.lower())


def encodeurl(url):
    return urlencode(url, safe='/', quote_via=quote_plus)


def quoteurl(url):
    return quote_plus(url, safe='/')


def parse_method(method):
    if not method.upper() in METHOD:
        out.error(f"unknown HTTP method in \"{method}\" (should be \"{METHOD}\")")
    return method.upper()


def parse_ipaddrl(*ipaddr):
    # ipl = []
    # for i in ipaddr:
    # 	if regex.isipaddr(i):
    # 		ipl += [i]
    # return ipl
    return [i for i in ipaddr if regex.isipaddr(i)]


def parse_domainl(*dom):
    # doml = []
    # for d in dom:
    # 	if regex.isdomain(d):
    # 		doml += [d]
    # return doml
    return [d for d in dom if regex.isdomain(d)]


def parse_fullurll(*url):
    # urll = []
    # for u in url:
    # 	if regex.isfullurl(u):
    # 		urll += [u]
    # return urll
    return [u for u in url if regex.isfullurl(u)]


def parse_fullurl(url):
    if regex.isfullurl(url):
        return url.lower()
    else:
        out.warn(f"malformed full URL \"{url}\"")


def parse_url(url):
    if regex.isurl(url):
        return url.lower()
    else:
        out.error(f"malformed URL \"{url}\"")


def parse_uri(uri):
    if regex.isuri(uri):
        # return uri.lower()
        return uri
    else:
        out.error(f"malformed URI \"{uri}\"")
