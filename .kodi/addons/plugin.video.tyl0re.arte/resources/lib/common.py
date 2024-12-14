# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import xbmcvfs
import time
from datetime import datetime, timedelta
from calendar import timegm as TGM
import requests
from urllib.parse import parse_qsl, urlencode, quote, unquote, unquote_plus
from urllib.request import urlopen
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from .provider import Client


HOST_AND_PATH               = sys.argv[0]
ADDON_HANDLE                = int(sys.argv[1])
dialog                                   = xbmcgui.Dialog()
addon                                   = xbmcaddon.Addon()
addon_id                             = addon.getAddonInfo('id')
addon_name                       = addon.getAddonInfo('name')
addon_version                    = addon.getAddonInfo('version')
addonPath                           = xbmcvfs.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath                              = xbmcvfs.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
searchHackFile                    = os.path.join(dataPath, 'searchString')
defaultFanart                      = os.path.join(addonPath, 'resources', 'media', 'fanart.jpg')
icon                                      = os.path.join(addonPath, 'resources', 'media', 'icon.png')
artpic                                    = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
evepic                                   = os.path.join(addonPath, 'resources', 'media', 'events', '').encode('utf-8').decode('utf-8')
thepic                                   = os.path.join(addonPath, 'resources', 'media', 'themes', '').encode('utf-8').decode('utf-8')
COUNTRY                             = {0: 'de', 1: 'fr'}[int(addon.getSetting('language'))]
enableINPUTSTREAM         = addon.getSetting('useInputstream') == 'true'
prefSTREAM                         = addon.getSetting('prefer_stream')
LIMIT_NUMBER                  = int(addon.getSetting('entry_limitation'))
useThumbAsFanart             = addon.getSetting('useThumbAsFanart') == 'true'
enableADJUSTMENT           = addon.getSetting('show_settings') == 'true'
DEB_LEVEL                          = (xbmc.LOGINFO if addon.getSetting('enableDebug') == 'true' else xbmc.LOGDEBUG)
KODI_ov20                          = int(xbmc.getInfoLabel('System.BuildVersion')[0:2]) >= 20
BASE_URL                            = 'https://www.arte.tv/'
API_URL                               = 'https://api-cdn.arte.tv/api/emac/v3/'+COUNTRY+'/web/'
OPA_token                           = 'AOwImM4EGZ2gjYjRGZzEzYxMTNxMWOjJDO4gDO3UWN3UmN5IjNzAzMlRmMwEWM2I2NhFWN1kjYkJjZ1cjY1czN reraeB'
EMAC_token                        = 'wYxYGNiBjNwQjZzIjMhRDOllDMwEjM2MDN3MjY4U2M1ATYkVWOkZTM5QzM4YzN2ITM0E2MxgDO1EjN5kjZmZWM reraeB'
PLAY_token                         = 'QMjZTOkF2NwQDZlFTOmJDOiFGN1QGM4EjY5QWOhBzN4YzM4YGMiRTNjZjZyImMjFWZlRWZ3Q2Y1MmYyYDZyYzM reraeB'
traversing                            = Client(Client.CONFIG_ARTE)

xbmcplugin.setContent(ADDON_HANDLE, 'movies')

def py3_dec(d, nom='utf-8', ign='ignore'):
	if isinstance(d, bytes):
		d = d.decode(nom, ign)
	return d

def translation(id):
	return addon.getLocalizedString(id)

def failing(content):
	log(content, xbmc.LOGERROR)

def debug_MS(content):
	log(content, DEB_LEVEL)

def log(msg, level=xbmc.LOGINFO):
	return xbmc.log('[{} v.{}]{}'.format(addon_id, addon_version, str(msg)), level)

def get_userAgent(REV='109.0', VER='112.0'):
	base = 'Mozilla/5.0 {} Gecko/20100101 Firefox/'+VER
	if xbmc.getCondVisibility('System.Platform.Android'):
		if 'arm' in os.uname()[4]: return base.format('(X11; Linux arm64; rv:'+REV+')') # ARM based Linux
		return base.format('(X11; Linux x86_64; rv:'+REV+')') # x64 Linux
	elif xbmc.getCondVisibility('System.Platform.Windows'):
		return base.format('(Windows NT 10.0; Win64; x64; rv:'+REV+')') # Windows
	elif xbmc.getCondVisibility('System.Platform.IOS'):
		return 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1' # iOS iPhone/iPad
	elif xbmc.getCondVisibility('System.Platform.Darwin') or xbmc.getCondVisibility('System.Platform.OSX'):
		return base.format('(Macintosh; Intel Mac OS X 10.15; rv:'+REV+')') # Mac OSX
	return base.format('(X11; Linux x86_64; rv:'+REV+')') # x64 Linux

