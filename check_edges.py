import cv2
import numpy as np
import glob
import os

files = glob.glob("All Products/Aug 8*/*.jpg")

def extract_seq(f):
    return int(os.path.basename(f).split('-')[0])

files.sort(key=extract_seq)

def get_file(n):
    for f in files:
        if extract_seq(f) == n:
            return f
    return None

def rmse(n1, n2):
    f1, f2 = get_file(n1), get_file(n2)
    if not f1 or not f2: return 999
    
    img1 = cv2.imread(f1)
    img2 = cv2.imread(f2)
    
    # Just center crop
    h, w = img1.shape[:2]
    cy, cx = h//2, w//2
    dy, dx = int(h*0.3), int(w*0.15)
    c1 = img1[cy-dy:cy+dy, cx-dx:cx+dx]
    c2 = img2[cy-dy:cy+dy, cx-dx:cx+dx]
    
    c1 = cv2.resize(c1, (100, 200))
    c2 = cv2.resize(c2, (100, 200))
    
    return np.sqrt(np.mean((c1.astype(float) - c2.astype(float))**2))

print(f"59 vs 60: {rmse(59, 60):.2f}")
print(f"60 vs 61: {rmse(60, 61):.2f}")
print(f"61 vs 62: {rmse(61, 62):.2f}")

print(f"71 vs 72: {rmse(71, 72):.2f}")
print(f"72 vs 73: {rmse(72, 73):.2f}")

print(f"107 vs 108: {rmse(107, 108):.2f}")
print(f"108 vs 109: {rmse(108, 109):.2f}")

