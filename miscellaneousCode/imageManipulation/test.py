from PIL import Image, ImageSequence
import os
import requests

# Open the image
# for i in range(1,3):
# image = Image.open('space.gif')
# image = image.convert('1')
# image.save("bw.gif", lossless = True)

def convert_gif_to_monochrome_and_resize(input_path, output_path, new_width=None):
    # Open the original GIF
    with Image.open(input_path) as img:
        # Create a list to hold the converted and resized frames
        frames = []

        # Iterate through each frame of the GIF
        for frame in ImageSequence.Iterator(img):
            if new_width != None:
                # Calculate the new height maintaining the aspect ratio
                aspect_ratio = frame.height / frame.width
                new_height = int(new_width * aspect_ratio)

                # Resize the frame
                resized_frame = frame.resize((new_width, new_height))
                monochrome_frame = resized_frame.convert('L')
            # Convert the frame to monochrome (grayscale)
            else:
                monochrome_frame = frame.convert('L')

            # Append the converted frame to the list
            frames.append(monochrome_frame)

        # Save the frames as a new GIF
        frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)

def crop_and_convert(input_path, output_path):
    im = Image.open(input_path)
    # print(im.mode)
    
    frames = []
    i = 0
    for frame in ImageSequence.Iterator(im):
        
        # Get the dimensions of the original image
        original_width, original_height = frame.size

        # Calculate the aspect ratio of the original image
        aspect_ratio = original_width / original_height

        # Calculate the target dimensions (128x64)
        target_width = 32
        target_height = 128
        frame = frame.convert('L').convert('1')
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
        frames.append(frame)
        frame.save("image\\frames\\"+str(i).zfill(3)+".jpg", lossless = True)
        i+=1
        # print(frame.mode)
    # frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, format='GIF')
    print("done")

# Exa
input_file = 'swirl.gif'
crop_and_convert(input_file, input_file[:-4]+'_converted.gif')