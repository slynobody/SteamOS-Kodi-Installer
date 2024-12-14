# -*- coding: utf-8 -*-

from .common import *
from .records import get_ListItem


if not xbmcvfs.exists(dataPath):
	xbmcvfs.mkdirs(dataPath)

def mainMenu():
	config = traversing.get_config()
	for pick in config['picks']:
		title = pick['title_de'] if COUNTRY == 'de' else pick['title_fr']
		action = pick['action']
		INLAY = API_URL if pick.get('action') != 'listMusics' else COUNTRY
		url = pick.get('url').format(INLAY) if pick.get('url') is not None else '00'
		img = pick.get('img').format(artpic) if pick.get('img') is not None else icon
		if action not in ['aConfigs', 'iConfigs']:
			addDir(title, img, {'mode': action, 'url': url})
		if enableADJUSTMENT and action == 'aConfigs':
			addDir(title, img, {'mode': 'aConfigs'}, folder=False)
			if enableINPUTSTREAM and ADDON_operate('inputstream.adaptive') and action == 'iConfigs':
				addDir(title, img, {'mode': 'iConfigs'}, folder=False)
	if not ADDON_operate('inputstream.adaptive'):
		addon.setSetting('useInputstream', 'false')
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listStartMag(url):
	debug_MS("(navigator.listStartMag) ------------------------------------------------ START = listStartMag -----------------------------------------------")
	FOUND, counter = (0 for _ in range(2))
	excludedIDD = ['f704b0ac-f94c-4808-9320-4d7a78772320', '2211e62b-acb1-49d2-a5f7-ec38511a61b8']
	# Fernsehfilme auf 1.Startseite(320) // Les téléfilms auf 2.Startseite(1b8)
	DATA = getUrl(url, AUTH=EMAC_token)
	debug_MS("++++++++++++++++++++++++")
	debug_MS("(navigator.listStartMag) XXXXX CONTENT : {} XXXXX".format(str(DATA)))
	debug_MS("++++++++++++++++++++++++")
	for each in DATA.get('zones', []):
		counter += 1
		if counter in [1, 2] and each.get('displayOptions', '') and each.get('displayOptions', {}).get('showZoneTitle', '') is False and each.get('displayOptions', {}).get('showItemTitle', '') is True:
			for video in each['data']: # Falls Videos in erster oder zweiter Rubrik = direkt anzeigen
				FOUND += 1
				LINKING(video, 'DATA_ONE', phrase, '(listStartpage=VIDEOS)')
		elif each.get('data', '') and len(each['data']) > 0:
			if (len(each.get('data')) == 1 and str(each['data'][0].get('programId')) in ['', 'None']) or \
				(str(each.get('id')) in excludedIDD): continue # 1. z.b. Newsletter // 2. excludedIDD 
			FOUND += 1
			LINKING(each, 'ZONE_ONE', 'HOME', '(listStartpage=FOLDER)')
	for magazine in DATA.get('data', []):
		FOUND += 1
		LINKING(magazine, 'DATA_ONE', 'MAGAZINE', '(listMagazines=FOLDER)')
	xbmcplugin.endOfDirectory(ADDON_HANDLE) 

