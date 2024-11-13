# -*- coding: utf-8 -*-


__all__ = ["parseQuery", "buildUrl", "urlReplace"]


from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


# parseQuery -------------------------------------------------------------------

__parse_consts__ = {
    "none": None,
    "true": True,
    "false": False
}

def parseValue(value):
    try:
        return __parse_consts__[value.lower()]
    except KeyError:
        return value

def parseQuery(query):
    return {
        k: parseValue(v)
        for k, v in parse_qsl(query.lstrip("?"))
    }


#  buildUrl --------------------------------------------------------------------

def buildUrl(*args, **kwargs):
    url = "/".join(args)
    return "?".join((url, urlencode(kwargs))) if kwargs else url


#  urlReplace ------------------------------------------------------------------

def urlReplace(url, **kwargs):
    return urlunsplit(urlsplit(url)._replace(**kwargs))