def _header(REFERRER=None, USERTOKEN=None):
	header = {}
	header['Connection'] = 'keep-alive'
	header['Cache-Control'] = 'no-cache'
	header['User-Agent'] = get_userAgent()
	header['DNT'] = '1'
	header['Upgrade-Insecure-Requests'] = '1'
	header['Accept-Encoding'] = 'gzip'
	header['Accept-Language'] = 'en-US,en;q=0.8,de;q=0.7'
	if REFERRER:
		header['Referer'] = REFERRER
	if USERTOKEN:
		header['Authorization'] = USERTOKEN[::-1]
	return header

def getUrl(url, method='GET', REF=None, AUTH=None, headers=None, cookies=None, allow_redirects=False, verify=True, stream=None, data=None, json=None):
	simple = requests.Session()
	ANSWER = None
	try:
		response = simple.get(url, headers=_header(REF, AUTH), allow_redirects=allow_redirects, verify=verify, stream=stream, timeout=30)
		ANSWER = response.json() if method in ['GET', 'POST'] else response.text
		debug_MS("(common.getUrl) === CALLBACK === status : {} || url : {} || header : {} ===".format(str(response.status_code), response.url, _header(REF, AUTH)))
	except requests.exceptions.RequestException as e:
		failing("(common.getUrl) ERROR - ERROR - ERROR ##### url: {} === error: {} #####".format(url, str(e)))
		dialog.notification(translation(30521).format('URL'), translation(30523).format(str(e)), icon, 12000)
		return sys.exit(0)
	return ANSWER

def ADDON_operate(IDD):
	check_1 = xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "id":1, "method":"Addons.GetAddonDetails", "params":{{"addonid":"{}", "properties":["enabled"]}}}}'.format(IDD))
	check_2 = 'undone'
	if '"enabled":false' in check_1:
		try:
			xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "id":1, "method":"Addons.SetAddonEnabled", "params":{{"addonid":"{}", "enabled":true}}}}'.format(IDD))
			failing("(common.ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *{}* ist NICHT aktiviert !!! #####\n##### Es wird jetzt versucht die Aktivierung durchzuführen !!! #####".format(IDD))
		except: pass
		check_2 = xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "id":1, "method":"Addons.GetAddonDetails", "params":{{"addonid":"{}", "properties":["enabled"]}}}}'.format(IDD))
	if '"error":' in check_1 or '"error":' in check_2:
		dialog.ok(addon_id, translation(30501).format(IDD))
		failing("(common.ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *{}* ist NICHT installiert !!! #####".format(IDD))
		return False
	if '"enabled":true' in check_1 or '"enabled":true' in check_2:
		return True
	if '"enabled":false' in check_2:
		dialog.ok(addon_id, translation(30502).format(IDD))
		failing("(common.ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *{}* ist NICHT aktiviert !!! #####\n##### Eine automatische Aktivierung ist leider NICHT möglich !!! #####".format(IDD))
	return False

def get_Local_DT(info):
	fixed_format = '%Y{0}%m{0}%dT%H{1}%M{1}%S'.format('-', ':') # 2019-06-13T13:30:00Z
	utcDT = datetime(*(time.strptime(info, fixed_format)[0:6]))
	try:
		localDT = datetime.fromtimestamp(TGM(utcDT.timetuple()))
		assert utcDT.resolution >= timedelta(microseconds=1)
		localDT = localDT.replace(microsecond=utcDT.microsecond)
	except (ValueError, OverflowError): # ERROR on Android 32bit Systems = cannot convert unix timestamp over year 2038
		localDT = datetime.fromtimestamp(0) + timedelta(seconds=TGM(utcDT.timetuple()))
		localDT = localDT - timedelta(hours=datetime.timetuple(localDT).tm_isdst)
	return localDT

def get_Description(info):
	if 'fullDescription' in info and info['fullDescription'] and len(info['fullDescription']) > 10:
		return cleaning(info['fullDescription'])
	elif 'description' in info and info['description'] and len(info['description']) > 10:
		return cleaning(info['description'])
	elif 'shortDescription' in info and info['shortDescription'] and len(info['shortDescription']) > 10:
		return cleaning(info['shortDescription'])
	return ""

def get_Picture(elem_id, resources, elem_type):
	if resources.get(elem_type, '') and resources.get(elem_type, {}).get('blurUrl', ''):
		return resources[elem_type]['resolutions'][-1]['url']
	return None

def getSorting():
	return [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_DATE, xbmcplugin.SORT_METHOD_DURATION]

def cleaning(text):
	if text is not None:
		text = text.strip()
	return text

params = dict(parse_qsl(sys.argv[2][1:]))
name = unquote_plus(params.get('name', ''))
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', 'root'))
page = unquote_plus(params.get('page', '1'))
phrase = unquote_plus(params.get('phrase', 'standard'))
extras = unquote_plus(params.get('extras', 'standard'))
