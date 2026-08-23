from PIL import Image
import os
files = os.listdir("New Products /GO_84")
img = Image.open(f"New Products /GO_84/{files[0]}")
print(f"TopLeft: {img.getpixel((0,0))}")
