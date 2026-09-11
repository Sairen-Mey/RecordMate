from classes import Note, RangeNote




def save_note(note:Note) -> None:
    with open("data/notes.txt", "a", encoding="utf-8") as file:
        line = f"{note.timecode}-{note.text}\n"
        file.write(line)

def save_range_note(range_note:RangeNote):
    with open("data/notes.txt", "a", encoding="utf-8") as file:
        line = f"{range_note.obs_timecode_start}|{range_note.obs_timecode_end}-{range_note.text}"
        file.write(line)