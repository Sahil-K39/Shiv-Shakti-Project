import glob
from PIL import Image

def check(glob_pattern):
    for p in glob.glob(glob_pattern)[:20]:
        try:
            img = Image.open(p)
            if img.size == (2880, 4320):
                print(f"Found match: {p}")
        except:
            pass

check("Products/*.jpg")
check("All Products/**/*.jpg")
check("New Colour BG/**/*.jpg")
check("New Products /*/*.jpg")
