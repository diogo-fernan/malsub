from malsub.common import out, rw, util
from malsub.core import ascii, crypto, file, meta, serv, web
from malsub.service import base

# __NOINPUT = '\u2013'  # en-dash
__NOINPUT = '\u2014'  # em-dash

anserv = []
iarg = []
pause = 0


def run(arg, usage):
    def inarg():
        if (arg["--ipaddr"] or arg["--domain"] or arg["--appl"] or arg["--url"]) \
                and not (arg["--download"] or arg["--find"] or arg["--find"]
                         or arg["--report"] or arg["--submit"]):
            print(usage)
            exit(0)

        global iarg, pause
        try:
            pause = int(arg["--pause"])
            if int(pause) < 0:
                raise ValueError
        except ValueError:
            out.warn(f"invalid pause interval integer value \"{pause}\", "
                     f"defaulting to zero")
            pause = 0

        if arg["--test"]:
            iarg = base.Service.get_apifn()
        elif arg["--find"]:
            iarg = arg["<input>"]
        elif arg["--quota"]:
            iarg = __NOINPUT
        else:
            # domain
            if arg["--domain"]:
                iarg = web.parse_domainl(*arg["<input>"])
                if not iarg:
                    out.error("all input domain names are invalid")
            # ipaddr
            elif arg["--ipaddr"]:
                iarg = web.parse_ipaddrl(*arg["<input>"])
                if not iarg:
                    out.error("all input IP addresses are invalid")
            # url
            elif arg["--url"]:
                iarg = web.parse_fullurll(*arg["<input>"])
                if not iarg:
                    out.error("all input URLs are invalid")
            # file, hash
            else:
                from glob import glob
                from os.path import isdir, isfile, normpath

                if arg["--recursive"]:
                    tmp = [f for f in arg["<input>"] if isfile(f)]
                    for f in [normpath(f) for f in arg["<input>"] if isdir(f)]:
                        tmp += [f for f in
                                glob(f + meta.SEP + "**", recursive=True) if
                                isfile(f)]
                    tmp += [h for h in arg["<input>"] if
                            not isfile(h) and not isdir(h)]
                    arg["<input>"] = tmp

                if arg["--submit"]:
                    iarg = file.new(*arg["<input>"])
                elif arg["--report"]:  # file, hash
                    iarg = [f for f in arg["<input>"] if not isfile(f)]
                    tmp = [f for f in arg["<input>"] if isfile(f)]
                    if rw.validff(tmp):  # file
                        iarg += [crypto.sha256(f) for f in tmp]
                    iarg = crypto.parse_hashl(*iarg)  # hash
                else:  # arg["--download"]
                    if arg["<input>"]:
                        iarg = crypto.parse_hashl(*arg["<input>"])
                    else:
                        iarg = __NOINPUT
        out.debug("iarg", obj=iarg)

        if iarg != __NOINPUT and \
                not arg["--test"] and len(iarg) != len(arg["<input>"]):
            rw.yn("one or more input arguments are invalid")

    def loadserv():
        from malsub.service import serv as _serv
        global anserv

        out.debug("_serv", obj=_serv)
        if arg["--analysis"].lower() != "all":
            from re import findall
            anserv = [s for s in
                      list(findall(r"[\w-]+", arg["--analysis"].lower()))]
            notanserv = [s[1:] for s in anserv if s.startswith("-")]
            if "all" in anserv:
                anserv = [s for s in _serv if s not in notanserv]
            else:
                anserv = [s for s in anserv if s[1:] not in notanserv]

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
                if type(k) is not dict:
                    out.error(f"service \"{anserv[n].name}\" missing a valid API key \"{k}\"")
                elif k.get("apikey") is None:
                    out.error(f"service \"{anserv[n].name}\" missing a valid API key \"{k}\"")
                elif k.get("apikey") == "":
                    out.error(f"service \"{anserv[n].name}\" missing a valid API key \"{k}\"")
                elif k.get("apikey").get("api_key") == "<apikey>":
                    out.error(f"service \"{anserv[n].name}\" missing a valid API key \"{k}\"")
                else:
                    anserv[n].set_apikey(k)
            out.debug("apikey", obj=apikey)

    if arg["--verbose"] == 1:
        out.LEVEL = out.log.verb
    elif arg["--verbose"] > 1:
        out.LEVEL = out.log.debug
    out.debug("arg", obj=arg)

    inarg()
    loadserv()
    loadkey()
    ascii.banner()

    from malsub.common import frmt
    if arg["--servhelp"]:
        header = ["service", "description", "subscription", "url", "api"]
        summ = []
        for s in anserv:
            summ += [[s.obj.name] + s.obj.help()]
            pass
        out.info("\n" + frmt.tablevert(header, summ))
    else:
        from time import sleep, time
        from malsub.core.work import exec

        summ = []
        for i, j in enumerate(iarg):
            start = time()
            fn, kwarg = "", {}
            if arg["--test"]:
                fn = base.TEST_API
                kwarg = {"apifn": j}
            elif arg["--find"]:
                fn = base.SEARCH
                kwarg = {"srch": j}
            elif arg["--quota"]:
                fn = base.QUOTA
            else:
                # app
                if arg["--appl"]:
                    kwarg = {"hash": j}
                    fn = base.REPORT_APP
                # domain
                elif arg["--domain"]:
                    kwarg = {"dom": j}
                    if arg["--report"]:
                        fn = base.REPORT_DOM
                # ipaddr
                elif arg["--ipaddr"]:
                    kwarg = {"ip": j}
                    if arg["--report"]:
                        fn = base.REPORT_IP
                # url
                elif arg["--url"]:
                    kwarg = {"url": j}
                    if arg["--submit"]:
                        fn = base.SUBMIT_URL
                    elif arg["--report"]:
                        fn = base.REPORT_URL
                # file, hash
                else:
                    if arg["--submit"]:
                        fn = base.SUBMIT_FILE
                        kwarg = {"file": j}
                    elif arg["--report"]:
                        fn = base.REPORT_FILE
                        kwarg = {"hash": j}
                    elif arg["--download"]:
                        fn = base.DOWNLOAD_FILE
                        kwarg = {"hash": j}

            if fn:  # and kwarg:
                summ += [[i + 1, util.trunc(j), *exec(anserv, fn, kwarg)]]

            if i < len(iarg) - 1 and time() - start < pause:
                nap = pause - (time() - start)
                out.verb(f"sleeping for {nap} seconds")
                sleep(nap)
        file.close(iarg)

        header = ["#", "input"] + [s.obj.name for s in anserv]
        out.verb(f"{meta.MALSUB_NAME} finished with results:\n"
                 f"{frmt.tablevert(header, summ)}")

    return
