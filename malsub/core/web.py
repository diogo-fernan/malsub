from requests import get as requests_get, post as requests_post
from urllib.parse import quote_plus, urlencode

from malsub.common import out, regex
from malsub.core import meta

GET = 'GET'
POST = 'POST'
METHOD = [GET, POST]

__timeout = 60

__header = {'Accept': '*/*',
            'User-Agent': f"{meta.MALSUB_NAME} {meta.MALSUB_URL}",
            'Connection': 'close'}

__http_nocontent = 204


class NoContentException(Exception):
    def __init__(self):
        self.msg = "HTTP response code is 204 or server returned no content"
        super(NoContentException, self).__init__(self.msg)


def _request(fn, uri, header=None, cookie=None, data=None, json=None, file=None,
             param=None, verify=True, bin=False):
    if header and type(header) is dict:
        header.update(__header)
    else:
        header = __header
    # try:
    res = fn(uri,
             cookies=cookie,
             data=data,
             json=json,
             files=file,
             params=param,
             headers=header,  # {**header, **__header},
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
    out.debug(f"successfull HTTP response from \"{uri}\": "
              f"{res.status_code} \"{res.reason}\"")
    if res.status_code == __http_nocontent or res.headers.get(
            "Content-Length") == 0:
        raise NoContentException

    filename = regex.http_filename(res.headers.get("Content-Disposition"))
    if bin:
        return res.content, filename
    return res.text, filename


def post(uri, header=None, cookie=None, data=None, json=None, file=None,
         param=None, verify=True, bin=False):
    return _request(requests_post, uri, header, cookie, data, json, file, param,
                    verify, bin)


def get(uri, header=None, cookie=None, data=None, json=None, file=None,
        param=None, verify=True, bin=False):
    return _request(requests_get, uri, header, cookie, data, json, file, param,
                    verify, bin)


def request(apispec, bin=False):
    if apispec.method == POST:
        fn = post
    else:  # apisec.method == GET:
        fn = get
    return fn(apispec.fulluri,
              apispec.header, apispec.cookie,
              apispec.data, apispec.json, apispec.file,
              apispec.param,
              apispec.verify, bin)


def test(apispec):
    if apispec.method == POST:
        fn = requests_post
    else:
        fn = requests_get
    # try:
    res = fn(apispec.fulluri,
             cookies=apispec.cookie,
             data=apispec.data,
             json=apispec.json,
             params=apispec.param,
             headers={**apispec.header, **__header},
             verify=apispec.verify,
             timeout=__timeout,
             stream=False)
    res.raise_for_status()
    # except Exception as e:
    #  	out.warn(f"unsuccessfull test HTTP {apisec.method} to "
    # 			 f"\"{apisec.fulluri}\": {e}")
    # else:
    out.debug(
        f"successfull test HTTP {apispec.method} to \"{apispec.fulluri}\"")
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
        out.error(
            f"unknown HTTP method in \"{method}\" (should be \"{METHOD}\")")
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
