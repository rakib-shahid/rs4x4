import PIL as pil
from PIL import Image
import requests
import hid
import colorsys


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

def printReqs(first_px,total_pix):
    print(f"Total pixels: {total_pix}")
    print(f"Bytes per pixel = {len(bytearray(first_px))}")
    print(f"Total bytes necessary = {total_pix*len(bytearray(first_px))}")
    print(f"Minimum HID messages needed: {total_pix*len(bytearray(first_px))/30}")
    print(len(bytearray(first_px)))

image_url = 'https://i.scdn.co/image/ab67616d0000485106ed5d1d101e98e6a270b570'
opened_img = Image.open(requests.get(image_url,stream=True).raw)

dims = opened_img.size
total_pix = dims[0] * dims[1]

pix_data = []

first_px = opened_img.getpixel(xy=(0,0))
for r in range(0,64):
    for c in range(0,64):
        curr_px = opened_img.getpixel((r,c))
        pix_data.append(colorsys.rgb_to_hsv(curr_px[0],curr_px[1],curr_px[2]))