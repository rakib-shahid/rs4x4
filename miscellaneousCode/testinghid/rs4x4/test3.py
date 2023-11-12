from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import spotifykeys
import requests
import json
import time


###################################### 
# spotify setup
redirect_uri='https://localhost:8888/callback'
client_id=spotifykeys.client_id
client_secret=spotifykeys.client_secret
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
token_valid = True
scope = ['user-read-currently-playing']



track_info = {
    "is_playing": False,
    "track_name": '',
    "artist_name": ''
}

spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

def readToken():
    f = open(".cache", "r")
    token_content = f.read()
    if len(token_content) != 0:
        token = json.loads(token_content)
        return token
    else:
        raise IndexError

def getNewToken():
    authorization_url, state = spotify.authorization_url(auth_url)
    print('Please go here and authorize: ', authorization_url)
    redirect_response = input('\n\nPaste the full redirect URL here: ')

    auth = HTTPBasicAuth(client_id, client_secret)
    token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

    f = open(".cache", "w")
    print(token)
    f.write(str(token).replace("'", '"'))
    f.close()


# test = "{'access_token': 'BQCJrVy-X9yX0HERr0Y8gsoEYEksJbAA7YYtjOcHme7gKX8P3-kaHTbb-3S-QAbvt41LFcxd77S1hJBgkzONeaSSNS_VzvQ4upT102e1Gn1PUak6rGRsTSoa7ED-0a8k6Rtahxqg6R7EqBfd8pVHvsiTckwRQaiKbrJHfNA-R8cTjRb4sCI', 'token_type': 'Bearer', 'expires_in': 3600, 'refresh_token': 'AQChHbmRSA-U_Uj-q5eeEsLjuyYGdGcYbJXC9pYYuIC5PFjWopU0hnnvELZAEu3RYesNrxbbwxI6jJCEGBbv7EU8S9UwO8nMWoQclg7Tk9O8wK7JaoFKJIWI7S3BDunTVq8', 'scope': ['user-read-currently-playing'], 'expires_at': 1699752664.6937788}"

# test_json = json.loads(test)
# print(test_json)

while True:
    try:
        spotify.token = readToken()
        response = spotify.get('https://api.spotify.com/v1/me/player/currently-playing')
        response_json = json.loads(response.content)
        if 'error' in list(response_json.keys()):
            raise IndexError
        print(response_json)
    except IndexError:
        getNewToken()
    except json.decoder.JSONDecodeError:
        getNewToken()
        
    time.sleep(1)

