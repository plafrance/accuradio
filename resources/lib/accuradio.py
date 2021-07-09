import json
import requests
import sys
import xbmc
import xbmcgui
import resources.lib.settings as settings
import resources.lib.kodiutils as utils

__addonid__ = 'plugin.audio.accuradio'
__settings__ = settings.Settings(__addonid__, sys.argv)

def isConnected():
    return False

def get_home_page_items():
    return [
        {
            "name": __settings__.get_string(STR_GENRE),
            "url" : ""
        },
        {
            "name": __settings__.get_string(STR_SEARCH),
            "url" : ""
        }
    ]

def get_genre_items():
    url = "https://accuradio.com/c/m/json/brands/"

    content = fetch_url(url)

    genres = [
        {
            "name": genre["name"],
            "url": "https://accuradio.com/c/m/json/genre/?param=" + (genre["canonical_url"] if genre["canonical_url"]!="" else genre["name"].lower())
        }
        for genre in content["brands"] ]

    return genres

def get_channel_items(url):
    content = fetch_url(url)

    channels = [
        {
            "name": channel["name"],
            "url": "https://accuradio.com/playlist/json/" + channel["_id"]["$oid"],
            "thumbnail": "https://c2.accu.fm/tiles/default/" + str(channel["oldid"]) + ".jpg"
        }
        for channel in content["channels"] ]
                       
    return channels
                    
def get_track_items(url):
    content = fetch_url(url + "/?ando=3503&intro=true&spotschedule=594ac69eab53e37d52ff0c34&fa=null&rand=0.5835843411109176&ab=1")
    
    tracks = [
        {
            "name": track["title"],
            "url": track["primary"] + track["fn"] + ".m4a",
            "duration": int(track["duration"]) if "duration" in track else None,
            "artist_name": track["artist"]["artistdisplay"] if "artist" in track else "Anonymous"
        } | {
            "album_name": track["album"]["title"],
            "year": track["album"]["year"],
            "thumbnail": "https://www.accuradio.com/static/images/covers300" + track["album"]["cdcover"],
        } if "album" in track else {}
        for track in content
        if "ad_type" not in track
    ]
            
    return tracks

def fetch_url(url):
    hdr = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}
    req = requests.get( url, headers=hdr )
    return req.json()
    

def get_listitem_genre():    
    item = xbmcgui.ListItem(
        __settings__.get_string(STR_GENRE),
        __settings__.get_string(STR_GENRE))
    url = utils.add_params(
        root=__settings__.get_argv(0), params={'path': 'browse_genres'})
    return (item, url)

def get_listitem_search(): 
    item = xbmcgui.ListItem(
        __settings__.get_string(STR_SEARCH),
        __settings__.get_string(STR_SEARCH))        
    url = utils.add_params(
        root=__settings__.get_argv(0), params={'path': 'search'})
    
    return (item, url)

