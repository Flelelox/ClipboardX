import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Database:

    def __init__(self):

        db_dir = BASE_DIR / "database"
        db_dir.mkdir(exist_ok=True)

        self.db_path = db_dir / "clipboard.db"

        self.conn = sqlite3.connect(self.db_path)

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clipboard (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            text TEXT NOT NULL,

            tag TEXT NOT NULL,

            favorite INTEGER DEFAULT 0,

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.conn.commit()

    def add_item(self, text, tag):

        self.cursor.execute("""

        INSERT INTO clipboard(text, tag)

        VALUES(?,?)

        """, (text, tag))

        self.conn.commit()

        return self.cursor.lastrowid

    def load_items(self, limit=1000):

        self.cursor.execute("""

        SELECT *

        FROM clipboard

        ORDER BY id DESC

        LIMIT ?

        """, (limit,))

        return [dict(row) for row in self.cursor.fetchall()]

    def search(self, query):

        self.cursor.execute("""

        SELECT *

        FROM clipboard

        WHERE text LIKE ?

        ORDER BY id DESC

        """, (f"%{query}%",))

        return [dict(row) for row in self.cursor.fetchall()]

    def delete_item(self, item_id):

        self.cursor.execute(

            "DELETE FROM clipboard WHERE id=?",

            (item_id,)

        )

        self.conn.commit()

    def favorite(self, item_id, value):

        self.cursor.execute("""

        UPDATE clipboard

        SET favorite=?

        WHERE id=?

        """, (value, item_id))

        self.conn.commit()

    def clear(self):

        self.cursor.execute("DELETE FROM clipboard")

        self.conn.commit()

    def count(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM clipboard"

        )

        return self.cursor.fetchone()[0]

    def get_statistics(self):

        self.cursor.execute("""

        SELECT tag, COUNT(*) as total

        FROM clipboard

        GROUP BY tag

        ORDER BY total DESC

        """)

        return [dict(row) for row in self.cursor.fetchall()]

    def export_txt(self, filename):

        rows = self.load_items()

        with open(filename, "w", encoding="utf-8") as f:

            for row in rows:

                f.write("=" * 60 + "\n")

                f.write(f"ID: {row['id']}\n")

                f.write(f"Дата: {row['created']}\n")

                f.write(f"Тег: {row['tag']}\n")

                f.write(f"Избранное: {bool(row['favorite'])}\n\n")

                f.write(row["text"])

                f.write("\n\n")

    def close(self):

        self.conn.close()