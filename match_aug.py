import os
import glob
from PIL import Image, ImageChops
import math
import shutil

def rmse(img1, img2):
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    return math.sqrt(sum(sq) / float(img1.size[0] * img1.size[1]))

print("Loading Aug images...")
aug_images = []
for p in glob.glob("All Products/Aug 1*/*.jpg") + glob.glob("All Products/Aug 8*/*.jpg"):
    try:
        img = Image.open(p).convert("RGB")
        # Crop center slightly to avoid background edge differences if possible
        w, h = img.size
        # Resize small for fast matching
        img = img.resize((64, 96))
        aug_images.append({"path": p, "img": img})
    except:
        pass

print("Matching GO folders to Aug images...")
go_folders = sorted([d for d in os.listdir("All Products") if d.startswith("GO_") and os.path.isdir(os.path.join("All Products", d))])

matches = {}
for go in go_folders:
    # Just take the first image of the product to find the matching Aug image
    go_files = glob.glob(f"All Products/{go}/*.jpg") + glob.glob(f"All Products/{go}/*.png")
    if not go_files:
        continue
        
    try:
        go_img = Image.open(go_files[0]).convert("RGB")
        # Ensure it's not transparent, composite on white
        if go_img.mode == 'RGBA':
            bg = Image.new("RGBA", go_img.size, (255, 255, 255, 255))
            go_img = Image.alpha_composite(bg, go_img).convert("RGB")
        
        go_img = go_img.resize((64, 96))
        
        best_match = None
        best_dist = 1000000
        for aug in aug_images:
            dist = rmse(go_img, aug["img"])
            if dist < best_dist:
                best_dist = dist
                best_match = aug["path"]
                
        matches[go] = best_match
        print(f"Matched {go} to {os.path.basename(best_match)} (dist: {best_dist:.1f})")
    except Exception as e:
        print(f"Error on {go}: {e}")

