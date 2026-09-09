from client import obs_reader
from classes import Note, RangeNote
from note_saver import save_note


range_note:dict[int,RangeNote] = {}
range_note[0] = RangeNote()
idishnik = 0

while True:
    action:str = input("1 - add note | 2 - add rang note | 0 - exit loop\n")
    if action == "1":
        obs_record_status = obs_reader.get_record_status()
        if obs_record_status['outputActive']:
            timestamp = obs_record_status['outputTimecode']
            text = input("text:")
            note = Note(obs_timestamp=timestamp, note_text=text)
            save_note(note=note)
        else:
            print("record is not active")
            break
    elif action == "2":
        obs_record_status = obs_reader.get_record_status()
        if obs_record_status['outputActive']:
            time = obs_record_status['outputTimecode']
            if range_note[idishnik].obs_timestamp_start is None and range_note[idishnik].obs_timestamp_end is None:
                range_note[idishnik] = RangeNote()
            if range_note[idishnik].obs_timestamp_start is None:
                text = input("\n")
                range_note[idishnik].note_text=text
                range_note[idishnik].set_obs_time_start(obs_timestamp_start=time)
            else:
                range_note[idishnik].set_obs_time_end(obs_timestamp_end=time)
        else:
            print("record is not active")
            break
    elif action == "3":
        range_note[idishnik].note_info()
    else:
        print("adios")
        break




#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}