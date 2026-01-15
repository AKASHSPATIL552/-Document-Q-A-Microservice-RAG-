import sqlite3

def init_db():
    conn = sqlite3.connect("metadata.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            chunk_id TEXT,
            uploaded_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_metadata(filename, chunk_id, time):
    conn = sqlite3.connect("metadata.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (filename, chunk_id, uploaded_at) VALUES (?, ?, ?)",
        (filename, chunk_id, time)
    )
    conn.commit()
    conn.close()
