import fitz
import os
from PIL import Image

pdf_path = "Image to PDF 20260818 14.45.32.pdf"
doc = fitz.open(pdf_path)

out_dir = "pdf_extracted"
os.makedirs(out_dir, exist_ok=True)

for i in range(len(doc)):
    page = doc[i]
    image_list = page.get_images()
    if image_list:
        xref = image_list[0][0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        with open(f"{out_dir}/{i+1:02d}.jpg", "wb") as f:
            f.write(image_bytes)

print(f"Extracted {len(os.listdir(out_dir))} images.")
