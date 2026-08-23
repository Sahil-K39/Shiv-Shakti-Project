import os
import glob
from PIL import Image
import math

def rmse(img1, img2):
    # crop center 50x150
    w, h = img1.size
    box = (w//2 - 25, h//2 - 75, w//2 + 25, h//2 + 75)
    c1 = img1.crop(box)
    
    w, h = img2.size
    box = (w//2 - 25, h//2 - 75, w//2 + 25, h//2 + 75)
    c2 = img2.crop(box)
    
    # compare
    diff = 0
    d1 = list(c1.getdata())
    d2 = list(c2.getdata())
    for (r1,g1,b1), (r2,g2,b2) in zip(d1, d2):
        diff += (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
    return diff

aug_images = []
for p in glob.glob("All Products/Aug 1*/*.jpg") + glob.glob("All Products/Aug 8*/*.jpg"):
    try:
        img = Image.open(p).convert("RGB")
        img = img.resize((200, 300)) # standard size
        aug_images.append({"path": p, "img": img})
    except:
        pass

print(f"Loaded {len(aug_images)} Aug images")

go_folders = sorted([d for d in os.listdir("All Products") if d.startswith("GO_")])
for go in go_folders[:5]:
    files = glob.glob(f"All Products/{go}/*.jpg") + glob.glob(f"All Products/{go}/*.png")
    if not files: continue
    go_img = Image.open(files[0]).convert("RGB").resize((200, 300))
    
    best = None
    best_d = float('inf')
    for aug in aug_images:
        d = rmse(go_img, aug["img"])
        if d < best_d:
            best_d = d
            best = aug["path"]
            
    print(f"{go} -> {os.path.basename(best)}")