def listThemes(url):
	debug_MS("(navigator.listThemes) ------------------------------------------------ START = listThemes -----------------------------------------------")
	DATA = getUrl(url, AUTH=EMAC_token)
	debug_MS("++++++++++++++++++++++++")
	debug_MS("(navigator.listThemes) XXXXX CONTENT : {} XXXXX".format(str(DATA)))
	debug_MS("++++++++++++++++++++++++")
	for theme in DATA['main']:
		CATY = str(theme['code'])
		title = cleaning(theme['label'])
		tagline = (cleaning(theme.get('description', '')) or "")
		debug_MS("(navigator.listThemes) ### NAME = {} || CATEGORY = {} ###".format(title, CATY))
		addDir(title, thepic+CATY+'.png', {'mode': 'listShowContent', 'url': API_URL+CATY.replace('ARS', 'ARTE_CONCERT')+'/', 'phrase': 'THEMECAT', 'name': title}, tagline)
	addDir(translation(30641) if COUNTRY == 'de' else translation(30642), thepic+'EMI.png', {'mode': 'listShowContent', 'url': API_URL+'EMI/', 'phrase': 'THEMECAT', 'name': 'Broadcasts'})
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listMusics(url):
	debug_MS("(navigator.listMusics) ------------------------------------------------ START = listMusics -----------------------------------------------")
	config = traversing.get_config()
	COMBI = []
	DATA = getUrl(url, AUTH=OPA_token)
	debug_MS("++++++++++++++++++++++++")
	debug_MS("(navigator.listMusics) XXXXX CONTENT : {} XXXXX".format(str(DATA)))
	debug_MS("++++++++++++++++++++++++")
	LG = True if COUNTRY == 'de' else False
	addDir(translation(30651) if LG else translation(30652), thepic+'XMU.png', {'mode': 'listShowContent', 'url': API_URL+'ARTE_CONCERT_MODERN/', 'phrase': 'MUSICCAT', 'name': 'CONCERT_MODERN'})
	addDir(translation(30653) if LG else translation(30654), thepic+'XCL.png', {'mode': 'listShowContent', 'url': API_URL+'ARTE_CONCERT_CLASSIC/', 'phrase': 'MUSICCAT', 'name': 'CONCERT_CLASSIC'})
	addDir(translation(30655) if LG else translation(30656), thepic+'AIO.png', {'mode': 'listShowContent', 'url': config['categories_one'].format(API_URL, 'ARS'), 'phrase': 'MUSICCAT', 'name': 'CONCERT_ALL'})
	for music in DATA['categories'][4].get('subcategories', []):
		CATY = str(music['code'])
		title = cleaning(music['label'])
		tagline = (cleaning(music.get('description', '')) or "")
		position = music['order']
		COMBI.append([position, title, CATY, tagline])
	for position, title, CATY, tagline in sorted(COMBI, key=lambda n: int(n[0]), reverse=False):
		debug_MS("(navigator.listMusics) ### POS = {} || NAME = {} || CATEGORY = {} ###".format(str(position), title, CATY))
		addDir(translation(30657).format(title), thepic+CATY+'.png', {'mode': 'listShowContent', 'url': config['categories_three'].format(API_URL, 'ARS', CATY), 'phrase': 'MUSICCAT', 'name': title}, tagline)
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listShowContent(url, PHRASE, NAME, PAGE):
	debug_MS("(navigator.listShowContent) ------------------------------------------------ START = listShowContent -----------------------------------------------")
	debug_MS("(navigator.listShowContent) ### URL : {} || PHRASE : {} || NAME : {} || PAGE : {} ###".format(url, PHRASE, NAME, str(PAGE)))
	# https://www.arte.tv/api/rproxy/emac/v3/de/web/data/MANUAL_TEASERS/?code=collections_SER&zone=07b776c7-8cc5-41e7-a16f-e4a5b51730cb&page=1&limit=6 || RUBRIK - kurz und witzig unter Serien
	# DURATION = https://www.arte.tv/api/rproxy/emac/v3/de/web/data/VIDEO_LISTING/?imageFormats=landscape&videoType=LONGER_DURATION&page=2&limit=20 || SEARCH = https://api-cdn.arte.tv/api/emac/v3/de/web/data/SEARCH_LISTING/?imageFormats=landscape&query=europe&page=2&limit=20
	# STANDARD =  https://api-cdn.arte.tv/api/emac/v3/de/web/data/VIDEO_LISTING/?imageFormats=landscape&videoType=MOST_VIEWED&page=1&limit=20
	FOUND, pos_1, pos_2 = (0 for _ in range(3))
	NPG = None
	excluded_DE = ['9f40ea44-6fef-428c-8d4c-19ef8516c865', '6acb1e4f-642c-46cf-9834-7265de658732', '8a4b86cd-2951-4244-9918-71bf54da50f4', '00744070-d5ce-4da1-807e-4d7df4732f33', \
		'50ece0c1-8dea-4d97-96ef-d58db33fcebb', 'f9a0c109-3c4d-412f-be76-3264b30dd844', '3c6c562c-3616-41e9-8aa8-0c9aae7b1186', '6f3697b2-7403-4da7-ad12-f223bb7f4d82']
	# Alle Kategorien in 1.Dokus(865)+2.Sendungen(732) // Musikkategorien in 3.ARTE_CONCERT_MODERN(0f4)+4.ARTE_CONCERT_CLASSIC(f33) //...
	# ...Frisch von der Bühne in 5.ARTE_CONCERT_MODERN(ebb)+6.ARTE_CONCERT_CLASSIC(844) // Das Wichtigste in Kürze unter 7.Aktuelles(186) // 8.DOKUS meistgesehen(d82)
	excluded_FR = ['572fccff-8b0d-40df-9c99-3daef82adc75', '47845061-9b41-4ca2-af15-0cde8e36858f', '20f50fc0-36f5-4925-ad5a-626b9c539dfa', '676f19e4-2811-4baa-b91c-db173b851318', \
		'c1ecdb74-c91c-475f-ab8c-a633f36d04a2', 'f883a63b-933f-45f0-888e-7f01decb1e2c', '489a55e7-bf4c-4720-b287-03555842c4f0', '110663a9-1f54-46cc-8021-eaba6e7aa13f']
	# Parcourir les catégories in 1.Dokus(c75)+2.Sendungen(58f) // Parcourir les genres in 3.ARTE_CONCERT_MODERN(dfa)+4.ARTE_CONCERT_CLASSIC(318) //...
	# ...Tout nouveau, tout beau in 5.ARTE_CONCERT_MODERN(4a2)+6.ARTE_CONCERT_CLASSIC(e2c) // actue en bref in 7.Aktuelles(4f0) // Les vidéos les plus vues in 8.DOKUS(13f)
	excludedIDD = excluded_DE+excluded_FR
	excludedCODE = ['collection_content', 'collection_upcoming', 'collection_article', 'collection_associated', 'collection_partner'] # Unwanted Collections
	url = '{0}&page={1}&limit={2}'.format(url.replace(' ', '%20').replace('-internal', '-cdn'), str(PAGE), str(LIMIT_NUMBER)) if int(PAGE) == 1 and not url.endswith('/') else url.replace('-internal', '-cdn')
	if int(PAGE) > 1 and not url.endswith('/') and 'limit=' in url:
		actual = re.compile(r'limit=([0-9]+)', re.S).findall(url)[0]
		url = re.sub(r'limit=[0-9]+', 'limit='+str(LIMIT_NUMBER), url) if int(actual) > int(LIMIT_NUMBER) else url
	DATA = getUrl(url, AUTH=EMAC_token)
	debug_MS("++++++++++++++++++++++++")
	debug_MS("(navigator.listShowContent) XXXXX CONTENT : {} XXXXX".format(str(DATA)))
	debug_MS("++++++++++++++++++++++++")
	CODENAMES = [cn for cn in DATA.get('zones', []) if cn.get('code', '') and str(cn['code'].get('name')).lower() in ['collection_videos', 'collection_subcollection'] and cn.get('data', '')]
	for each in DATA.get('zones', []):
		pos_1 += 1
		if pos_1 == 1 and each.get('displayOptions', '') and each.get('displayOptions', {}).get('showZoneTitle', '') is False and each.get('displayOptions', {}).get('showItemTitle', '') is True:
			for video_1 in each['data']: # Falls Videos in erster Rubrik = direkt anzeigen
				FOUND += 1
				LINKING(video_1, 'DATA_TWO', phrase, '(listShowContent=VIDEOS[1])')
		elif each.get('data', '') and len(each['data']) > 0:
			if (len(each['data']) == 1 and str(each['data'][0].get('programId')) in ['', 'None']) or \
				(str(each.get('id')) in excludedIDD) or \
				(each.get('code', '') and str(each['code'].get('name')).lower() in excludedCODE): continue # 1. z.b. Newsletter // 2. excludedIDD // 3. excludedCODE
			newPHR = DATA['page'] if DATA.get('page', '') in ['HOME', 'ACT', 'SCI', 'DEC', 'HIS', 'CIN', 'SER'] else phrase # WeitergabeCode für Meistgesehen und Letzte Chance
			FOUND += 1
			if len(each['data']) == 1 and str(each['data'][0].get('programId'))[:3] == 'RC-': # z.b. Happy Hour unter Alle Filme
				LINKING(each['data'][0], 'DATA_TWO', phrase, '(listShowContent=VIDEOS[2])')
			elif each.get('code', '') and str(each['code'].get('name')).lower() in ['collection_videos', 'collection_subcollection'] and len(CODENAMES) == 1:
				if str(each.get('nextPage'))[:4] == 'http':
					NPG = each['nextPage']
				for video_2 in each['data']: # Falls nur einmal *collection_videos* oder nur einmal *collection_subcollection* in Collectionen vorhanden = direkt anzeigen
					pos_2 += 1
					LINKING(video_2, 'DATA_TWO', phrase, '(listShowContent=VIDEOS[3])')
					if NPG and LIMIT_NUMBER == pos_2: break
			else:
				LINKING(each, 'ZONE_TWO', newPHR, '(listShowContent=FOLDER[2])')
	for movie in DATA.get('data', []):
		if 'category=' in url and 'LAST_CHANCE' in url and movie.get('availability', '') and movie.get('availability', {}).get('end', ''):
			LOCALstop = get_Local_DT(movie['availability']['end'][:19])
			if LOCALstop > (datetime.now() + timedelta(days=7)): break # Letzte Chance in Alle Filme/Alle Serien begrenzen auf max. 7 Tage
		FOUND += 1
		LINKING(movie, 'DATA_TWO', phrase, '(listShowContent=VARIABLE[1])')
	if FOUND == 0:
		message = translation(30526).format(NAME) if NAME != "" else translation(30525)
		return dialog.notification(translation(30524).format('Ergebnisse'), message, icon, 8000)
	# NEXTPAGE = https://api-cdn.arte.tv/api/emac/v3/de/web/data/COLLECTION_SUBCOLLECTION/?collectionId=RC-014035&subCollectionId=RC-015171&page=2&limit=20
	if (not ('category=' in url and 'LAST_CHANCE' in url) and DATA.get('data', []) and str(DATA.get('nextPage'))[:4] == 'http') or NPG is not None: # Keine nächste Seite für Letzte Chance in Alle Filme/Alle Serien
		newPAGE = NPG if NPG else DATA['nextPage']
		debug_MS("(navigator.listShowContent) This is NextPage : {}".format(newPAGE))
		debug_MS("(navigator.listShowContent) Now show NextPage ...")
		special_title = translation(30723) if COUNTRY == 'de' else translation(30724)
		addDir(special_title, artpic+'nextpage.png', {'mode': 'listShowContent', 'url': newPAGE, 'phrase': 'NEXTPAGE', 'name': NAME, 'page': int(PAGE)+1})
	xbmcplugin.endOfDirectory(ADDON_HANDLE) 

