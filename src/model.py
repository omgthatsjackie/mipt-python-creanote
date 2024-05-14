import sqlite3


class Note:
    def __init__(self, id, user_id, title, content):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, content TEXT)")
            conn.commit()

    def create_note(self, user_id, title, content):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
            conn.commit()
            return cursor.lastrowid

    def get_notes(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes WHERE user_id=?", (user_id,))
            return [Note(*row) for row in cursor.fetchall()]

    def get_note(self, note_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
            row = cursor.fetchone()
            if row:
                return Note(*row)
            return None

    def update_note(self, note_id, title, content):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
            conn.commit()

    def delete_note(self, note_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
            conn.commit()
