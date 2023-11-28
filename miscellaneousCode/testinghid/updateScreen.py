import time
from typing import Iterable
import spotifykeys
from PIL import Image
import requests
import spotipy
import wmi
import hid
import colorsys
import threading

# import math
###################################### 
# spotify setup
SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=spotifykeys.client_id, client_secret=spotifykeys.client_secret, redirect_uri= SPOTIPY_REDIRECT_URI,scope='user-read-currently-playing', show_dialog=True)
spotify = spotipy.Spotify(auth_manager=auth_manager)

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
product_id    = 0x0753

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

    request_data = [0x00] * (report_length - 3) # First byte is Report ID
    request_data[1] = op
    request_data[3:len(data)] = data
    if (track_info["is_playing"]):
        request_data[2] = 1
    else:
        request_data[2] = 0
    # print(f"len(request_data) = {len(request_data)}")
    print(f"request_data = {request_data}")
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
# image functions
def send_image_data(data,first = None,last=None):
    # send_raw_report(0xCC,data,offset1,offset2)
    # print(offset)
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length - 4) # First byte is Report ID
    if (first == True):
        request_data[1] = 0xFD
    elif (last == True):
        request_data[1] = 0xFC
    else:
        request_data[1] = 0xFE
    request_data[2:len(data)] = data
    # print(f"len(request_data) = {len(request_data)}")
    print(f"image_data = {request_data}")
    # print(f"Raw bytes = {bytes(request_data)}")

    try:
        interface.write(bytes(request_data))

        # response_report = interface.read(report_length, timeout=1000)
    except Exception as e:
        print(e)
    

def rgb_to565(r, g, b):
    msb = ((r >> 3 & 0x1F) << 3) + (g >> 5 & 0x07)
    lsb = ((g >> 2 & 0x07) << 5) + (b >> 3 & 0x1F)
    return [msb, lsb]


class NoDeviceException(Exception):
    """Custom excption for reporting errors"""

class ImageSender:
    def __init__(self, url: str):
        """Create the 'sender' by storing the Pillow Image and its QMK'ized data"""
        _image = Image.open(requests.get(url,stream=True).raw).convert('RGB')

        _buffer = []
        for row in range(_image.height):
            for col in range(_image.width):
                rgb = _image.getpixel((row, col))
                fsf = rgb_to565(*rgb) 
                _buffer.append(fsf)

        self._image = _image
        self._buffer = _buffer


    def _chunks(self, bytes_per_chunk: int) -> Iterable[list[int]]:
        """Get the raw data in chunks ready to be sent"""
        for offset in range(0, len(self._buffer), bytes_per_chunk):
            # NOTE: last item may be smaller
            yield self._buffer[offset:offset + bytes_per_chunk]
    def send(self, drawing_offset: tuple[int, int] = (0, 0)):
        """Method to send"""

        interface = get_raw_hid_interface()
        print(interface)
        if interface is None:
            raise NoDeviceException

        # TODO: implement a custom message to execute `qp_set_viewport` into the desired range
        # viewport(drawing_offset, self._image.size)

        # -- Send actual pixels
        # NOTE: This relies on your firmware not drawing while you are sending, it would mess up the viewport

        # set up message header
        request = bytearray([0] * report_length)
        request[1] = 0xFE
        n = 30  # whatever this ends up being

        # send data re-using the buffer
        for chunk in self._chunks(n):
            request[2] = len(chunk)
            request[2:2 + len(chunk)] = chunk
            print(request)

            try:
                interface.write(bytes(request))
                response_report = interface.read(report_length, timeout=1000)
            finally:
                interface.close()
def get_image_data_new(image_url):
    sender  = ImageSender(image_url)
    
    image_buffer = sender._buffer
    columns = []
    chunk = []
    for i in range(len(image_buffer)):
        chunk.extend(image_buffer[i])
        if (len(chunk) == 128):
            columns.append(chunk)
            chunk = []

    hidmessages = []
    for column in columns:
        hidmessages.append(column[:30])
        hidmessages.append(column[30:60])
        hidmessages.append(column[60:90])
        hidmessages.append(column[90:120])
        hidmessages.append(column[120:])
    # for i in range(5):
    #     print(hidmessages[i])
    return hidmessages



