import json
import sqlite3
import datetime

with open("data/final-products-import.json", "r") as f:
    data = json.load(f)

conn = sqlite3.connect("shiv_shakti.db")
cursor = conn.cursor()

# Insert or update each product
for p in data["products"]:
    cursor.execute("SELECT id FROM products WHERE sku = ?", (p["sku"],))
    row = cursor.fetchone()

    # image_url is usually the first image
    image_list = json.loads(p["images"])
    image_url = image_list[0] if image_list else ""

    if row:
        print(f"Updating {p['sku']}...")
        cursor.execute("""
            UPDATE products SET 
                name=?, category=?, price=?, description=?, image_url=?, slug=?,
                sale_price=?, is_on_sale=?, collection=?, sizes=?, colors=?,
                images=?, quantity=?, is_featured=?, is_active=?,
                updated_at=?
            WHERE sku=?
        """, (
            p["name"], p["category"], p["price"], p["description"], image_url, p["slug"],
            p["sale_price"], p["sale_active"], p["collection"], p["sizes"], p["colors"],
            p["images"], p["quantity"], p["is_featured"], p["is_active"],
            datetime.datetime.now(), p["sku"]
        ))
    else:
        print(f"Inserting {p['sku']}...")
        cursor.execute("""
            INSERT INTO products (
                name, category, price, description, image_url, slug,
                sale_price, is_on_sale, collection, sizes, colors,
                images, quantity, is_featured, is_active, sku, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["name"], p["category"], p["price"], p["description"], image_url, p["slug"],
            p["sale_price"], p["sale_active"], p["collection"], p["sizes"], p["colors"],
            p["images"], p["quantity"], p["is_featured"], p["is_active"], p["sku"],
            datetime.datetime.now()
        ))

conn.commit()
conn.close()
print("Done seeding database!")
