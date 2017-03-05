from json import dumps, loads

from terminaltables import AsciiTable

from malsub.common import out


def tablevert(header, rows):
    return AsciiTable([header, *rows]).table


def jsonhoriz(json):
    tree = _jsonload(json)
    header = list(tree.keys())
    rows = list(tree.values())
    return AsciiTable([header, rows]).table


def jsonvert(json):
    tree = _jsonload(json)
    rows = [[k, tree[k]] for k in tree]
    header = [f"column ({len([i for i in rows])})"] + [
        "value"]  # * _depth(tree)
    return AsciiTable([header, *rows]).table


def _jsonload(json):
    if type(json) is dict:
        return json
    elif type(json) is str:
        try:
            tree = loads(json)
        except Exception as e:
            out.error(f"type \"{type(json)}\" invalid for parsing through JSON:"
                      f" {e}")
        else:
            return tree
    else:
        out.debug(f"type \"{type(json)}\" invalid for parsing through JSON")


def jsontree(json, depth=-1):
    tree = _jsonload(json)
    return _prune(tree, depth)


def jsondump(json, depth=-1):
    tree = _jsonload(json)
    return dumps(_prune(tree, depth), indent=2, sort_keys=True)


def _prune(obj, dep=-1, curr=0):
    if dep > 0:
        if curr == dep:
            if type(obj) is dict:
                obj = {}
            elif type(obj) is list:
                obj = []
            return obj
        else:
            if type(obj) is dict:
                return {k: _prune(obj[k], dep, curr + 1) for k in obj}
            elif type(obj) is list:
                return [_prune(i, dep, curr + 1) for i in obj]
            else:
                return obj
    else:
        return obj


def _depth(obj):
    if type(obj) is dict:
        return 1 + max(_depth(obj[a]) for a in obj)
    if type(obj) is list:
        return 1 + max(_depth(a) for a in obj)
    return 0


def xmlparse(xml):
    # import xml.etree.ElementTree
    # xml = ElementTree.fromstring(xml)
    from xml.dom.minidom import parseString
    xml = parseString(xml).toprettyxml(indent='  ')
    xml = "\n".join([s.rstrip() for s in xml.splitlines() if s.strip()])
    return xml
