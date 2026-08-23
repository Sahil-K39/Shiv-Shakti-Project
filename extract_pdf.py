import sys
import subprocess

try:
    import fitz
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF", "Pillow"])
    import fitz

from PIL import Image
import io

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
page = doc[0]
image_list = page.get_images(full=True)
if image_list:
    xref = image_list[0][0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    print(f"PDF Image 1 size: {img.size}")
    print(f"PDF Image 1 top-left pixel: {img.getpixel((0,0))}")
else:
    print("No images found on page 1")
