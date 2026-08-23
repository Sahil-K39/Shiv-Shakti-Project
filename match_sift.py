import cv2
import numpy as np
import glob
import os

aug_files = glob.glob("All Products/Aug 1*/*.jpg") + glob.glob("All Products/Aug 8*/*.jpg")
go_folders = sorted([d for d in os.listdir("All Products") if d.startswith("GO_")])

print(f"Loading {len(aug_files)} Aug images...")
aug_kp_des = []
sift = cv2.SIFT_create()

for f in aug_files:
    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    if img is None: continue
    img = cv2.resize(img, (400, 600))
    kp, des = sift.detectAndCompute(img, None)
    aug_kp_des.append((f, kp, des))

print("Matching...")
bf = cv2.BFMatcher()

for go in go_folders[:3]:
    files = glob.glob(f"All Products/{go}/*.jpg") + glob.glob(f"All Products/{go}/*.png")
    if not files: continue
    
    img = cv2.imread(files[0], cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (400, 600))
    kp1, des1 = sift.detectAndCompute(img, None)
    
    best_match = None
    best_good = 0
    
    for f, kp2, des2 in aug_kp_des:
        if des2 is None: continue
        matches = bf.knnMatch(des1, des2, k=2)
        good = 0
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good += 1
        
        if good > best_good:
            best_good = good
            best_match = f
            
    print(f"{go} -> {os.path.basename(best_match)} (good matches: {best_good})")

