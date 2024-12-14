# -*- coding: utf-8 -*-

'''
    Copyright (C) 2023 realvito

    ARTE.TV

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from resources.lib.common import *
from resources.lib import navigator


def run():
	if mode == 'root':
		navigator.mainMenu()
	elif mode == 'listStartMag':
		navigator.listStartMag(url)
	elif mode == 'listThemes':
		navigator.listThemes(url)
	elif mode == 'listMusics':
		navigator.listMusics(url)
	elif mode == 'listShowContent':
		navigator.listShowContent(url, phrase, name, page)
	elif mode == 'listVideosDate':
		navigator.listVideosDate(url, extras)
	elif mode == 'listRunTime':
		navigator.listRunTime(url)
	elif mode == 'SearchARTE':
		navigator.SearchARTE()
	elif mode == 'playVideo':
		navigator.playVideo(url)
	elif mode == 'playLive':
		navigator.playLive(url, name)
	elif mode == 'liveTV':
		navigator.liveTV()
	elif mode == 'aConfigs':
		addon.openSettings()
		xbmc.executebuiltin('Container.Refresh')
	elif mode == 'iConfigs':
		xbmcaddon.Addon('inputstream.adaptive').openSettings()

run()
