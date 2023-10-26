import sys
import hid

import requests
import apikey
import time

import wmi

vendor_id     = 0xFEDD
product_id    = 0x0753

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    # print(f"Manufacturer: {interface.manufacturer}")
    # print(f"Product: {interface.product}")

    return interface

def send_raw_report(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)

    # print("Request:")
    # print(request_report)

    try:
        interface.write(request_report)

        response_report = interface.read(report_length, timeout=1000)

        # print("Response:")
        # print(response_report)
    finally:
        interface.close()

user = 'rshahid10'
key = apikey.key
url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={key}&limit=1&format=json'

lastString = "Not playing anything"
outString = "Not playing anything"
nowplaying = False

def getTemps():
    cpuTemp = 0
    gpuTemp = 0
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature':
            if "cpu package" in (sensor.Name).lower():
                cpuTemp = sensor.Value
            if "gpu core" in (sensor.Name).lower():
                gpuTemp = sensor.Value
    return cpuTemp,gpuTemp

def currentlyPlaying():
    response = requests.get(url)
    data = response.json()
    try:
        if data['recenttracks']['track'][0]['@attr']['nowplaying'] == 'true':
            nowplaying = True
    except:
        nowplaying = False
    return nowplaying

def getCurrentSong(url, lastString, outString, nowplaying):
    response = requests.get(url)
    data = response.json()
    try:
        if data['recenttracks']['track'][0]['@attr']['nowplaying'] == 'true':
            nowplaying = True
    except:
        nowplaying = False
    try:
        trackName = data['recenttracks']['track'][0]['name']
        artistName = data['recenttracks']['track'][0]['artist']['#text']
    except KeyError:
        print("KeyError encountered, idk what to do lol")
    if nowplaying:
        outString = (f"♪ {artistName} - {trackName}")
        # check if state changed, if changed print
    else:
        outString = ("Not playing anything")
        # check if state changed, if changed print
    return lastString, outString, nowplaying

if __name__ == '__main__':
    while True:
        
        lastString, outString, nowplaying = getCurrentSong(url,lastString,outString,nowplaying)
        if nowplaying:
            try:
                send_raw_report(
                    bytes(outString,'utf-8')
                )
            except FileNotFoundError:
                print("Device not connected")
            lastString = outString
        
        if not nowplaying:
            cpuTemp,gpuTemp = getTemps()
            try:
                send_raw_report(
                    bytes(f"CPU {'{:.1f}'.format(cpuTemp)} | GPU {'{:.1f}'.format(gpuTemp)}",'utf-8')
                )
            except FileNotFoundError:
                print("oopsies filenotfounderror")
        
        time.sleep(0.5)
    
    
# with hid.Device(vendor_id, product_id) as h:
# 	print(f'Device manufacturer: {h.manufacturer}')
# 	print(f'Product: {h.product}')
# 	print(f'Serial Number: {h.serial}')