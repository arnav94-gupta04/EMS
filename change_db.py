from db import get_connection

conn = get_connection()
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE log_emp ADD COLUMN selfie BLOB;")
except Exception as e:
    print("Column 'selfie' may already exist:", e)

try:
    cur.execute("ALTER TABLE log_emp ADD COLUMN geo_coords TEXT;")
except Exception as e:
    print("Column 'geo_coords' may already exist:", e)

conn.commit()
conn.close()
print("Schema updated successfully.")
