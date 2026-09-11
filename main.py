from client import obs_reader
from classes import Note, RangeNote
from data.bd import (
    save_range_note_to_db,
    get_range_notes,
    get_range_note_by_id,
    update_range_note_by_id
)




while True:
    action:str = input("1 - to add range note / to close range note | 2 - show info range note by id | 3 - show all range note | 0 - exit loop\n")
    if action == "1":
        obs_record_status = obs_reader.get_record_status()
        if obs_record_status['outputActive']:
            timecode = obs_record_status['outputTimecode']

            range_note_id = int(input("id:"))
            dict_range = get_range_note_by_id(range_note_id=range_note_id)

            range_note = RangeNote()

            text = None
            needed_text = int(input("text-1||0"))
            if needed_text:
                text = input("text:")
                range_note.set_text(text=text)


            if dict_range is None:
                range_note.set_obs_time_start(obs_timecode_start=timecode)
                save_range_note_to_db(range_note=range_note)

            else:
                range_note.set_obs_time_end(obs_timecode_end=timecode)
                update_range_note_by_id(range_note_id=range_note_id, range_note=range_note)
    elif action == "2":
        range_note_id = int(input("id:"))
        dict_range = get_range_note_by_id(range_note_id=range_note_id)

        start = dict_range['start_timecode'] if dict_range['start_timecode'] is not None else "None"
        end = dict_range['end_timecode'] if dict_range['end_timecode'] is not None else "None"
        text = dict_range['text'] if dict_range['text'] is not None else "None"
        print(start, end, text)

    elif action == "3":
        rows = get_range_notes()
        for dict_range in rows:
            start = dict_range['start_timecode'] if dict_range['start_timecode'] is not None else "None"
            end = dict_range['end_timecode'] if dict_range['end_timecode'] is not None else "None"
            text = dict_range['text'] if dict_range['text'] is not None else "None"
            print(start, end, text)

    else:
        print("adios")
        break




#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}