def listVideosDate(START, EXTRA):
	debug_MS("(navigator.listVideosDate) ------------------------------------------------ START = listVideosDate -----------------------------------------------")
	debug_MS("(navigator.listVideosDate) ### URL : {} || EXTRA : {} ###".format(START, EXTRA))
	config = traversing.get_config() # URL-Tag = https://api-cdn.arte.tv/api/emac/v3/de/web/pages/TV_GUIDE/?day=2021-12-08
	if EXTRA == 'DISPLAY':
		DATA = getUrl(START, AUTH=EMAC_token)
		for movie in DATA['zones'][-1]['data']:
			if 'FULL_VIDEO' in str(movie.get('stickers')) and str(movie.get('duration')) not in ['', 'None', '0']:
				LINKING(movie, 'DATA_TRE', 'VIDEODATE', '(listVideosDate)')
	else:
		i = -20
		while i <= 20:
			END = (datetime.now() - timedelta(days=i)).strftime('%Y{0}%m{0}%d'.format('-'))
			DATE = (datetime.now() - timedelta(days=i)).strftime('%w{0}%d{1}%m{1}'.format('~', '.'))
			DAY = [obj for obj in config['days'] if obj.get('route') == DATE.split('~')[0]]
			DD = DAY[0]['title_de'] if COUNTRY == 'de' else DAY[0]['title_fr']
			if i == 0: addDir("[I][COLOR lime]"+DATE.split('~')[1]+DD+"[/COLOR][/I]", icon, {'mode': 'listVideosDate', 'url': START+END, 'extras': 'DISPLAY'})
			else: addDir(DATE.split('~')[1]+DD, icon, {'mode': 'listVideosDate', 'url': START+END, 'extras': 'DISPLAY'})
			i += 1
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def listRunTime(url):
	debug_MS("(navigator.listRunTime) ------------------------------------------------ START = listRunTime -----------------------------------------------")
	config = traversing.get_config()
	for item in config['times']:
		title = item['title_de'] if COUNTRY == 'de' else item['title_fr']
		newURL = item.get('suffix').format(url)
		addDir(title, icon, {'mode': 'listShowContent', 'url': newURL, 'phrase': 'RUNTIME', 'name': title})
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def SearchARTE():
	debug_MS("(navigator.SearchARTE) ------------------------------------------------ START = SearchARTE -----------------------------------------------")
	config = traversing.get_config()
	keyword = None
	if xbmcvfs.exists(searchHackFile):
		with open(searchHackFile, 'r') as look:
			keyword = look.read()
	if xbmc.getInfoLabel('Container.FolderPath') == HOST_AND_PATH: # !!! this hack is necessary to prevent KODI from opening the input mask all the time !!!
		special_title = translation(30721) if COUNTRY == 'de' else translation(30722)
		keyword = dialog.input(heading=special_title, type=xbmcgui.INPUT_ALPHANUM, autoclose=10000)
		if keyword:
			keyword = quote(keyword)
			with open(searchHackFile, 'w') as record:
				record.write(keyword)
	if keyword: return listShowContent(config['search_query'].format(API_URL, keyword), 'SEARCHING', unquote(keyword), page)
	return None

