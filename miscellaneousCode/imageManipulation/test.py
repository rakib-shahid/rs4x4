from PIL import Image
import os

# Open the image
for i in range(1,3):
    image = Image.open(f'image/frames/{i}.bmp')
    image = image.convert('1')
    image.save("image\\frames\\"+str(i)+"bw.bmp", lossless = True)
