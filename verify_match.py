import os
import glob
from PIL import Image

def get_thumbnail(path):
    img = Image.open(path).convert("RGB")
    img.thumbnail((100, 100))
    return img

go_files = sorted(glob.glob("All Products/GO_48/*.jpg"))
print("GO_48 files:", go_files)

# Just print the first 10 files in Aug 1
aug1_files = sorted(glob.glob("All Products/Aug 1*/*.jpg"))
print("Aug 1 files:", aug1_files[:10])

