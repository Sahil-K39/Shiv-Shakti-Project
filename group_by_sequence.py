import os
import glob
import re

files = glob.glob("All Products/Aug 1*/*.jpg")

def extract_seq(f):
    m = re.search(r'153A(\d+)', f)
    if m:
        return int(m.group(1))
    return 0

files.sort(key=extract_seq)

for f in files[:20]:
    print(os.path.basename(f))
