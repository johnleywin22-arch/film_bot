import sqlite3

DB_NAME = "films.db"

def create_table():
    """Ma'lumot bazasida filmlar jadvalini yaratish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            file_id TEXT NOT NULL,
            description TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_film(code: str, title: str, file_id: str, description: str = ""):
    """Bazaga yangi film qo'shish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO films (code, title, file_id, description) VALUES (?, ?, ?, ?)",
            (code.upper(), title, file_id, description)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Kod allaqachon mavjud
    finally:
        conn.close()

def get_film(code: str):
    """Kod bo'yicha filmni topish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT code, title, file_id, description FROM films WHERE code = ?",
        (code.upper(),)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"code": row[0], "title": row[1], "file_id": row[2], "description": row[3]}
    return None

def update_film(code: str, title: str, file_id: str, description: str = ""):
    """Mavjud filmni yangilash"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE films SET title=?, file_id=?, description=? WHERE code=?",
        (title, file_id, description, code.upper())
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_film(code: str):
    """Filmni bazadan o'chirish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films WHERE code=?", (code.upper(),))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_all_films():
    """Barcha filmlar ro'yxatini olish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code, title, description FROM films ORDER BY added_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"code": r[0], "title": r[1], "description": r[2]} for r in rows]

def get_stats():
    """Statistika olish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM films")
    count = cursor.fetchone()[0]
    conn.close()
    return {"total_films": count}