def playVideo(url):
	debug_MS("(navigator.playVideo) ------------------------------------------------ START = playVideo -----------------------------------------------")
	""" 
	Übergabe des Abspiellinks von anderem Video-ADDON: plugin://plugin.video.tyl0re.arte/?mode=playVideo&url=048256-000-A oder: plugin://plugin.video.tyl0re.arte/?mode=playVideo&url=https://www.arte.tv/de/videos/048256-000-A/wir-waren-koenige/
	https://api.arte.tv/api/opa/v3/videoStreams?programId=104742-001-A&channel=DE&kind=SHOW&protocol=%24in:HTTPS,HLS&quality=%24in:EQ,HQ,MQ,SQ,XQ&profileAmm=%24in:AMM-PTWEB,AMM-PTHLS,AMM-OPERA,AMM-CONCERT-NEXT,AMM-Tvguide&limit=100
	DEUTSCH:::"DE" = Original deutsch | "OmU" = Original mit deutschen Untertiteln | "OV" = Stumm oder Originalversion
	FRANCE::: "VOF" = Original französisch | "VF" = französisch vertont | "VOSTF" = Stumm oder Original mit französischen Untertiteln
	"""
	config = traversing.get_config()
	MASTERS, MEDIAS, BestMASTERS, BestMEDIAS = ([] for _ in range(4))
	PRESENT_ONE, PRESENT_TWO, STREAM, QUALITY, FINAL_URL, TEST_URL = (False for _ in range(6))
	PLID = re.compile('/videos/([^/]+?)/', re.S).findall(url)[0] if url[:4] == 'http' else url
	debug_MS("(navigator.playVideo[1]) ### Original-URL : {} || PLID : {} ###".format(str(url), str(PLID)))
	QUALITIES = [2160, 1080, 720, 406, 360, 216]
	SHORTCUTS = ['DE', 'OmU', 'OV', 'VO'] if COUNTRY == 'de' else ['VOF', 'VF', 'VOSTF', 'VO']
	try:
		DATA_ONE = getUrl(config['streaming_various'].format(str(PLID), COUNTRY.upper()), AUTH=OPA_token) # Für diverse - Streams
		if len(DATA_ONE['videoStreams']) >= 1:
			PRESENT_ONE = True
	except: pass
	if PRESENT_ONE:
		for each in DATA_ONE.get('videoStreams', []):
			quality, version = (0 for _ in range(2))
			quality  = each.get('height') if isinstance(each.get('height'), int) else 0
			media   = (each.get('mediaType', '') or "")
			mime    = (each.get('mimeType', '') or "")
			stream  = (each.get('url', '') or "")
			version = each.get('audioSlot') if isinstance(each.get('audioSlot'), int) else 0
			name    = (each.get('audioLabel', '') or "")
			lang      = (each.get('audioShortLabel', '') or "")
			if version == 1 and media and media.lower() == 'hls' and '.m3u8' in stream and int(quality) > 408:
				MASTERS.append({'url': stream, 'quality': quality, 'mimeType': mime, 'name': name, 'language': lang})
			if version == 1 and media and media.lower() == 'mp4' and 'mp4' in stream and int(quality) > 358:
				MEDIAS.append({'url': stream, 'quality': quality, 'mimeType': mime, 'name': name, 'language': lang})
	if not MASTERS:
		try:
			DATA_TWO = getUrl(config['streaming_hls'].format(COUNTRY, str(PLID))) # Für HLS- und m3u8- Streams // z.Zt. ohne Token 09.05.2022
			if len(DATA_TWO['data']['attributes']['streams']) >= 1:
				PRESENT_TWO = True
		except: pass
		if PRESENT_TWO:
			for elem in DATA_TWO['data']['attributes']['streams']:
				quality, version = (0 for _ in range(2))
				stream    = (elem.get('url') or "")
				if elem.get('versions', ''):
					name   = (elem.get('versions', {})[0].get('label', '') or "")
					lang     = (elem.get('versions', {})[0].get('shortLabel', '') or "")
				if elem.get('mainQuality', ''):
					quality = (elem.get('mainQuality', {}).get('label', '') or "")
					quality = quality.replace('p', '') if not isinstance(quality, int) else 0
				mime       = 'application/vnd.apple.mpegurl'
				version    = (elem.get('slot', 0) or 0)
				if version == 1 and '.m3u8' in stream and int(quality) > 404:
					MASTERS.append({'url': stream, 'quality': quality, 'mimeType': mime, 'name': name, 'language': lang})
	if MASTERS:
		debug_MS("(navigator.playVideo[2]) ORIGINAL_M3U8 ##### unsorted_LIST : {} ###".format(str(MASTERS)))
		order_dict = {qual: index for index, qual in enumerate(QUALITIES)}
		BestMASTERS = sorted(MASTERS, key=lambda m: order_dict.get(m['quality'], float('inf')))
		debug_MS("(navigator.playVideo[2]) SORTED_LIST | M3U8 ### sorted_LIST : {} ###".format(str(BestMASTERS)))
	if MEDIAS:
		debug_MS("(navigator.playVideo[2]) ORIGINAL_MP4 ##### unsorted_LIST : {} ###".format(str(MEDIAS)))
		order_dict = {qual: index for index, qual in enumerate(QUALITIES)}
		BestMEDIAS = sorted(MEDIAS, key=lambda x: order_dict.get(x['quality'], float('inf')))
		debug_MS("(navigator.playVideo[2]) SORTED_LIST | MP4 ### sorted_LIST : {} ###".format(str(BestMEDIAS)))
	if prefSTREAM == '1' and not enableINPUTSTREAM and BestMEDIAS:
		debug_MS("(navigator.playVideo[3]) ~~~~~ TRY NUMBER ONE TO GET THE FINALURL (mp4) ~~~~~")
		STREAM, MIME, QUALITY, FINAL_URL = 'MP4', 'video/mp4', BestMEDIAS[0]['quality'], BestMEDIAS[0]['url']
	if not FINAL_URL and BestMASTERS:
		debug_MS("(navigator.playVideo[4]) ~~~~~ TRY NUMBER TWO TO GET THE FINALURL (m3u8) ~~~~~")
		STREAM = 'HLS' if enableINPUTSTREAM else 'M3U8'
		MIME, QUALITY, FINAL_URL = 'application/vnd.apple.mpegurl', BestMASTERS[0]['quality'], BestMASTERS[0]['url']
	try: # Test ob das Video abspielbar ist !!!
		code = urlopen(FINAL_URL, timeout=6).getcode()
		if code in [200, 201, 202]: TEST_URL = True
	except: pass
	if FINAL_URL and TEST_URL:
		LSM = xbmcgui.ListItem(path=FINAL_URL)
		LSM.setMimeType(MIME)
		if ADDON_operate('inputstream.adaptive') and STREAM in ['HLS', 'MPD']:
			LSM.setProperty('inputstream', 'inputstream.adaptive')
			LSM.setProperty('inputstream.adaptive.manifest_type', STREAM.lower())
		xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, LSM)
		log("(navigator.playVideo) [{}p] {}_stream : {} ".format(str(QUALITY), STREAM, FINAL_URL))
		debug_MS("(navigator.playVideo[5]) ++++++++++++++++++++")
	elif FINAL_URL and not TEST_URL:
		failing("(navigator.playVideo) ##### Abspielen des Streams NICHT möglich #####\n ##### IDD : {} || FINAL_URL : {} #####\n ########## Der generierte Stream von *arte.tv* ist DEFEKT !!! ##########".format(PLID, str(FINAL_URL)))
		return dialog.notification(translation(30521).format('VIDEO'), translation(30527), icon, 10000)
	else:
		failing("(navigator.playVideo) ##### Abspielen des Streams NICHT möglich ##### IDD : {} #####\n ########## KEINEN Stream-Eintrag auf *arte.tv* gefunden !!! ##########".format(PLID))
		return dialog.notification(translation(30521).format('VIDEO'), translation(30528), icon, 8000)

