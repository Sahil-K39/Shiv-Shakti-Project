import fitz

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
for i in range(len(doc)):
    page = doc[i]
    images = page.get_images(full=True)
    for idx, img in enumerate(images):
        print(f"Page {i} Image {idx}: {img[2]}x{img[3]}")
