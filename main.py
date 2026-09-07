from client import get_record_status
from classes import Note
from note_saver import save_note




while True:
    action:str = input("1 - add note | 0 - exit loop\n")
    if action == "1":
        obs_record_status = get_record_status()
        if obs_record_status['outputActive']:
            timestamp = obs_record_status['outputTimecode']
            text = input("text:")
            note = Note(obs_timestamp=timestamp, note_text=text)
            # note.note_info()
            save_note(note=note)
        else:
            print("record is not active")
            break
    else:
        print("adios")
        break




#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}