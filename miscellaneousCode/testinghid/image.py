import time
from typing import Iterable
import PIL as pil
from PIL import Image
import requests
import hid
import colorsys
import math


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

def send_raw_report(data, op = None,offset = None):
    print(offset)
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        raise FileNotFoundError

    request_data = [0x00] * (report_length - 4) # First byte is Report ID
    request_data[1] = op
    request_data[4:len(data)] = data
    if (offset != None):
        request_data[2] = offset
    print(f"len(request_data) = {len(request_data)}")
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

def printReqs(opened_img):
    first_px = opened_img.getpixel(xy=(0,0))
    dims = opened_img.size
    total_pix = dims[0] * dims[1]
    print(f"Total pixels: {total_pix}")
    print(f"Bytes per pixel = {len(bytearray(first_px))}")
    print(f"Total bytes necessary = {total_pix*len(bytearray(first_px))}")
    print(f"Minimum HID messages needed: {math.ceil(total_pix*len(bytearray(first_px))/27)}")

def send_image_data(data,first = None,last = None):
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
        print("THIS SHOULD HAVE BEEN LAST")
        request_data[1] = 0xFC
    else:
        request_data[1] = 0xFE
    request_data[2:len(data)] = data
    print(f"len(request_data) = {len(request_data)}")
    print(f"request_data = {request_data}")
    # print(f"Raw bytes = {bytes(request_data)}")
    request_report = bytes(request_data)

    try:
        interface.write(request_report)

        response_report = interface.read(report_length, timeout=1000)
    except Exception as e:
        print(e)
    

def get_image_data(image_url):
    opened_img = Image.open(requests.get(image_url,stream=True).raw)

    pix_data = []

    pix_counter = 0
    hid_message_bytes = []
    for r in range(0,64):
        for c in range(0,64):
            # each hid message can send 27 bytes of data
            if (pix_counter == 30):
                pix_data.append(hid_message_bytes)
                hid_message_bytes = []
                pix_counter = 0
            curr_px = opened_img.getpixel((r,c))
            curr_px = [x / 255 for x in curr_px]
            curr_px = colorsys.rgb_to_hsv(*curr_px)
            for val in curr_px:
                hid_message_bytes.append(int(val*255))
            pix_counter += 3
    # add final message (last 16 bytes)
    pix_data.append(hid_message_bytes)
    return pix_data

def rgb_to565(r, g, b):
    msb = ((r >> 3 & 0x1F) << 3) + (g >> 5 & 0x07)
    lsb = ((g >> 2 & 0x07) << 5) + (b >> 3 & 0x1F)
    return [msb, lsb]

def get_image_data_new(image_url):
    sender  = ImageSender(image_url)

    image_buffer = sender._buffer
    sets = []
    chunk = []
    for i in range(len(image_buffer)):
        chunk.extend(image_buffer[i])
        if (len(chunk) == 128):
            sets.append(chunk)
            chunk = []

    hidmessages = []
    for column in sets:
        msg = []
        for i in range(len(column)):
            msg.append(column[i])
            if (len(msg) == 30):
                hidmessages.append(msg)
                msg = []
        hidmessages.append(msg)
    return hidmessages

class NoDeviceException(Exception):
    """Custom excption for reporting errors"""

class ImageSender:
    def __init__(self, url: str):
        """Create the 'sender' by storing the Pillow Image and its QMK'ized data"""
        _image = Image.open(requests.get(image_url,stream=True).raw)

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

image_url = 'https://i.scdn.co/image/ab67616d0000485106ed5d1d101e98e6a270b570'

hidmessages = get_image_data_new(image_url)  
for i in range(6):
    print(hidmessages[i])

# for i in range(len(hidmessages)):
#     if i == 0:
#         send_image_data(bytes(hidmessages[i]),first=True)
#     if len(hidmessages[i]) == 8:
#         send_image_data(bytes(hidmessages[i]),last=True)
#     else:
#         send_image_data(bytes(hidmessages[i]))