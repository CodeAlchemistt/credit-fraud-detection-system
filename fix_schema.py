import mysql.connector

conn = mysql.connector.connect(
    host="zephyr.proxy.rlwy.net",
    port=51784,
    user="root",
    password="AiGjhoFBkvmmWsngnEMlAADkoQZzAVTW",
    database="railway"
)

cur = conn.cursor()

try:
    cur.execute("""
        ALTER TABLE transactions
        ADD COLUMN Merchant VARCHAR(255)
    """)
    print("Merchant column added")
except Exception as e:
    print("Merchant:", e)

try:
    cur.execute("""
        ALTER TABLE transactions
        ADD COLUMN Risk_Score INT
    """)
    print("Risk_Score column added")
except Exception as e:
    print("Risk_Score:", e)

conn.commit()

cur.close()
conn.close()

print("Done")