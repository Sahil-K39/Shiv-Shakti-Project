import fitz
from PIL import Image
import io

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
for i in range(len(doc)):
    page = doc[i]
    images = page.get_images(full=True)
    for idx, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        with open(f"extracted_{i}_{idx}.jpg", "wb") as f:
            f.write(image_bytes)
        print(f"Extracted {i}_{idx}")
        if i == 0:
            break
    if i == 0:
        break
