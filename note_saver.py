from classes import Note




def save_note(note:Note) -> None:
    with open("data/notes.txt", "a", encoding="utf-8") as file:
        line = f"{note.timestamp}-{note.text}\n"

        file.write(line)

