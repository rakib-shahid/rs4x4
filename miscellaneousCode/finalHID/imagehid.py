from PIL import Image
import requests
# import hidsendz?

def rgb_to565(r, g, b):
    msb = ((r >> 3 & 0x1F) << 3) + (g >> 5 & 0x07)
    lsb = ((g >> 2 & 0x07) << 5) + (b >> 3 & 0x1F)
    return [msb, lsb]

def get_image_bytes(url: str):
    image = Image.open(requests.get(url,stream=True).raw).convert('RGB')
    buffer = []
    for row in range(image.height):
        for col in range(image.width):
            rgb = image.getpixel((col, row))
            fsf = rgb_to565(*rgb) 
            buffer.append(fsf)
    image.close()
    return buffer

def image_hid_messages(image_url):
    image_buffer = get_image_bytes(image_url)
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
    return hidmessages


# def image_hid(track_info,threads):
    
#     hidmessages = image_hid_messages(track_info["image_url"])  
#     i = 0
    
#     while (track_info["is_playing"] and len(threads) == 1 and i < len(hidmessages)):
#         if i == 0:
#             send_image_data(bytes(hidmessages[i]),first=True)
#         if len(hidmessages[i]) == 8:
#             send_image_data(bytes(hidmessages[i]),last=True)
#         else:
#             send_image_data(bytes(hidmessages[i]))
#         i+= 1
#     threads.clear()
#     print("image_hid thread done")