def playLive(url, name):
	LTM = xbmcgui.ListItem(path=url, label=name)
	LTM.setMimeType('application/vnd.apple.mpegurl')
	if ADDON_operate('inputstream.adaptive'):
		LTM.setProperty('inputstream', 'inputstream.adaptive')
		LTM.setProperty('inputstream.adaptive.manifest_type', 'hls')
		LTM.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')
	xbmc.Player().play(item=url, listitem=LTM)

def liveTV():
	debug_MS("(navigator.liveTV) ------------------------------------------------ START = liveTV -----------------------------------------------")
	config = traversing.get_config()
	for item in config['transmission']:
		if COUNTRY == 'de' and not 'Event' in item.get('description') and not 'Germany' in item.get('description'): continue
		elif COUNTRY == 'fr' and not 'Event' in item.get('description') and not 'France' in item.get('description'): continue
		img = item.get('img').format(evepic) if item.get('img') is not None else icon
		listitem = xbmcgui.ListItem(path=item['url'], label=item['title'])
		listitem.setArt({'icon': icon, 'thumb': img, 'poster': img, 'fanart': defaultFanart})
		xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url='{0}?{1}'.format(HOST_AND_PATH, urlencode({'mode': 'playLive', 'url': item['url'], 'name': item['title']})), listitem=listitem)
	xbmcplugin.endOfDirectory(ADDON_HANDLE)

def LINKING(info, category=None, phrase=None, extras=None):
	uvz, LEM, folder = get_ListItem(info, category, phrase, extras)
	if uvz is None: return
	return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=uvz, listitem=LEM, isFolder=folder)

def addDir(name, image, params={}, tagline=None, plot='...', folder=True):
	u = '{0}?{1}'.format(HOST_AND_PATH, urlencode(params))
	liz = xbmcgui.ListItem(name)
	if KODI_ov20:
		videoInfoTag = liz.getVideoInfoTag()
		videoInfoTag.setTitle(name), videoInfoTag.setPlot(plot), videoInfoTag.setTagLine(tagline), videoInfoTag.setStudios(['ARTE'])
	else:
		liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': plot, 'Tagline': tagline, 'Studio': 'ARTE'})
	liz.setArt({'icon': icon, 'thumb': image, 'poster': image, 'fanart': defaultFanart})
	if image and useThumbAsFanart and image != icon and not artpic in image:
		liz.setArt({'fanart': image})
	return xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=u, listitem=liz, isFolder=folder)
