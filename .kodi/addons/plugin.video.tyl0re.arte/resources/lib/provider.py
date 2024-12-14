# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcaddon

def translation(id):
	return xbmcaddon.Addon().getLocalizedString(id)


class Client(object):
	CONFIG_ARTE = {
		'categories_one': '{}data/VIDEO_LISTING/?category={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=MOST_RECENT',
		'categories_two': '{}data/VIDEO_LISTING/?{}imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType={}',
		'categories_three': '{}data/VIDEO_LISTING/?category={}&subcategories={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=MOST_RECENT',
		'collections_one': '{}data/{}/?collectionId={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true',
		'collections_two': '{}data/{}/?collectionId={}&subCollectionId={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true',
		'codes_one': '{}data/MOST_RECENT_SUBCATEGORY/?subCategoryCode={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true',
		'codes_two': '{}data/MANUAL_TEASERS/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&code={}&zone={}',
		'search_query': '{}data/SEARCH_LISTING/?query={}&imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true',
		'streaming_hls': 'https://api.arte.tv/api/player/v2/config/{}/{}',
		'streaming_various': 'https://api.arte.tv/api/opa/v3/videoStreams?programId={}&channel={}&kind=SHOW&protocol=%24in:HTTPS,HLS&quality=%24in:EQ,HQ,MQ,SQ,XQ&profileAmm=%24in:AMM-PTWEB,AMM-PTHLS,AMM-OPERA,AMM-CONCERT-NEXT,AMM-Tvguide&limit=100',
		'picks': [
		{
			'title_de': translation(30601),
			'title_fr': translation(30602),
			'action': 'listStartMag',
			'url': '{}pages/HOME/',
			'description': 'Startpage'
		},
		{
			'title_de': translation(30603),
			'title_fr': translation(30604),
			'action': 'listThemes',
			'url': '{}MENU/',
			'description': 'Theme-Categories'
		},
		{
			'title_de': translation(30605),
			'title_fr': translation(30606),
			'action': 'listMusics',
			'url': 'https://api.arte.tv/api/opa/v3/categories?language={}&limit=50',
			'description': 'Music-Categories'
		},
		{
			'title_de': translation(30607),
			'title_fr': translation(30608),
			'action': 'listStartMag',
			'url': '{}data/VIDEO_LISTING/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=MAGAZINES&limit=50',
			'description': 'Broadcast A-Z'
		},
		{
			'title_de': translation(30609),
			'title_fr': translation(30610),
			'action': 'listVideosDate',
			'url': '{}pages/TV_GUIDE/?day=',
			'description': 'Program sorted by date'
		},
		{
			'title_de': translation(30611),
			'title_fr': translation(30612),
			'action': 'listRunTime',
			'url': '{}data/VIDEO_LISTING/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=',
			'description': 'Videos sorted by runtime'
		},
		{
			'title_de': translation(30613),
			'title_fr': translation(30614),
			'action': 'listShowContent',
			'url': '{}data/VIDEO_LISTING/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=MOST_VIEWED',
			'description': 'Most viewed'
		},
		{
			'title_de': translation(30615),
			'title_fr': translation(30616),
			'action': 'listShowContent',
			'url': '{}data/VIDEO_LISTING/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=MOST_RECENT',
			'description': 'New Videos'
		},
		{
			'title_de': translation(30617),
			'title_fr': translation(30618),
			'action': 'listShowContent',
			'url': '{}data/VIDEO_LISTING/?imageFormats=landscape%2Cbanner%2Csquare%2Cportrait&imageWithText=true&videoType=LAST_CHANCE',
			'description': 'Last Chance'
		},
		{
			'title_de': translation(30619),
			'title_fr': translation(30620),
			'action': 'SearchARTE',
			'img': '{}basesearch.png',
			'description': 'Search ...'
		},
		{
			'title_de': translation(30621),
			'title_fr': translation(30622),
			'action': 'liveTV',
			'img': '{}livestream.png',
			'description': 'Live & Event TV'
		},
		{
			'title_de': translation(30623),
			'title_fr': translation(30624),
			'action': 'aConfigs',
			'img': '{}settings.png',
			'description': 'ARTE Settings'
		},
		{
			'title_de': translation(30625),
			'title_fr': translation(30626),
			'action': 'iConfigs',
			'img': '{}settings.png',
			'description': 'Inputstream Settings'
		}],
		'days': [
		{
			'title_de': translation(30671),
			'title_fr': translation(30672),
			'route': '1',
			'description': 'Monday'
		},
		{
			'title_de': translation(30673),
			'title_fr': translation(30674),
			'route': '2',
			'description': 'Tuesday'
		},
		{
			'title_de': translation(30675),
			'title_fr': translation(30676),
			'route': '3',
			'description': 'Wednesday'
		},
		{
			'title_de': translation(30677),
			'title_fr': translation(30678),
			'route': '4',
			'description': 'Thursday'
		},
		{
			'title_de': translation(30679),
			'title_fr': translation(30680),
			'route': '5',
			'description': 'Friday'
		},
		{
			'title_de': translation(30681),
			'title_fr': translation(30682),
			'route': '6',
			'description': 'Saturday'
		},
		{
			'title_de': translation(30683),
			'title_fr': translation(30684),
			'route': '0',
			'description': 'Sunday'
		}],
		'times': [
		{
			'title_de': translation(30701),
			'title_fr': translation(30702),
			'suffix': '{}SHORT_DURATION',
			'description': 'Short Duration'
		},
		{
			'title_de': translation(30703),
			'title_fr': translation(30704),
			'suffix': '{}MEDIUM_DURATION',
			'description': 'Medium Duration'
		},
		{
			'title_de': translation(30705),
			'title_fr': translation(30706),
			'suffix': '{}LONG_DURATION',
			'description': 'Long Duration'
		},
		{
			'title_de': translation(30707),
			'title_fr': translation(30708),
			'suffix': '{}LONGER_DURATION',
			'description': 'Duration without Limitation'
		}],
		'transmission': [
		{
			'title': translation(32101),
			'url': 'https://artesimulcast.akamaized.net/hls/live/2030993/artelive_de/master.m3u8',
			'img': '{}ARTE_LIVE.png',
			'description': 'ARTE ~ Germany live'
		},
		{
			'title': translation(32102),
			'url': 'https://artesimulcast.akamaized.net/hls/live/2031003/artelive_fr/master.m3u8',
			'img': '{}ARTE_LIVE.png',
			'description': 'ARTE ~ France live'
		},
		{
			'title': translation(32103),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025494/channel01/master.m3u8',
			'img': '{}ONE.png',
			'description': 'ARTE Event 1'
		},
		{
			'title': translation(32104),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025495/channel02/master.m3u8',
			'img': '{}TWO.png',
			'description': 'ARTE Event 2'
		},
		{
			'title': translation(32105),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025496/channel03/master.m3u8',
			'img': '{}THREE.png',
			'description': 'ARTE Event 3'
		},
		{
			'title': translation(32106),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025497/channel04/master.m3u8',
			'img': '{}FOUR.png',
			'description': 'ARTE Event 4'
		},
		{
			'title': translation(32107),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025498/channel05/master.m3u8',
			'img': '{}FIVE.png',
			'description': 'ARTE Event 5'
		},
		{
			'title': translation(32108),
			'url': 'https://arteconcerthls.akamaized.net/hls/live/2025499/channel06/master.m3u8',
			'img': '{}SIX.png',
			'description': 'ARTE Event 6'
		}],
	}

	def __init__(self, config):
		self._config = config

	def get_config(self):
		return self._config
