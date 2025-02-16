import sqlite3

def get_connection():
    conn = sqlite3.connect("ems.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable name-based access to columns
    return conn
