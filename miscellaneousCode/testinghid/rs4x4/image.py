import PIL as pil
from PIL import Image
import requests
import hid
import colorsys
import math


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

def printReqs(opened_img,dims):
    first_px = opened_img.getpixel(xy=(0,0))
    dims = opened_img.size
    total_pix = dims[0] * dims[1]
    print(f"Total pixels: {total_pix}")
    print(f"Bytes per pixel = {len(bytearray(first_px))}")
    print(f"Total bytes necessary = {total_pix*len(bytearray(first_px))}")
    print(f"Minimum HID messages needed: {total_pix*len(bytearray(first_px))/30}")
    print(len(bytearray(first_px)))

image_url = 'https://i.scdn.co/image/ab67616d0000485106ed5d1d101e98e6a270b570'
opened_img = Image.open(requests.get(image_url,stream=True).raw)

pix_data = []

hid_counter = 0
hid_message_bytes = []
for r in range(0,64):
    for c in range(0,64):
        if (hid_counter == 30):
            pix_data.append(hid_message_bytes)
            hid_message_bytes = []
            hid_counter = 0
        curr_px = opened_img.getpixel((r,c))
        curr_px = [x / 255 for x in curr_px]
        hid_message_bytes.append(colorsys.rgb_to_hsv(*curr_px))
        hid_counter += 1
# add final message (len != 30)
pix_data.append(hid_message_bytes)

# each hid message can send 30 bytes of data, each pix is 3 bytes
total_hid_messages = len(pix_data)
print(pix_data[0])
print()

# first_px = opened_img.getpixel(xy=(0,0))
# first_px = [x / 255 for x in first_px]
# print(first_px)
# print(colorsys.rgb_to_hsv(*first_px))