import requests
import apikey
import time

user = 'rshahid10'
key = apikey.key
url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={key}&limit=1&format=json'
# print(apikey.key)

lastString = "Not playing anything"
outString = "Not playing anything"
nowplaying = False

while True:
    response = requests.get(url)
    data = response.json()
    nowplaying = None
    trackName = data['recenttracks']['track'][0]['name']
    artistName = data['recenttracks']['track'][0]['artist']['#text']
    try:
        if data['recenttracks']['track'][0]['@attr']['nowplaying'] == 'true':
            nowplaying = True
    except:
        nowplaying = False
    if nowplaying:
        outString = (f"{artistName} - {trackName}")
        # check if state changed, if changed print
        if outString != lastString:
            print(outString)
    else:
        outString = ("Not playing anything")
        # check if state changed, if changed print
        if outString != lastString:
            print(outString)
    lastString = outString
    time.sleep(1)
        