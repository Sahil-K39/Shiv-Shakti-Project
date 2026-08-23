from PIL import Image
import glob

def get_bg(path):
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        print(f"{path}: top-left pixel is {img.getpixel((0,0))}")
    except Exception as e:
        print(f"Error: {e}")

for p in glob.glob("Products/*.jpg")[:5]:
    get_bg(p)
