import spotify_api as sp
import time
# print(sp.getCurrentTrack())

track_info = {
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

print(f"track info = {track_info}")
while True:
    token = sp.getToken()
    updateTrackInfo(token)
    print(f"updated track info = {track_info}")
    time.sleep(0.33)