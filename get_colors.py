import os
from PIL import Image

def get_dominant_color(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.jpg') or f.endswith('.png')]
    if not files: return "none"
    img = Image.open(os.path.join(folder, files[0])).convert("RGB")
    # center pixel
    w, h = img.size
    return img.getpixel((w//2, h//2))

print(f"GO_84: {get_dominant_color('All Products/GO_84')}")
print(f"GO_85: {get_dominant_color('All Products/GO_85')}")
print(f"GO_85_1: {get_dominant_color('All Products/GO_85_1')}")
