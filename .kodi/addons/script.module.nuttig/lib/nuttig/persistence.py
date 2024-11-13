# -*- coding: utf-8 -*-


__all__ = ["dumpObject", "loadObject", "Persistent", "save"]


from pathlib import Path
from json import dump, load

from .addon import getAddonProfile


# json -------------------------------------------------------------------------

def dumpObject(obj, path):
    with path.open("w+") as f:
        dump(obj, f)


def loadObject(path, default=None):
    if path.exists():
        with path.open("r") as f:
            return load(f)
    return default


# ------------------------------------------------------------------------------
# Persistent

def save(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            self.__save__()
    return wrapper


class Persistent(object):

    def __init_subclass__(cls, **kwargs):
        cls.__path__ = Path(
            getAddonProfile(),
            getattr(cls, "__filename__", f"{cls.__name__.lower()}.json")
        )
        super(Persistent, cls).__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        if not self.__path__.exists():
            super(Persistent, self).__init__(*args, **kwargs)
        else:
            with self.__path__.open("r") as f:
                super(Persistent, self).__init__(load(f))

    def __save__(self):
        with self.__path__.open("w+") as f:
            dump(self, f)
