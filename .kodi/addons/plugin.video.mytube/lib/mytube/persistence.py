# -*- coding: utf-8 -*-


from collections import OrderedDict

from nuttig import save, Persistent


# ------------------------------------------------------------------------------
# MyNavigationHistory

class MyNavigationHistory(Persistent, dict):

    def __missing__(self, action):
        self[action] = list()
        return self[action]

    def __push__(self, action, key, value):
        if ((item := {key: value}) in self[action]):
            self[action] = self[action][:self[action].index(item)]
        try:
            return self[action][-1]
        except IndexError:
            return None
        finally:
            self[action].append(item)

    @save
    def page(self, action, page):
        if (page == 1):
            self[action].clear()
        return self.__push__(action, "page", page)

    @save
    def continuation(self, action, continuation):
        if (not continuation):
            self[action].clear()
        return self.__push__(action, "continuation", continuation)

    @save
    def clear(self):
        super(MyNavigationHistory, self).clear()


# ------------------------------------------------------------------------------
# MySearchHistory

class MySearchHistory(Persistent, OrderedDict):

    def __init__(self, *args, **kwargs):
        old = migrate("mysearchhistory.json")
        super(MySearchHistory, self).__init__(*args, **kwargs)
        if old:
            for k, v in old.items():
                for q in v.values():
                    self.record(
                        {
                            "query": q["query"],
                            "type": q["type"][:-1],
                            "sort": q["sort_by"]
                        }
                    )

    @save
    def record(self, query):
        self[(q := query["query"])] = query
        super(MySearchHistory, self).move_to_end(q)

    @save
    def remove(self, q):
        del self[q]

    @save
    def clear(self):
        super(MySearchHistory, self).clear()

    @save
    def move_to_end(self, q):
        super(MySearchHistory, self).move_to_end(q)


# ------------------------------------------------------------------------------
# MyFeedChannels

class MyFeedChannels(Persistent, OrderedDict):

    def __init__(self, *args, **kwargs):
        old = migrate("mychannelfeed.json")
        super(MyFeedChannels, self).__init__(*args, **kwargs)
        if old:
            for k, v in old.items():
                self.add(k, v)

    @save
    def add(self, key, value):
        self[key] = value

    @save
    def remove(self, key):
        del self[key]

    @save
    def clear(self):
        super(MyFeedChannels, self).clear()


# ------------------------------------------------------------------------------

# this should take care of migrating old data
# (I really, REALLY, hope...)

import json
import pathlib
import shutil

from nuttig import getAddonProfile, Logger

def migrate(name):
    old = None
    if (
        ((path := pathlib.Path(getAddonProfile(), name)).exists()) and
        (not (backup := path.with_name(f"{path.name}.bak")).exists())
    ):
        logger = Logger()
        logger.info(f"migrating path: {path}")
        logger.info(f"backup: {backup}")
        try:
            shutil.copyfile(path, backup)
            with open(path, "r") as f:
                old = json.load(f)
        except Exception as err:
            logger.error(f"failed to migrate: {err}")
        else:
            path.unlink()
    return old
