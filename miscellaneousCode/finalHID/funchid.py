import hid
import re
from PIL import Image
import requests

#####################################################
# hid setup
vendor_id     = 0xFEDD
product_id    = 0x0753

usage_page    = 0xFF60
usage         = 0x61
report_length = 32

def clean_song_string(song_string):
    og_regex = r'[^a-zA-Z0-9 ♫()\-*+,./:;_{}[\]#$%^&*@!<>=|\\]`~'
    cleaned_string = re.sub(og_regex, '?', song_string)
    return cleaned_string

def cycleString(input_string, i):
    if len(input_string) > 18:
        
        result = input_string[1:]+input_string[0]
        print(f'input = {input_string}\nresult = {result}')
        # print("cycling")
        # start_index = i % len(input_string)
        # substring = input_string[start_index:] + input_string[:start_index]
        # result = substring[:18]
    else:
        result = input_string
    return result

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])

    # print(f"Manufacturer: {interface.manufacturer}")
    # print(f"Product: {interface.product}")

    return interface

def send_raw_report(track_info,op,data):
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
# image related functions        
        
# pretty much a copy of send_raw_report
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

def get_image_data_new(image_url):
    # sender  = ImageSender(image_url)
    image = Image.open(requests.get(image_url,stream=True).raw).convert('RGB')
    buffer = []
    for row in range(image.height):
        for col in range(image.width):
            rgb = image.getpixel((row, col))
            fsf = rgb_to565(*rgb) 
            buffer.append(fsf)
    
    columns = []
    chunk = []
    for i in range(len(buffer)):
        chunk.extend(buffer[i])
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

    return hidmessages

def image_hid(threads, track_info):
    
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
