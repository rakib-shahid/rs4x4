import spotify_api as sp
import time
import funchid as fh
import threading
# print(sp.getCurrentTrack())

track_info = {
    "is_playing": False,
    "track_name": '',
    "artist_name": '',
    "image_url": ''
}

old_track_info = {
    "is_playing": False,
    "track_name": '',
    "artist_name": '',
    "image_url": ''
}

def updateTrackInfo(token):
    current_track_info = sp.getCurrentTrack(token)
    # print(f"current_track_info = {current_track_info}")
    try:
        track_info["is_playing"] = current_track_info["is_playing"]
        track_info["track_name"] = current_track_info["item"]["name"]
        track_info["artist_name"] = current_track_info["item"]["artists"][0]["name"]
        track_info["image_url"] = current_track_info["item"]["album"]["images"][2]["url"]
    except KeyError as e:
        return sp.getNewToken()
    except:
        track_info["is_playing"] = False
        track_info["track_name"] = ""
        track_info["artist_name"] = ""
        track_info["image_url"] = ""

outString = ''
lastString = ''
cycled = ''
threads = []
i = 1
print(f"track info = {track_info}")
while True:
    token = sp.getToken()
    updateTrackInfo(token)
    if (old_track_info != track_info):
        outString = f'♫ {(track_info["artist_name"])} - {(track_info["track_name"])} '
    # print(fh.clean_song_string(outString[:18]))
    # print(f"updated track info = {track_info}")
    outString = fh.cycleString(outString,i)
    new_track = (old_track_info["track_name"] != '')
    print(fh.cycleString(fh.clean_song_string(outString[:18]),i))
    if (track_info['is_playing']) & new_track:
        fh.send_raw_report(track_info,0xFF, bytes(fh.cycleString(fh.clean_song_string(outString),i),'utf-8'))
    else:
        fh.send_raw_report(track_info, 0xFF, bytes("",'utf-8'))
        i = 0
    time.sleep(0.33)
    i+=1
    old_track_info = track_info