from PIL import Image
import requests

image_url = 'https://i.scdn.co/image/ab67616d0000485109fd83d32aee93dceba78517'
def rgb_to565(r, g, b):
    msb = ((r >> 3 & 0x1F) << 3) + (g >> 5 & 0x07)
    lsb = ((g >> 2 & 0x07) << 5) + (b >> 3 & 0x1F)
    return [msb, lsb]

def get_image_bytes(url: str):
    image = Image.open(requests.get(url,stream=True).raw).convert('RGB')
    buffer = []
    print(f"Image dims = {image.width} x {image.height}")
    for row in range(image.height):
        for col in range(image.width):
            rgb = image.getpixel((col, row))
            fsf = rgb_to565(*rgb) 
            buffer.append(fsf)
    image.close()
    return buffer

print(get_image_bytes(image_url))