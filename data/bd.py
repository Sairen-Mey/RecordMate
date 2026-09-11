import sqlite3
from pathlib import Path
from classes import Note, RangeNote

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = (BASE_DIR.parent / "data" / "RM.db").resolve()

def get_conn() -> sqlite3.Connection:
    # print("DB FILE:", os.path.abspath(DB_PATH))
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                timecode TEXT NOT NULL
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS range_notes (
                range_note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_timecode TEXT NOT NULL,
                text TEXT,
                end_timecode TEXT 
            );
        """)

        conn.commit()


def save_note_to_db(note:Note) -> int:
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO notes (text, timecode)
            VALUES (?, ?)
        """, (note.text,note.timecode))

        conn.commit()

        return cursor.lastrowid

def get_notes():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT note_id, text, timecode
            FROM notes
        """)

        rows = cursor.fetchall()
        return rows

def get_note_by_id(note_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT note_id, text, timecode
            FROM notes
            WHERE note_id = ?
        """,
        (note_id,)
        )
        row = cursor.fetchone()
        return row



def save_range_note_to_db(range_note:RangeNote):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO range_notes (text, start_timecode, end_timecode)
            VALUES (?, ?, ?)
        """,(
            range_note.text,
            range_note.obs_timecode_start,
            range_note.obs_timecode_end))

        conn.commit()

def update_range_note_by_id(range_note_id:int, range_note:RangeNote):
    with get_conn() as conn:
        conn.execute("""
            UPDATE range_notes 
            SET end_timecode = ?, text = ?
            WHERE range_note_id = ?
        """, (range_note.obs_timecode_end, range_note.text, range_note_id))

        conn.commit()

def get_range_notes():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT range_note_id, text, start_timecode, end_timecode
            FROM range_notes
        """)

        rows = cursor.fetchall()
        return rows


def get_range_note_by_id(range_note_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT range_note_id, text, start_timecode, end_timecode
            FROM range_notes
            WHERE range_note_id = ?
        """,
        (range_note_id,)
        )
        row = cursor.fetchone()
        return row




if __name__ == '__main__':
    # init_db()
    pass