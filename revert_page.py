import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# Replace the hacky logic with the original simple logic
content = re.sub(
    r"const productsWithBg = products\.filter\(p => \{[\s\S]*?\}\);\s*const featuredProducts = .*?;\s*const marqueeProducts = .*?;",
    "const featuredProducts = products.slice(0, 8);\n  const marqueeProducts = products.slice(8, 28);",
    content
)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
