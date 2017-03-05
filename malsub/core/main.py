from malsub.common import out, rw, util
from malsub.core import ascii, crypto, file, meta, serv, web
from malsub.service import base

# __NOINPUT = '\u2013'  # en-dash
__NOINPUT = '\u2014'  # em-dash

anserv = []
ina = []
pause = 0


def run(arg):
    def loadserv():
        from malsub.service import serv as _serv
        global anserv

        out.debug("_serv", obj=_serv)
        if arg["--analysis"].lower() != "all":
            from re import findall
            anserv = list(findall(r"\w+", arg["--analysis"].lower()))

            inv = [s for s in anserv if s not in _serv]
            if inv:
                out.error(f"input service(s) \"{','.join(inv)}\" unknown")
            anserv = serv.ServiceList([s for s in _serv if s in anserv])
        else:
            anserv = serv.ServiceList([s for s in _serv])
        out.debug("anserv", obj=anserv)

    def loadkey():
        from yaml import safe_load as loadyaml
        from yaml.scanner import ScannerError
        global anserv

        try:
            apikey = {n.lower(): k for n, k in
                      loadyaml(open(meta.APIKEY_PATH)).items() if
                      n.lower() in anserv}
        except IOError as e:
            out.error(f"cannot open API keys file \"{meta.APIKEY_PATH}\": {e}")
        except ScannerError as e:
            out.error(f"cannot load API keys file \"{meta.APIKEY_PATH}\": {e}")
        else:
            for n, k in apikey.items():
                if type(k) is not dict or k.get("apikey") is None:
                    out.error(f"service \"{anserv[n].name}\" missing "
                              f"a valid API key \"{k}\"")
                else:
                    anserv[n].set_apikey(k)
            out.debug("apikey", obj=apikey)

    def inarg():
        global ina, pause
        try:
            pause = int(arg["--pause"])
            if int(pause) < 0:
                pause = 0
        except ValueError:
            out.warn(f"invalid pause interval integer value \"{pause}\", "
                     f"defaulting to zero")

        if arg["--test"]:
            ina = base.Service.get_apifn()
        elif arg["--find"]:
            ina = arg["<input>"]
        elif arg["--quota"]:
            ina = __NOINPUT
        else:
            # domain
            if arg["--domain"]:
                ina = web.parse_domainl(*arg["<input>"])
                if not ina:
                    out.error("all input domain names are invalid")
            # ipaddr
            elif arg["--ipaddr"]:
                ina = web.parse_ipaddrl(*arg["<input>"])
                if not ina:
                    out.error("all input IP addresses are invalid")
            # url
            elif arg["--url"]:
                ina = web.parse_fullurll(*arg["<input>"])
                if not ina:
                    out.error("all input URLs are invalid")
            # file, hash
            else:
                if arg["--submit"]:
                    ina = file.new(*arg["<input>"])
                elif arg["--report"]:
                    # ina = arg["<input>"]
                    ina = crypto.parse_hashl(*arg["<input>"])
                else:  # arg["--download"]
                    if arg["<input>"]:
                        ina = crypto.parse_hashl(*arg["<input>"])
                    else:
                        ina = __NOINPUT
        out.debug("ina", obj=ina)

        if ina != __NOINPUT and not arg["--test"] and len(ina) != len(
                arg["<input>"]):
            rw.yn("one or more input arguments are invalid")

    if arg["--verbose"] == 1:
        out.LEVEL = out.log.verb
    if arg["--verbose"] > 1:
        out.LEVEL = out.log.debug
    out.debug("arg", obj=arg)

    loadserv()
    loadkey()
    ascii.banner()
    inarg()

    from time import sleep, time
    from malsub.core.work import exec

    summ = []
    for i, j in enumerate(ina):
        start = time()
        fn, kwargs = "", {}
        if arg["--test"]:
            fn = base.TEST_API
            kwargs = {"apifn": j}
        elif arg["--find"]:
            fn = base.SEARCH
            kwargs = {"srch": j}
        elif arg["--quota"]:
            fn = base.QUOTA
        else:
            # app
            if arg["--appl"]:
                kwargs = {"hash": j}
                fn = base.REPORT_APP
            # domain
            elif arg["--domain"]:
                kwargs = {"dom": j}
                if arg["--report"]:
                    fn = base.REPORT_DOM
            # ipaddr
            elif arg["--ipaddr"]:
                kwargs = {"ip": j}
                if arg["--report"]:
                    fn = base.REPORT_IP
            # url
            elif arg["--url"]:
                kwargs = {"url": j}
                if arg["--submit"]:
                    fn = base.SUBMIT_URL
                elif arg["--report"]:
                    fn = base.REPORT_URL
            # file, hash
            else:
                if arg["--submit"]:
                    fn = base.SUBMIT_FILE
                    kwargs = {"file": j}
                elif arg["--report"]:
                    fn = base.REPORT_FILE
                    kwargs = {"hash": j}
                elif arg["--download"]:
                    fn = base.DOWNLOAD_FILE
                    kwargs = {"hash": j}

        if fn:  # and kwargs:
            summ += [[i + 1, util.trunc(j), *exec(anserv, fn, kwargs)]]

        if i < len(ina) - 1 and time() - start < pause:
            nap = pause - (time() - start)
            out.verb(f"sleeping for {nap} seconds")
            sleep(nap)
    file.close(ina)

    from malsub.common import frmt
    header = ["#", "input"] + [s.obj.name for s in anserv]
    out.verb(f"{meta.MALSUB_NAME} finished with results:\n"
             f"{frmt.tablevert(header, summ)}")

    return
