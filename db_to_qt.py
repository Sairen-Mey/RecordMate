from data.bd import get_sessions, get_notes_by_session, get_range_note_by_session
from classes import Session, Note, RangeNote
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

    notes_list:list[Note] = []

    for row in notes:
        note = Note(
            note_text=row["text"],
            obs_timecode=row["timecode"]
        )
        notes_list.append(note)

    return notes_list

def update_qt_notes_list(notes_list:list[Note], list_widget:QListWidget):
    list_widget.clear()

    for note in notes_list:
        item = QListWidgetItem(
            f"[{note.timecode}] {note.text}"
        )
        list_widget.addItem(item)


def db_range_notes_to_qt(session_id:int) -> list[RangeNote]:
    range_notes = get_range_note_by_session(session_id)

    range_notes_list:list[RangeNote] = []

    for row in range_notes:
        text = row["text"]
        start_timecode = row["start_timecode"]
        end_timecode = row["end_timecode"]
        range_note_id = row["range_note_id"]

        range_note = RangeNote()


        range_note.set_range_note_id(range_note_id)

        if start_timecode:
            range_note.set_obs_time_start(obs_timecode_start=start_timecode)

        if text:
            range_note.set_text(text=text)

        else:
            range_note.set_text(text="[NONE]")

        if end_timecode:
            range_note.set_obs_time_end(obs_timecode_end=end_timecode)
        else:
            range_note.set_obs_time_end(obs_timecode_end="[NONE]")

        range_notes_list.append(range_note)

    return range_notes_list

def update_qt_range_notes_list(range_notes_list:list[RangeNote], list_widget:QListWidget):
    list_widget.clear()

    for range_note in range_notes_list:
        item = QListWidgetItem(
            f"[{range_note.obs_timecode_start}|{range_note.obs_timecode_end}] {range_note.text}"
        )

        item.setData(
            Qt.ItemDataRole.UserRole,
            range_note.range_note_id
        )

        list_widget.addItem(item)