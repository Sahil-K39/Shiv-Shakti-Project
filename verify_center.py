from PIL import Image, ImageChops
import math

with open("sorted_photo.txt") as f1, open("sorted_prod.txt") as f2:
    photos = f1.read().splitlines()
    prods = f2.read().splitlines()

def get_rmse(img1, img2):
    diff = ImageChops.difference(img1, img2)
    h = diff.histogram()
    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    return math.sqrt(sum(sq) / float(img1.size[0] * img1.size[1]))

errors = 0
for i in range(124):
    try:
        p1 = Image.open("Photoroom/" + photos[i]).convert("RGBA")
        p2 = Image.open("Products/" + prods[i]).convert("RGB")
        
        # The products image is 2976x4464
        # The photoroom image is 1512x2016
        # They might be cropped differently.
        # Let's just find the first 5 and see.
    except:
        pass
print("Done")
