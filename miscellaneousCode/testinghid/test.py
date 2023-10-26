import requests
import apikey
import time
import wmi

user = 'rshahid10'
key = apikey.key
url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={key}&limit=1&format=json'
# print(apikey.key)

lastString = "Not playing anything"
outString = "Not playing anything"
nowplaying = False

def getCurrentSong(url, lastString, outString, nowplaying):
    response = requests.get(url)
    data = response.json()
    nowplaying = None
    try:
        trackName = data['recenttracks']['track'][0]['name']
        artistName = data['recenttracks']['track'][0]['artist']['#text']
    except KeyError:
        print("KeyError encountered, idk what to do lol")
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
    return lastString, outString, nowplaying

def getTemps():
    cpuTemp = 0
    gpuTemp = 0
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        
        if sensor.SensorType==u'Temperature':
            if "cpu package" in (sensor.Name).lower():
                print("CPU")
                print(sensor.Value)
                cpuTemp = sensor.Value
            if "gpu core" in (sensor.Name).lower():
                print("GPU")
                print(sensor.Value)
                gpuTemp = sensor.Value
    return cpuTemp,gpuTemp


getTemps()
while True:
    # lastString, outString, nowplaying = getCurrentSong(url,lastString,outString,nowplaying)
    # lastString = outString
    getTemps()
    
    # time.sleep(1)
    

        