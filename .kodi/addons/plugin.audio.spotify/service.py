#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    plugin.audio.spotify
    Spotify player for Kodi
    Main service entry point
"""

if __name__ == "__main__":
    import platform
    import sys
    from resources.lib.utils import log_msg

    log_msg(f"Python version: {sys.version}.")
    log_msg(f"Python exe: {sys.executable}.")
    log_msg(f"Platform: {platform.platform()}.")

    from resources.lib.main_service import MainService

    MainService().run()
