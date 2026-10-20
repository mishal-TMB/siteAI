from database import get_db_connection
conn = get_db_connection()
cur = conn.cursor(dictionary=True)
cur.execute("SELECT id, username, email, password_hash, balance FROM users ORDER BY id DESC LIMIT 5")
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()