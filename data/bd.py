import sqlite3
from pathlib import Path
from classes import Note, RangeNote

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = (BASE_DIR.parent / "data" / "RM.db").resolve()

def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                closed_at TEXT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                timecode TEXT NOT NULL,
                
                FOREIGN KEY (session_id)
                REFERENCES sessions(session_id)
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS range_notes (
                range_note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                start_timecode TEXT NOT NULL,
                text TEXT,
                end_timecode TEXT,
                
                FOREIGN KEY (session_id)
                REFERENCES sessions(session_id) 
            );
        """)

        conn.commit()


def create_session(date:str) -> int:
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO sessions (created_at)
            VALUES (?) 
        """, (date,))

        return cursor.lastrowid

def close_session(session_id:int, date:str):
    with get_conn() as conn:
        conn.execute("""
            UPDATE sessions
            SET closed_at = ?
            WHERE session_id = ?
        """, (date, session_id,))

def get_sessions():
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT session_id, created_at, closed_at
            FROM sessions
        """)

        row = cursor.fetchall()

        return row

def save_note_to_db(note:Note, session_id:int) -> int:
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO notes (session_id, text, timecode)
            VALUES (?, ?, ?)
        """, (session_id, note.text, note.timecode))

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

def get_notes_by_session(session_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT note_id, session_id, text, timecode
            FROM notes
            WHERE session_id = ?
        """, (session_id,))

        rows = cursor.fetchall()
        return rows

def get_note_by_id(note_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT note_id, session_id, text, timecode
            FROM notes
            WHERE note_id = ?
        """,
        (note_id,))
        row = cursor.fetchone()
        return row


def update_note_by_id(note_id:int, note:Note):
    with get_conn() as conn:
        conn.execute("""
            UPDATE notes
            SET text = ?
            WHERE note_id = ?
        """, (note.text, note_id))


def save_range_note_to_db(range_note:RangeNote, session_id:int):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO range_notes (session_id, text, start_timecode, end_timecode)
            VALUES (?, ?, ?, ?)
        """,(
            session_id,
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
            SELECT range_note_id, session_id, text, start_timecode, end_timecode
            FROM range_notes
        """)

        rows = cursor.fetchall()
        return rows


def get_range_note_by_id(range_note_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT range_note_id, session_id, text, start_timecode, end_timecode
            FROM range_notes
            WHERE range_note_id = ?
        """,
        (range_note_id,))
        row = cursor.fetchone()
        return row

def get_range_note_by_session(session_id:int):
    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT range_note_id, session_id, text, start_timecode, end_timecode
            FROM range_notes
            WHERE session_id = ?
        """,(session_id,))
        row = cursor.fetchall()
        return row


if __name__ == '__main__':
    # init_db()
    pass