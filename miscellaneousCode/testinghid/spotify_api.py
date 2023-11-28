from spotifykeys import client_id, client_secret, redirect_uri
import requests, base64, webbrowser, json
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

scope = 'user-read-currently-playing'
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

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

# gets token locally or new one online
def getToken():
    token = None
    try:
        token = readToken()
    except:
        authorization_url, state = spotify.authorization_url(auth_url)
        print('Please go here and authorize: ', authorization_url)
        webbrowser.open(authorization_url)
        redirect_response = input('\n\nPaste the full redirect URL here: ')

        auth = HTTPBasicAuth(client_id, client_secret)
        token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
        writeToken(token)
        token = token['access_token']
    finally:
        # print(token)
        return token
        
# returns json of api response
def getCurrentTrack():
    url = 'https://api.spotify.com/v1/me/player/currently-playing/'
    headers = {
        'Authorization':f'Bearer {getToken()}'
    }
    response = requests.get(url,headers=headers)
    try:
        return json.loads(response.content)
    except:
        return None

token = getToken()
getCurrentTrack()
# print(readToken())