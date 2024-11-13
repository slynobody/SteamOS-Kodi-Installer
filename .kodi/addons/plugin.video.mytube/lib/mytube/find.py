# -*- coding: utf-8 -*-


from json import JSONDecoder
from re import finditer, search


class MatchError(Exception):

    def __init__(self, msg):
        super(MatchError, self).__init__(f"No matches found for {msg}")


class PatternsError(MatchError):

    def __init__(self, *patterns):
        super(PatternsError, self).__init__(f"patterns: {patterns}")


def __find__(string, pattern):
    if (match := search(pattern, string)):
        return match
    raise PatternsError(pattern)


def __finditer__(string, pattern):
    if (matches := list(finditer(pattern, string))):
        return matches
    raise PatternsError(pattern)


def find(string, *patterns):
    for pattern in patterns:
        try:
            return JSONDecoder(strict=False).raw_decode(
                string[__find__(string, pattern).end():]
            )[0]
        except (PatternsError, ValueError):
            continue
    raise PatternsError(*patterns)


def findIter(string, *patterns):
    for pattern in patterns:
        for match in __finditer__(string, pattern):
            try:
                return JSONDecoder(strict=False).raw_decode(
                    string[match.end():]
                )[0]
            except (PatternsError, ValueError):
                continue
    raise PatternsError(*patterns)


def findInValues(values, pattern, callback):
    for value in values:
        if isinstance(value, str) and (pattern in value):
            callback(value)
        elif isinstance(value, list):
            findInValues(value, pattern, callback)
        elif isinstance(value, dict):
            findInValues(value.values(), pattern, callback)
