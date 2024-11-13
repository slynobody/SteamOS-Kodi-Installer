# -*- coding: utf-8 -*-


import xbmc

from nuttig import executeJSONRPC


# ------------------------------------------------------------------------------
# Monitor

class Monitor(xbmc.Monitor):

    @staticmethod
    def send(sender, message, data):
        executeJSONRPC(
            "JSONRPC.NotifyAll", sender=sender, message=message, data=data
        )
