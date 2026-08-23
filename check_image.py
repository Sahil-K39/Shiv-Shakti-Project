import os
from PIL import Image

folder = "All Products/Aug 1, 2026 08_03_55 PM (1)"
files = os.listdir(folder)
img = Image.open(os.path.join(folder, files[0]))
print(f"Aug1 TopLeft: {img.getpixel((0, 0))}")
