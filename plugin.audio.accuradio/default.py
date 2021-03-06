from xbmcswift2 import Plugin, xbmc, ListItem

import sys
import xbmcaddon
import xbmcgui
import xbmcplugin

import resources.lib.kodiutils as utils
import resources.lib.accuradio as accuradio

from resources.lib.constants import *

__addonid__ = 'plugin.audio.accuradio'
__partnerid__ = '1234'
__author__ = 'Patrick Lafrance'

# Get addon information.
__addonname__ = xbmcaddon.Addon(id=__addonid__).getAddonInfo('name')
__version__ = xbmcaddon.Addon(id=__addonid__).getAddonInfo('version')

__params__ = sys.argv[2]
__path__ = utils.get_value(__params__, 'path')
__id__ = utils.get_value(__params__, 'id')

plugin = Plugin()

def make_playlist_items( items ):
    listitems = []

    for count,item in enumerate(items):
        listitem = ListItem(
            label = item["name"],
            icon = item["thumbnail"],
            thumbnail = item["thumbnail"],
            path = item["url"])
        listitem.set_info(
            'music',
            {'tracknumber': count+1,
             'duration': item["duration"],
             'year': item['year'],
             'album': item['album_name'],
             'artist': item['artist_name'],
             })

        listitems+=[listitem]

    return listitems

def make_directory_items( items, path ):
    return [
        {
            'label': item["name"],
            'path': plugin.url_for( path, url=item['url'] ),
            'thumbnail': item["thumbnail"] if "thumbnail" in item else None,
            'info_type': 'Video', # allows for a description, while the Music type doesn't
            'info': {
                'plot': item["description"] if "description" in item else None},
        }
        for item in items ]

@plugin.route('/genres')
def get_genres():
    return make_directory_items( accuradio.get_genre_items(), "get_channels" )

@plugin.route('/channels/<url>')
def get_channels( url ):
    return make_directory_items( accuradio.get_channel_items( url ) , "get_playlist" )

@plugin.route('/playlist/<url>')
def get_playlist( url ):
    tracks = accuradio.get_track_items(url + "/")

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
        { 'label' : plugin.get_string(STR_GENRE), 'path': plugin.url_for('get_genres') }
        ]
plugin.run()

