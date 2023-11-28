import spotifykeys
import requests, webbrowser, json,time
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

scope = 'user-read-currently-playing'
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
client_id = spotifykeys.client_id
client_secret = spotifykeys.client_secret
redirect_uri = spotifykeys.redirect_uri

spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

def readToken():
    f = open("test.cache", "r")
    token_content = f.read()
    if len(token_content) != 0:
        token = json.loads(token_content)
        return token['access_token']
    else:
        raise FileNotFoundError

def writeToken(token):
    f = open("test.cache", "w")
    f.write(str(token).replace("'", '"'))
    f.close()

def getNewToken():
    authorization_url, state = spotify.authorization_url(auth_url)
    print('Please go here and authorize: ', authorization_url)
    webbrowser.open(authorization_url)
    redirect_response = input('\n\nPaste the full redirect URL here: ')

    auth = HTTPBasicAuth(client_id, client_secret)
    token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
    writeToken(token)
    token = token['access_token']
    return token

# gets token locally or new one online
def getToken(new=None):
    token = None
    if not new:
        try:
            token = readToken()
        except:
            token = getNewToken()
        finally:
            return token
    else:
        return getNewToken()
        
# returns json of api response
def getCurrentTrack(token):
    out = None
    url = 'https://api.spotify.com/v1/me/player/currently-playing/'
    headers = {
        'Authorization':f'Bearer {token}'
    }
    response = requests.get(url,headers=headers, stream=True)
    try:
        out = json.loads(response.content)
        return out
    except Exception as e:
        print("Not playing anything")
    finally:
        return out

    

# track_info = {
#     "is_playing": False,
#     "track_name": '',
#     "artist_name": '',
#     "image_url": ''
# }

# def updateTrackInfo(token):
#     current_track_info = getCurrentTrack(token)
#     if (current_track_info != None):
#         track_info["is_playing"] = current_track_info["is_playing"]
#         track_info["track_name"] = current_track_info["item"]["name"]
#         track_info["artist_name"] = current_track_info["item"]["artists"][0]["name"]
#         track_info["image_url"] = current_track_info["item"]["album"]["images"][2]["url"]
#     else:
#         track_info["is_playing"] = False
#         track_info["track_name"] = ""
#         track_info["artist_name"] = ""
#         track_info["image_url"] = ""

# token = getToken()
# print(f"track info = {track_info}")
# while True:
#     updateTrackInfo(token)
#     print(f"updated track info = {track_info}")
#     time.sleep(0.33)