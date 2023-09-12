from PIL import Image

# Open the image
image = Image.open('test.jpg')

# Get the dimensions of the original image
original_width, original_height = image.size

# Calculate the aspect ratio of the original image
aspect_ratio = original_width / original_height

# Calculate the target dimensions (128x64)
target_width = 128
target_height = 64

# If the aspect ratio of the original image is wider than the target, crop the sides
if aspect_ratio > (target_width / target_height):
    new_width = int(original_height * (target_width / target_height))
    left = (original_width - new_width) // 2
    right = left + new_width
    image = image.crop((left, 0, right, original_height))
else:
    # If the aspect ratio is taller or equal, crop the top and bottom
    new_height = int(original_width * (target_height / target_width))
    top = (original_height - new_height) // 2
    bottom = top + new_height
    image = image.crop((0, top, original_width, bottom))

# Resize the image to the target dimensions
image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Save the cropped and downscaled image
image.save('output_image.jpg')

# Close the image file
image.close()