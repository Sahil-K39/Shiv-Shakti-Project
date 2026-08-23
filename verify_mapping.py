import sys
# Just visually check dimensions or colors?
# No, let's just generate an HTML file to see them side-by-side.
html = "<html><body><table>"
with open("sorted_photo.txt") as f1, open("sorted_prod.txt") as f2:
    photos = f1.read().splitlines()
    prods = f2.read().splitlines()
    
    for p1, p2 in zip(photos[:20], prods[:20]):
        html += f"<tr><td>{p1}</td><td>{p2}</td></tr>"

html += "</table></body></html>"
with open("verify.html", "w") as f:
    f.write(html)
