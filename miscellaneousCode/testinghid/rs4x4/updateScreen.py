import time
import spotifykeys
from pprint import pprint
import spotipy
import wmi
import hid
###################################### 
# spotify setup
SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=spotifykeys.client_id, client_secret=spotifykeys.client_secret, redirect_uri= SPOTIPY_REDIRECT_URI,scope='user-read-currently-playing', show_dialog=True)
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
        track_info["image_url"] = response["item"]["album"]["images"][2]["url"]
    except TypeError:
        track_info["is_playing"] = False
        track_info["track_name"] = ""
        track_info["artist_name"] = ""
        track_info["image_url"] = ""
#####################################################
# hid setup
vendor_id     = 0xFEDD
product_id    = 0x0754

usage_page    = 0xFF60
usage         = 0x61
report_length = 32
# hid functions
def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    # print(f"Manufacturer: {interface.manufacturer}")
    # print(f"Product: {interface.product}")

    return interface

def send_raw_report(op,data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length - 1) # First byte is Report ID
    request_data[1] = op
    request_data[2:len(data)] = data
    print(len(request_data))
    print(request_data)
    request_report = bytes(request_data)

    # print("Request:")
    # print(request_report)

    try:
        interface.write(request_report)

        response_report = interface.read(report_length, timeout=1000)

        # print("Response:")
        # print(response_report)
    except Exception as e:
        print(e)
#####################################################
# temp function
# noticeably slow
# CURRENTLY UNUSED AS IT SPIKES CPU USAGE
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
    return f"CPU {'{:.1f}'.format(cpuTemp)} | GPU {'{:.1f}'.format(gpuTemp)}"
#####################################################
# function to cycle string
def cycleString(input_string, i):
    if len(input_string) > 21:
        start_index = i % len(input_string)
        substring = input_string[start_index:] + input_string[:start_index]
        result = substring[:21]
    else:
        result = input_string 
    return result

outString = ''
lastString = ''
lastImageUrl = ''
cycled = ''
i = 1
apiTimer = 0

if __name__ == '__main__':
    while True:
        try:
            if (apiTimer % 2 == 0):
                try:
                    get_current_track_info()
                except Exception as e:
                    print(e)
                    print("getting new token")
                    auth_manager = spotipy.oauth2.SpotifyOAuth(spotifykeys.client_id, spotifykeys.client_secret, redirect_uri= SPOTIPY_REDIRECT_URI,scope='user-read-currently-playing', show_dialog=True)
                    spotify = spotipy.Spotify(auth_manager=auth_manager)
                    get_current_track_info()
                
            # print(track_info)
            if (track_info["is_playing"]):
                outString = f'{track_info["artist_name"]} - {track_info["track_name"]}'
                # print(outString)
                if not lastImageUrl == track_info["image_url"]:
                    print(track_info["image_url"])
                    send_raw_report(0xCC,
                        bytes("uhh",'utf-8')
                    )
                if not outString == lastString:
                    i = 1
                    send_raw_report(0xFF,
                        bytes(outString[:21],'utf-8')
                    )
                    cycled = outString
                else:
                    if len(outString) > 21:
                        send_raw_report(0xFF,
                            bytes(cycleString(outString+" | ",i),'utf-8')
                        )
                        i += 1
                    else:
                        send_raw_report(0xFF,
                            bytes(cycleString(outString,i),'utf-8')
                        )
                    
            else:
                send_raw_report(0xFF,
                    bytes("",'utf-8')
                )

                i = 0
            apiTimer += 1
            time.sleep(.25)
            lastString = outString
            lastImageUrl = track_info["image_url"]
        except FileNotFoundError:
            print("Device not connected")
        except hid.HIDException:
            print("unable to open device")