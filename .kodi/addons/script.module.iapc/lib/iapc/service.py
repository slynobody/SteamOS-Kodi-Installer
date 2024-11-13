# -*- coding: utf-8 -*-


__all__ = ["public", "Service"]


from json import loads
from traceback import format_exc

from nuttig import getAddonId, Logger

from .client import Client
from .monitor import Monitor


# public -----------------------------------------------------------------------

def public(func):
    func.__public__ = True
    return func


# ------------------------------------------------------------------------------
# Service

class Service(Monitor):

    @staticmethod
    def __methods__(value, key=None):
        for name in dir(value):
            if (
                (not name.startswith("_")) and
                (callable(method := getattr(value, name))) and
                (getattr(method, "__public__", False))
            ):
                yield f"{key}.{name}" if key else name, method

    #def __registerWatcher__(self, id):
    #    self.logger.info(f"registering: '{id}'")
    #    if id != self.id:
    #        self.__watchers__.add(id)

    #def __settingsChanged__(self, id):
    #    if id not in self.__watchers__:
    #        self.logger.info(f"onSettingsChanged() triggered by: '{id}'")
    #        self.onSettingsChanged()
    #        # or maybe jut call containerRefresh() (less sketchy ?)

    def __init__(self):
        self.id = getAddonId()
        self.logger = Logger(self.id, component="service")
        self.methods = {}
        #self.__watchers__ = set()
        #self.__special_methods__ = {
        #    "__registerWatcher__": self.__registerWatcher__,
        #    "__settingsChanged__": self.__settingsChanged__
        #}
        #self.methods = dict(self.__methods__(self), **self.__special_methods__)

    def serve_forever(self, timeout):
        while not self.waitForAbort(timeout):
            pass

    def serve(self, timeout=-1, **kwargs):
        #self.methods.update(self.__methods__(self), **self.__special_methods__)
        #__inner_methods__ = {}
        #for key, value in kwargs.items():
        #    __inner_methods__.update(self.__methods__(value, key))
        #self.methods.update(__inner_methods__)
        self.methods.update(self.__methods__(self))
        for key, value in kwargs.items():
            self.methods.update(self.__methods__(value, key))
        try:
            self.serve_forever(timeout)
        finally:
            self.methods.clear() # clear possible circular references
            #while __inner_methods__:
            #    k, v = __inner_methods__.popitem()
            #    del self.methods[k]
            #self.__watchers__.clear()

    def execute(self, request):
        try:
            name, args, kwargs = loads(request)
            try:
                method = self.methods[name]
            except KeyError:
                raise AttributeError(f"no method '{name}'") from None
            return {"result": method(*args, **kwargs)}
        except Exception:
            error = format_exc().strip()
            self.logger.error(f"error processing request\n{error}")
            return {"error": error}

    def onNotification(self, sender, method, data):
        if sender == self.id:
            self.send(method.split(".", 1)[1], sender, self.execute(data))

    #def onSettingsChanged(self):
    #    # XXX: do NOT call this method unless you REALLY understand
    #    # what you're doing. it might lead you to hair pulling crashes...
    #    for watcher in self.__watchers__:
    #        self.logger.info(f"notifying: '{watcher}'")
    #        try:
    #            Client(watcher).__settingsChanged__(self.id)
    #        except Exception as error:
    #            self.logger.error(error)
