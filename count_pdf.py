import fitz

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
print(f"Total pages: {len(doc)}")
img_count = 0
for i in range(len(doc)):
    page = doc[i]
    images = page.get_images(full=True)
    img_count += len(images)
print(f"Total images: {img_count}")
