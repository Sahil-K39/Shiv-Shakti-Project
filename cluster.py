import cv2
import numpy as np
import glob
import os

files = glob.glob("All Products/Aug 1*/*.jpg") + glob.glob("All Products/Aug 8*/*.jpg")

# We need to sort them by sequence number (the original camera number)
def extract_seq(f):
    import re
    m = re.search(r'153A(\d+)', f)
    if m:
        return int(m.group(1))
    return 0

files.sort(key=extract_seq)

def get_hist(f):
    img = cv2.imread(f)
    if img is None: return None
    
    # Crop the center 30% to only get the dress, ignore the background
    h, w = img.shape[:2]
    # usually dress is in the center
    cy, cx = h//2, w//2
    dy, dx = int(h*0.3), int(w*0.15)
    crop = img[cy-dy:cy+dy, cx-dx:cx+dx]
    
    # convert to HSV
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    return hist

print(f"Loaded {len(files)} files")

products = []
current_product = []
current_hist = None

for f in files:
    hist = get_hist(f)
    if hist is None: continue
    
    if current_hist is None:
        current_product.append(f)
        current_hist = hist
    else:
        # compare
        sim = cv2.compareHist(current_hist, hist, cv2.HISTCMP_CORREL)
        # also check sequence gap
        seq_gap = extract_seq(f) - extract_seq(current_product[-1])
        
        # If it's the same photoshoot, gap shouldn't be massive, and sim should be high
        if sim > 0.6 and seq_gap < 50:
            current_product.append(f)
            # update hist slightly? or keep first
        else:
            products.append(current_product)
            current_product = [f]
            current_hist = hist

if current_product:
    products.append(current_product)

print(f"Grouped into {len(products)} products!")
for i, p in enumerate(products[:10]):
    print(f"Product {i+1}: {len(p)} images")
    for f in p:
        print(f"  {os.path.basename(f)}")
