import time
import spotifykeys
import spotipy
###################################### 
# spotify setup
SPOTIPY_REDIRECT_URI='https://github.com/rakib-shahid/rs4x4'

auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=spotifykeys.client_id, client_secret=spotifykeys.client_secret, redirect_uri= SPOTIPY_REDIRECT_URI,scope='user-read-currently-playing', show_dialog=True,cache_handler=None)
spotify = spotipy.Spotify(auth_manager=auth_manager)

track_info = {
    "is_playing": False,
    "track_name": '',
    "artist_name": ''
}
# spotify function
def get_current_track_info():
    try:
        response = spotify.current_user_playing_track()

        track_info["is_playing"] = response["is_playing"]
        track_info["track_name"] = response["item"]["name"]
        track_info["artist_name"] = response["item"]["artists"][0]["name"]
    except TypeError:
        track_info["is_playing"] = False
        track_info["track_name"] = ""
        track_info["artist_name"] = ""
#####################################################

print(spotify.current_user_recently_played())
print("bub")
print(spotify.current_user_playing_track())
def cycleString(input_string, i):
    if len(input_string) > 26:
        start_index = i % len(input_string)
        substring = input_string[start_index:] + input_string[:start_index]
        result = substring[:26]
    else:
        result = input_string
    return result

outString = "♪ KEY - ONE OF THOSE NIGHTS       " 
test = "♪ OH MY GIRL - DUN DUN DANCE"
for i in range(1,10):
    test = cycleString(outString,i)
    print(test)