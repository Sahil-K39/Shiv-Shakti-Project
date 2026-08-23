import re

with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

# Replace the filter logic
old_logic = """        const studioProducts = data.filter(p => {
          return p.slug.startsWith('aug1_') || p.slug.startsWith('aug8_');
        });
        setProducts(studioProducts.length > 0 ? studioProducts : data);"""

new_logic = """        // Show all products, but reverse so newest (GO-93) show first
        setProducts(data.slice().reverse());"""

content = content.replace(old_logic, new_logic)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
