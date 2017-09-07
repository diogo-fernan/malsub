from concurrent.futures import as_completed, ThreadPoolExecutor
from multiprocessing import cpu_count
from traceback import format_exc

from malsub.common import color, out
from malsub.service import base

__maxt = cpu_count()


def exec(anserv, fn, kwarg):
    anserv.setfn(fn)
    fn = [s for s in anserv if not s.fnhasattr(base.UNSUPPORTED)]
    # fn = {n: getattr(s(), fn) for n, s in anserv.items() if
    #    not hasattr(getattr(s, fn), base.UNSUPPORTED)}
    # kwarg = {n: {"apikey": s.get_apikey()} for n, s in anserv.items()}

    summ = {s.name: color.grayb("unsupported") for s in anserv}

    if fn:
        with ThreadPoolExecutor(__maxt) as tp:
            # fut = {tp.submit(f, **kwarg[n], **kwargs): n for n, f in fn.items()}
            fut = {tp.submit(s.fn, **kwarg): s for s in fn}
            # timeout=60 (sec) # does not work like this
            for f in as_completed(fut, timeout=None):
                try:
                    data = f.result()
                except base.UnsupportedAttr:
                    pass
                except Exception as e:
                    summ[fut[f].name] = color.redb("unsuccessful")
                    out.warn(f"\"{fut[f].name}\" -- \"{fut[f].fnname}\" "
                             f"error: {e}\n{color.red(format_exc())}")
                else:
                    summ[fut[f].name] = color.greenb("successful")
                    out.info(f"\"{fut[f].name}\" -- \"{fut[f].fnname}\" "
                             f"completed:\n{data}")

    return [summ[s.name] for s in anserv]
