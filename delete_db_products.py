import psycopg2

conn_str = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    # We want to delete products that have sku starting with SS-FINAL-GO- and the number is >= 42
    cur.execute("SELECT id, sku FROM products WHERE sku LIKE 'SS-FINAL-GO-%'")
    rows = cur.fetchall()
    
    count = 0
    for row in rows:
        pid = row[0]
        sku = row[1]
        try:
            num = int(sku.replace("SS-FINAL-GO-", "").split("-")[0])
            if num >= 42:
                cur.execute("DELETE FROM products WHERE id = %s", (pid,))
                count += 1
        except:
            pass
            
    conn.commit()
    print(f"Deleted {count} products from Supabase.")
except Exception as e:
    print(e)
