from PIL import Image, ImageSequence

image_old = 'image\\space.gif'
im = Image.open(image_old)
# im = im.convert('1')

print(im.mode)
print("gif frames = " + str(im.n_frames))

i=0
for frame in ImageSequence.Iterator(im):
    i += 1
    
    # Get the dimensions of the original image
    original_width, original_height = frame.size

    # Calculate the aspect ratio of the original image
    aspect_ratio = original_width / original_height

    # Calculate the target dimensions (128x64)
    target_width = 128
    target_height = 64
    frame = frame.convert('1')
    # If the aspect ratio of the original image is wider than the target, crop the sides
    if aspect_ratio > (target_width / target_height):
        new_width = int(original_height * (target_width / target_height))
        left = (original_width - new_width) // 2
        right = left + new_width
        frame = frame.crop((left, 0, right, original_height))
    else:
        # If the aspect ratio is taller or equal, crop the top and bottom
        new_height = int(original_width * (target_height / target_width))
        top = (original_height - new_height) // 2
        bottom = top + new_height
        frame = frame.crop((0, top, original_width, bottom))

    # Resize the image to the target dimensions
    frame = frame.resize((target_width, target_height), Image.Resampling.LANCZOS)
    frame.save("image\\frames\\"+str(i)+".pbm", lossless = True)
im.close()
imm = Image.open("image\\frames\\1.pbm")
print(imm.mode)