from data.bd import get_sessions, get_notes_by_session
from classes import Session, Note
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


def db_session_to_qt_list() -> list[Session]:
    sessions = get_sessions()

    sessions_list = []

    for row in sessions:
        session = Session(
            session_id=row["session_id"],
            started_at=row["created_at"],
            closed_at=row["closed_at"]
        )

        sessions_list.append(session)

    return sessions_list

def update_qt_sessions_list(sessions_list:list[Session], list_widget:QListWidget):
    list_widget.clear()

    for session in sessions_list:
        item = QListWidgetItem(
            f"Session {session.session_id} | "
            f"{session.started_at} - {session.closed_at}"
        )

        item.setData(
            Qt.ItemDataRole.UserRole,
            session.session_id
        )
        list_widget.addItem(item)


def db_notes_to_qt(session_id:int) -> list[Note]:
    notes = get_notes_by_session(session_id)

    notes_list = []

    for row in notes:
        note = Note(
            note_text=row["text"],
            obs_timecode=row["timecode"]
        )
        notes_list.append(note)

    return notes_list

def update_qt_notes_lits(notes_list:list[Note], list_widget:QListWidget):
    list_widget.clear()

    for note in notes_list:
        item = QListWidgetItem(
            f"[{note.timecode}] {note.text}"
        )
        list_widget.addItem(item)