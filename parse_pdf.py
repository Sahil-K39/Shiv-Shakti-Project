import fitz

doc = fitz.open("Image to PDF 20260818 14.45.32.pdf")
for i in range(min(5, len(doc))):
    text = doc[i].get_text()
    if text.strip():
        print(f"Page {i} text: {text}")
