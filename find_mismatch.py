with open("sorted_photo.txt") as f1, open("sorted_prod.txt") as f2:
    photos = f1.read().splitlines()
    prods = f2.read().splitlines()

# We can't know the exact mismatch just by looking at lists if they are completely different names.
# But wait, we can just use the index mapping if we assume 1 image was dropped at the very end, or somewhere else.
# Actually, the user says "use the products like Image to PDF 20260818 14.45.32".
# Wait, let's just copy the 124 Products images using the exact sorted mapping!
# Let's verify by just printing the mapped names.
for i in range(124):
    print(f"{photos[i]} -> {prods[i]}")
