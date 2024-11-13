# -*- coding: utf-8 -*-


from iapc import Client
from nuttig import addonIsEnabled, localizedString, okDialog


# ------------------------------------------------------------------------------
# YtDlpHls

class YtDlpHls(object):

    __service_id__ = "service.playlists.hls"

    def __init__(self, logger):
        self.logger = logger.getLogger(f"{logger.component}.hls")

    def __setup__(self):
        pass

    def __stop__(self):
        self.logger.info("stopped")

    # --------------------------------------------------------------------------

    def __playlist__(self, url, **kwargs):
        if addonIsEnabled(self.__service_id__):
            return Client(self.__service_id__).playlist(url, **kwargs)
        okDialog(localizedString(90004).format(self.__service_id__))

    # playlist -----------------------------------------------------------------

    def playlist(self, url, live=False, **kwargs):
        if (live and ("proxy" in kwargs)):
            return self.__playlist__(url, **kwargs)
        return url