# def get_image_data(image_url):
#     opened_img = Image.open(requests.get(image_url,stream=True).raw).convert('RGB')

#     pix_data = []

#     pix_counter = 0
#     hid_message_bytes = []
#     for r in range(0,64):
#         for c in range(0,64):
#             # each hid message can send 27 bytes of data
#             if (pix_counter == 30):
#                 pix_data.append(hid_message_bytes)
#                 hid_message_bytes = []
#                 pix_counter = 0
#             curr_px = opened_img.getpixel((r,c))
#             # print(len(opened_img))
#             curr_px = [x / 255 for x in curr_px]
#             curr_px = colorsys.rgb_to_hsv(*curr_px)
#             for val in curr_px:
#                 hid_message_bytes.append(int(val*255))
#             pix_counter += 3
#     # add final message (last 16 bytes)
#     pix_data.append(hid_message_bytes)
#     return pix_data
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
    if len(input_string) > 18:
        start_index = i % len(input_string)
        substring = input_string[start_index:] + input_string[:start_index]
        result = substring[:18]
    else:
        result = input_string
    return result

outString = ''
lastString = ''
cycled = ''
i = 1
apiTimer = 0


def send_image_packet(packet,first,last):
    send_image_data(bytes(packet),first=first,last=last)

def image_hid():
    
    hidmessages = get_image_data_new(track_info["image_url"])  
    i = 0
    
    while (track_info["is_playing"] and len(threads) == 1 and i < len(hidmessages)):
        if i == 0:
            send_image_data(bytes(hidmessages[i]),first=True)
        if len(hidmessages[i]) == 8:
            send_image_data(bytes(hidmessages[i]),last=True)
        else:
            send_image_data(bytes(hidmessages[i]))
        i+= 1
    threads.clear()
    print("image_hid thread done")

def check_song():
    global song_changed
    global threads
    while True:
        print(track_info)
        try:
            try:
                get_current_track_info()
            except Exception as e:
                print(e)
                print("getting new token")
                auth_manager = spotipy.oauth2.SpotifyOAuth(spotifykeys.client_id, spotifykeys.client_secret, redirect_uri= SPOTIPY_REDIRECT_URI,scope='user-read-currently-playing', show_dialog=True)
                spotify = spotipy.Spotify(auth_manager=auth_manager)
                get_current_track_info()
            if not (track_info["image_url"] == old_track_info["image_url"]):
                
                if (len(threads) == 0):
                    image_thread = threading.Thread(target=image_hid)
                    image_thread.start()
                    threads.append(image_thread)
                else:
                    threads.append(1)
                    time.sleep(.05)
                    image_thread = threading.Thread(target=image_hid)
                    image_thread.start()
                    threads.append(image_thread)
                    
                
                
                
            time.sleep(0.33)
            old_track_info["is_playing"] = track_info["is_playing"]
            old_track_info["track_name"] = track_info["track_name"]
            old_track_info["artist_name"] = track_info["artist_name"]
            old_track_info["image_url"] = track_info["image_url"]
        except TypeError:
            track_info["is_playing"] = False
            track_info["track_name"] = ""
            track_info["artist_name"] = ""
            track_info["image_url"] = ""

threads = []
song_changed = threading.Event()
song_change_thread = threading.Thread(target=check_song)
song_change_thread.daemon = True
song_change_thread.start()


while True:
    try:
        if (track_info["is_playing"]):
            outString = f'♫ {track_info["artist_name"]} - {track_info["track_name"]} '
            if not (outString == lastString):
                i = 1
                send_raw_report(0xFF, bytes(outString[:18],'utf-8'))
                cycled = outString
            else:
                if len(outString) > 18:
                    send_raw_report(0xFF,bytes(cycleString(outString,i),'utf-8'))
                    i += 1
                else:
                    send_raw_report(0xFF, bytes(cycleString(outString,i),'utf-8'))
                
        else:
            send_raw_report(0xFF, bytes("",'utf-8'))

            i = 0
        apiTimer += 1
        time.sleep(.33)
        lastString = outString
        
    except FileNotFoundError:
        print("Device not connected")
    except hid.HIDException:
        print("unable to open device")
    