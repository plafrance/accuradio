from xbmcswift2 import Plugin, xbmc, ListItem

import xbmcgui
import xbmcplugin

import resources.lib.settings as settings
import resources.lib.kodiutils as utils
import resources.lib.accuradio as accuradio

from resources.lib.constants import *

__addonid__ = 'plugin.audio.accuradio'
__partnerid__ = '1234'
__author__ = 'Patrick Lafrance'

# Initialise settings.
__settings__ = settings.Settings(__addonid__, sys.argv)

# Get addon information.
__addonname__ = __settings__.get_name()
__version__ = __settings__.get_version()

# Get addon settings values.
#__username__ = __settings__.get('username')
#__password__ = __settings__.get('password')
__debuglevel__ = 3 #__settings__.get('debuglevel')

__params__ = utils.get_params(__settings__.get_argv(2))
__path__ = utils.get_value(__params__, 'path')
__id__ = utils.get_value(__params__, 'id')

plugin = Plugin()

def make_playlist_items( items ):
    listitems = []
    for count,item in enumerate(items):
        listitem = ListItem(
            label = item["name"],
            label2 = item["name"],
            icon = item["thumbnail"] if "thumbnail" in item else None,
            thumbnail = item["thumbnail"] if "thumbnail" in item else None,
            path = item["url"] )

        listitem.as_xbmc_listitem().setInfo('music',
                                            {'tracknumber': count+1,
                                             'title': item["name"],
                                             'duration': item["duration"],
                                             'year': item['year'],
                                             'album': item['album_name'],
                                             'artist': item['artist_name'],
                                             })

        listitems+=[listitem]

    return listitems

def make_directory_items( items, path ):
    return [ { 'label': item["name"], 'path': plugin.url_for( path, url=item['url'] ), 'thumbnail': item["thumbnail"] if "thumbnail" in item else None } for item in items ]

@plugin.route('/genres')
def get_genres():
    return make_directory_items( accuradio.get_genre_items(), "get_channels" )

@plugin.route('/channels/<url>')
def get_channels( url ):
    return make_directory_items( accuradio.get_channel_items( url) , "get_playlist" )

@plugin.route('/playlist/<url>')
def get_playlist( url ):
    tracks = accuradio.get_track_items(url)

    playlist = make_playlist_items( tracks )
    
    xbmc.PlayList(xbmc.PLAYLIST_MUSIC).clear()
    plugin.add_to_playlist( playlist, playlist='music' )
    xbmc.Player().play()

@plugin.route('/history')
def get_history():
    pass
    
@plugin.route('/features')
def get_features():
    pass
    
@plugin.route('/favorites')
def get_favorites():
    return make_directory_items( accuradio.get_favorites() , "get_playlist" )
    
@plugin.route('/search')
def search():
    pass


@plugin.route('/')
def get_home_page( ):
    return [
        { 'label' : __settings__.get_string(STR_GENRE), 'path': plugin.url_for('get_genres') },
        { 'label' : __settings__.get_string(STR_SEARCH), 'path': plugin.url_for('search') },
        { 'label' : __settings__.get_string(STR_FEATURES), 'path': plugin.url_for('get_features') },
        ] + ([
            { 'label' : __settings__.get_string(STR_FAVORITES), 'path': plugin.url_for('get_favorites') },
            { 'label' : __settings__.get_string(STR_HISTORY), 'path': plugin.url_for('get_history') },
        ] if accuradio.isConnected() else [])
plugin.run()

