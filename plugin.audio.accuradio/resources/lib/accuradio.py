import json
import requests
import sys
import xbmc
import xbmcgui
import resources.lib.kodiutils as utils
from xbmcswift2 import Plugin

from resources.lib.constants import *

plugin = Plugin()

__addonid__ = 'plugin.audio.accuradio'

def isConnected():
    return False

def get_home_page_items():
    return [
        {
            "name": plugin.get_string(STR_GENRE),
            "url" : ""
        },
        {
            "name": plugin.get_string(STR_SEARCH),
            "url" : ""
        }
    ]

def get_genre_items():
    url = "https://accuradio.com/c/m/json/brands/"

    content = fetch_url(url)

    genres = [
        {
            "name": genre["name"],
            "url": f"https://accuradio.com/c/m/json/genre/?param={get_genre_canonical_url( genre )}",
            "description": f"{genre['channels']} {plugin.get_string(STR_CHANNELS)}",
        }
        for genre in content["brands"] ]

    return genres

def get_genre_canonical_url( genre ):
    return genre["param"] if genre["param"]!="" else genre["name"].lower()

def get_channel_items(url):
    content = fetch_url(url)

    if "channels" not in content: return []
    
    channels = [
        {
            "name": channel["name"],
            "url": f"https://accuradio.com/playlist/json/{channel['_id']['$oid']}",
            "thumbnail": f"https://c2.accu.fm/tiles/default/{channel['oldid']}.jpg",
            "description": f"{channel['description']}\n{channel['track_count'] if 'track_count' in channel else 0} {plugin.get_string(STR_TRACKS)}"
        }
        for channel in content["channels"] ]
                       
    return channels
                    
def get_track_items(url):
    content = fetch_url(url)
    
    tracks = []
    
    for track in content:
        if "ad_type" not in track:
            new_track = {
                "name": track["title"],
                "url": track["primary"] + track["fn"] + ".m4a",
                "duration": int(track["duration"]) if "duration" in track else None,
                "artist_name": track["track_artist"] if "track_artist" in track else "Anonymous",
            }
           
            if "album" in track:
                new_track.update(
                    {
                        "album_name": track["album"]["title"],
                        "year": track["album"]["year"],
                        "thumbnail": f"https://www.accuradio.com/static/images/covers300{track['album']['cdcover']}",
                    })
            else:
                new_track.update(
                    {
                        "album_name": "",
                        "year": "",
                        "thumbnail": "https://static.accuradio.com/static/images/2014/defaultTile.jpg"
                    }
                )
                
            tracks+= [new_track]
            

    return tracks

def fetch_url(url):
    hdr = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}
    req = requests.get( url, headers=hdr )
    return req.json()
    

def get_listitem_genre():    
    item = xbmcgui.ListItem(
        plugin.get_string(STR_GENRE),
        plugin.get_string(STR_GENRE))
    url = utils.add_params(
        root=sys.argv[0], params={'path': 'browse_genres'})
    return (item, url)

def get_listitem_search(): 
    item = xbmcgui.ListItem(
        plugin.get_string(STR_SEARCH),
        plugin.get_string(STR_SEARCH))        
    url = utils.add_params(
        root=sys.argv[0], params={'path': 'search'})
    
    return (item, url)

