# -*- coding: utf-8 -*-

from .common import *


def get_ListItem(info, category, phrase, extras, folder=True, STOCK=False):
	config = traversing.get_config()
	tagline, Note_1 = ("" for _ in range(2))
	seriesname, startTIMES, begins, endTIMES, mpaa, uvz, duration, POSTER, THUMB, BANNER = (None for _ in range(10))
	FANART = defaultFanart
	IDD = (info.get('id', None) or None)
	IDD = IDD.split('_')[0] if IDD and '_' in IDD else IDD
	PID = (info.get('programId', None) or None)
	title = cleaning(info['title']).replace('event teaser', 'Special')
	if str(title)[:10].upper() in ['BANNER TEM', 'ZONE EVENT'] and info.get('data', '') and len(info['data']) > 0:
		title = cleaning(info['data'][0]['title'])+'  [COLOR lime](Special)[/COLOR]'
	tagline = (cleaning(info.get('teaserText', '')) or "")
	if tagline and len(tagline) > 125:
		tagline = tagline[:125]+'...'
	if info.get('availability', ''):
		if category == 'DATA_TRE' and str(info['availability'].get('upcomingDate'))[:4] not in ['None', '0', '1970']:
			LOCALupcom = get_Local_DT(info['availability']['upcomingDate'][:19])
			title = "[COLOR orange]{0}[/COLOR]  {1}".format(LOCALupcom.strftime('%H:%M'), title)
		if str(info['availability'].get('start'))[:4] not in ['None', '0', '1970']:
			LOCALstart = get_Local_DT(info['availability']['start'][:19])
			startTIMES = LOCALstart.strftime('%d{0}%m{0}%y {1} %H{2}%M').format('.', '•', ':')
			begins = LOCALstart.strftime('%d{0}%m{0}%Y').format('.')
		if str(info['availability'].get('end'))[:4] not in ['None', '0', '1970']:
			LOCALend = get_Local_DT(info['availability']['end'][:19])
			endTIMES = LOCALend.strftime('%d{0}%m{0}%y {1} %H{2}%M').format('.', '•', ':')
	if str(info.get('ageRating')).isdigit() and str(info.get('ageRating')) != '0':
		mpaa = translation(32201).format(str(info['ageRating'])) if COUNTRY == 'de' else translation(32203).format(str(info['ageRating']))
	if category in ['ZONE_ONE', 'ZONE_TWO']:
		FOLLOW = 'listShowContent'
		if info.get('code', '') and str(info['code'].get('name')).lower() in ['collection_videos', 'collection_subcollection']:
			gangway = '111'
			collection = info['code']['name'].upper()
			CID = info['code']['id']
			newREV = config['collections_one'].format(API_URL, collection, CID)
			if collection == 'COLLECTION_SUBCOLLECTION':
				newREV = config['collections_two'].format(API_URL, collection, CID.split('_')[0], CID.split('_')[1])
		else:
			if info.get('link', '') and info.get('link', {}).get('deeplink', '') and not title.lower().startswith(('meistgesehene ', 'letzte chance')) and not title.lower().endswith((' les plus vues', 'dernière chance')):
				gangway = '222'
				SHORTEN = info['link']['deeplink'].split('/')[-1] if 'emac' in info['link']['deeplink'] or 'collection' in info['link']['deeplink'] else info['link']['page']
				newREV = API_URL+SHORTEN+'/'
				if len(SHORTEN) == 3 and SHORTEN not in ['DOR', 'CIN', 'SER', 'ACT', 'CPO', 'ARS', 'SCI', 'DEC', 'HIS', 'EMI']: # Manche Links von 'link.page' funktionieren nicht daher zuerst 'link.deeplink' versuchen
					newREV = config['codes_one'].format(API_URL, SHORTEN)
			elif str(info.get('nextPage'))[:4] == 'http':
				gangway = '333'
				CLEARED = re.sub(r'(?:authorizedAreas=.*?&|abv=[A-Z]+&|&page=[0-9]+|&limit=[0-9]+)', '', info['nextPage'])
				CLEARED = re.sub(r'imageFormats=.*?&', 'imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&', CLEARED)
				newREV = 'https://api-cdn.arte.tv/api/emac/'+CLEARED.split('emac/')[1].replace('&imageWithText=true', '')+'&imageWithText=true'
			elif title.lower().startswith(('meistgesehene ', 'letzte chance')) or title.lower().endswith((' les plus vues', 'dernière chance')): # z.b. MOST_VIEWED auf der Startseite
				gangway = '444'
				CATY = 'category={}&'.format(phrase) if phrase in ['ACT', 'SCI', 'DEC', 'HIS', 'CIN', 'SER'] else "" 
				MOLA = 'LAST_CHANCE' if phrase in ['CIN', 'SER'] else 'MOST_VIEWED'
				newREV = config['categories_two'].format(API_URL, CATY, MOLA)
			elif IDD in ['3f77e1b5-a6c8-49b1-bd1a-3585d9c8ef88', '67747aea-5426-4b45-8ef4-f648fd227a69', 'ee9b8a20-d001-49b8-b284-1f7750a4bfc6', 'cbde5425-226c-4638-b9f6-6847e509db7f']:
				# 1.Musik entdecken(f88)+2.Alle Kategorien(a69) // 3.Parcourir les genres(fc6)+4.Parcourir toute l'offre(b7f)
				gangway = '555'
				FOLLOW = 'listMusics' if IDD in ['3f77e1b5-a6c8-49b1-bd1a-3585d9c8ef88', 'ee9b8a20-d001-49b8-b284-1f7750a4bfc6'] else 'listThemes'
				newREV = 'https://api.arte.tv/api/opa/v3/categories?language={}&limit=50'.format(COUNTRY) if IDD in ['3f77e1b5-a6c8-49b1-bd1a-3585d9c8ef88', 'ee9b8a20-d001-49b8-b284-1f7750a4bfc6'] else API_URL+'MENU/'
			else:
				gangway = '666'
				newREV = config['codes_two'].format(API_URL, info['code']['name'], IDD)
		uvz = '{0}?{1}'.format(HOST_AND_PATH, urlencode({'mode': FOLLOW, 'url': newREV, 'phrase': 'OVERVIEW', 'name': title}))
	elif category in ['DATA_ONE', 'DATA_TWO', 'DATA_TRE'] and str(PID) not in ['', 'None']:
		if info.get('kind', '') and (info.get('kind', {}).get('code', '') == "MAGAZINE" or info.get('kind', {}).get('isCollection', '') is True):
			gangway = '777'
			newREV = API_URL+str(PID)+'/'
			uvz = '{0}?{1}'.format(HOST_AND_PATH, urlencode({'mode': 'listShowContent', 'url': newREV, 'phrase': 'PLAYLIST', 'name': title}))
		else:
			gangway = '888'
			newREV = str(PID)
			uvz = '{0}?{1}'.format(HOST_AND_PATH, urlencode({'mode': 'playVideo', 'url': PID}))
			folder = False
			duration = int(info['duration']) if str(info.get('duration')).isdigit() else None
	else:
		gangway, newREV, uvz = 'NULL', 'UNKNOWN', None
	if info.get('availability', '') and info.get('availability', {}).get('type', '') == 'LIVESTREAM_WEB': newREV, uvz = 'LIVESTREAM_WEB', None # 1. noch nicht vorh. Videos // 2. z.b. Das Wichtigste in Kürze unter Aktuelles und Gesellschaft
	if info.get('subtitle', ''):
		if not folder: title = title+' - '+cleaning(info['subtitle'])
		else: tagline = cleaning(info['subtitle'])
	if startTIMES and endTIMES:
		Note_1 = translation(32205).format(str(startTIMES), str(endTIMES)) if COUNTRY == 'de' else translation(32206).format(str(startTIMES), str(endTIMES))
	elif startTIMES and endTIMES is None:
		Note_1 = translation(32207).format(str(startTIMES)) if COUNTRY == 'de' else translation(32208).format(str(startTIMES))
	if not folder:
		for method in getSorting(): xbmcplugin.addSortMethod(ADDON_HANDLE, method)
	LEM = xbmcgui.ListItem(title)
	plot = Note_1+get_Description(info)
	if plot == '': plot = '...'
	if KODI_ov20:
		videoInfoTag = LEM.getVideoInfoTag()
		videoInfoTag.setTvShowTitle(seriesname)
		videoInfoTag.setTitle(title)
		videoInfoTag.setTagLine(tagline)
		videoInfoTag.setPlot(plot)
		if duration: videoInfoTag.setDuration(int(duration))
		if begins: videoInfoTag.setDateAdded(begins)
		if begins: videoInfoTag.setFirstAired(begins)
		videoInfoTag.setStudios(['ARTE'])
		videoInfoTag.setMpaa(mpaa)
		if not folder: videoInfoTag.setMediaType('movie')
	else:
		ilabels = {}
		ilabels['Tvshowtitle'] = seriesname
		ilabels['Title'] = title
		ilabels['Tagline'] = tagline
		ilabels['Plot'] = plot
		if duration: ilabels['Duration'] = duration
		if begins: ilabels['Date'] = begins
		if begins: ilabels['Aired'] = begins
		ilabels['Studio'] = 'ARTE'
		ilabels['Mpaa'] = mpaa
		if not folder: ilabels['Mediatype'] = 'movie'
		LEM.setInfo(type='Video', infoLabels=ilabels)
	if info.get('images', ''):
		num, resources, STOCK = info.get('id', ''), info.get('images', []), True
	if not STOCK and info.get('data', '') and len(info['data']) > 0 and info['data'][0].get('images', ''):
		num, resources, STOCK = info.get('id', ''), info['data'][0].get('images', []), True
	if STOCK:
		POSTER = (get_Picture(num, resources, 'portrait') or get_Picture(num, resources, 'square'))
		THUMB = (get_Picture(num, resources, 'landscape') or get_Picture(num, resources, 'square'))
		BANNER = get_Picture(num, resources, 'banner')
		FANART = (get_Picture(num, resources, 'landscape') or defaultFanart)
	if not folder:
		LEM.setProperty('IsPlayable', 'true')
		LEM.setContentLookup(False)
		LEM.setArt({'icon': icon, 'thumb': THUMB, 'poster': THUMB, 'banner': BANNER, 'fanart': defaultFanart}) # POSTER werden bei Videos abgeschnitten dargestellt
		LEM.addContextMenuItems([(translation(32154), 'Action(Queue)')])
	else:
		LEM.setArt({'icon': icon, 'thumb': THUMB, 'poster': POSTER, 'banner': BANNER, 'fanart': defaultFanart})
	if useThumbAsFanart:
		LEM.setArt({'fanart': FANART})
	if extras:
		debug_MS(extras+" ### TITLE = {} || CATEGORY = {} || CALLno. = {} ###".format(title, str(category), gangway))
		debug_MS(extras+" ### URL = {} || is FOLDER = {} || DURATION = {} ###".format(newREV, str(folder), str(duration)))
		debug_MS(extras+" ### POSTER = {} || THUMB = {} ###".format(str(POSTER), str(THUMB)))
	return (uvz, LEM, folder)
