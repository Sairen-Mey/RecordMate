import sqlite3

from models.classes import RangeNote


def sql_to_range_note(row:sqlite3.Row) -> RangeNote:
    range_note = RangeNote()
    range_note.set_range_note_id(range_note_id=row["range_note_id"])
    range_note.set_obs_time_start(obs_timecode_start=row["start_timecode"])
    range_note.set_obs_time_end(obs_timecode_end=row["end_timecode"])
    range_note.set_text(text=row["text"])

    return range_note
