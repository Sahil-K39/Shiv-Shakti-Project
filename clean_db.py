import psycopg2

conn_str = "postgresql://postgres.aynrqlxjwpgzxjpwmjtv:Sahil%40062005%40@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    cur.execute("DELETE FROM products")
    conn.commit()
    print("Deleted all products from Supabase.")
except Exception as e:
    print(e)
