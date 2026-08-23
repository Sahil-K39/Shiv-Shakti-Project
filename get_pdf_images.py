import fitz

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
os_path = "frontend/public/final-products/pdf_bg"
import os
os.makedirs(os_path, exist_ok=True)
count = 0
for i in range(len(doc)):
    for img in doc[i].get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        path = f"{os_path}/pdf_{count:02d}.jpg"
        with open(path, "wb") as f:
            f.write(base_image["image"])
        count += 1
print(f"Extracted {count} images to {os_path}")
