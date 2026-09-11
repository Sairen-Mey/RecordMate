import sqlite3
from pathlib import Path
import os
from classes import Note, RangeNote

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = (BASE_DIR.parent / "data" / "RM.db").resolve()

def get_conn() -> sqlite3.Connection:
    print("DB FILE:", os.path.abspath(DB_PATH))
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
                text TEXT NOT NULL,
                start_timecode TEXT NOT NULL,
                end_timecode TEXT NOT NULL
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

def get_notes():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT note_id, text, timecode
            FROM notes
        """)

        rows = cursor.fetchall()
        return rows

def get_range_notes():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT range_note_id, text, start_timecode, end_timecode
            FROM range_notes
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
    note = Note("00:00:00.111", "tettetetetetett")
    save_note_to_db(note)
    n2 = get_note_by_id(1)
    print(n2['text'], n2['timecode'])
    # print("DB:", DB_PATH.resolve())