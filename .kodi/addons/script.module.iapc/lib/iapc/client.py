# -*- coding: utf-8 -*-


__all__ = ["AddonNotAvailable", "Client", "RequestError"]


from json import loads
from uuid import uuid4

from nuttig import addonIsEnabled, getAddonId

from .monitor import Monitor


# ------------------------------------------------------------------------------
# Request

class RequestError(Exception):

    def __init__(self, message="unknown request error"):
        super(RequestError, self).__init__(message)


class Request(Monitor):

    def __init__(self, id):
        self.id = id
        self.message = uuid4().hex
        self.response = RequestError()
        self.ready = False

    def execute(self, request):
        self.send(self.id, self.message, request)
        while not self.ready:
            if self.waitForAbort(0.1):
                self.response = RequestError("request aborted")
                break
        if isinstance(self.response, Exception):
            raise self.response
        return self.response

    def handle(self, response):
        try:
            response = loads(response)
            try:
                self.response = response["result"]
            except KeyError:
                self.response = RequestError(
                    f"remote error\n{response['error']}"
                )
        except Exception as error:
            self.response = error
        finally:
            self.ready = True

    def onNotification(self, sender, method, data):
        if sender == self.message and method.split(".", 1)[1] == self.id:
            self.handle(data)


# ------------------------------------------------------------------------------
# Client

class AddonNotAvailable(Exception):

    def __init__(self, id):
        super(AddonNotAvailable, self).__init__(
            f"addon '{id}' is not installed or not enabled"
        )


class Attribute(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __getattr__(self, name):
        return Attribute(self.id, f"{self.name}.{name}")

    def __call__(self, *args, **kwargs):
        return Request(self.id).execute((self.name, args, kwargs))


class Client(object):

    #def __init__(self, id=None, register=False):
    #    if id and (not addonIsEnabled(id)):
    #        raise AddonNotAvailable(id)
    #    self.__id__ = getAddonId()
    #    self.id = id or self.__id__
    #    if register and (self.id != self.__id__):
    #        self.__registerWatcher__(self.__id__)

    def __init__(self, id=None):
        if id and (not addonIsEnabled(id)):
            raise AddonNotAvailable(id)
        self.__id__ = getAddonId()
        self.id = id or self.__id__

    def __getattr__(self, name):
        return Attribute(self.id, name)

