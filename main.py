from client import obs_reader
from classes import Note, RangeNote
from data.bd import (
    create_session,
    close_session,
    get_sessions,
    save_range_note_to_db,
    save_note_to_db,
    get_notes_by_session,
    get_range_note_by_session,
    update_range_note_by_id,
    update_note_by_id,
    get_range_notes,
    get_range_note_by_id,
    get_notes,
    get_note_by_id
)

current_session_id: int|None = None

def on_record_state_changed(event):
    global current_session_id

    if event.output_state == "OBS_WEBSOCKET_OUTPUT_STARTED":
        current_session_id = create_session("f")
        print("session created")

    elif event.output_state == "OBS_WEBSOCKET_OUTPUT_STOPPED":
        if current_session_id is not None:
            close_session(current_session_id, "a")
            current_session_id = None
        print("session closed")

obs_reader.event_client.callback.register(on_record_state_changed)

while True:
    a = input("aaaaaaaaa")
    if a == "q":
        sessions = get_sessions()
        for session in sessions:
            print(session['session_id'], session['created_at'], session['closed_at'])
    elif a == "ses":
        ses_id = int(input())
        sess_notes = get_notes_by_session(ses_id)
        for note in sess_notes:
            print(note['session_id'],note['timecode'], note['text'])
        print("-------"*3)
        sess_rnotes = get_range_note_by_session(ses_id)
        for rnote in sess_rnotes:
            print(rnote['session_id'], rnote['start_timecode'], rnote['end_timecode'], rnote['text'])

    elif a == "1":
        obs_record_status = obs_reader.get_record_status()
        timecode = obs_record_status['outputTimecode']
        text = input("text:")
        note = Note(timecode, text)
        save_note_to_db(note, current_session_id)
    elif a == "2":
        obs_record_status = obs_reader.get_record_status()
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
            save_range_note_to_db(range_note=range_note, session_id=current_session_id)
        else:
            range_note.set_obs_time_end(obs_timecode_end=timecode)
            update_range_note_by_id(range_note_id=range_note_id, range_note=range_note)

    elif a == "notes":
        sess_notes = get_notes_by_session(current_session_id)
        for note in sess_notes:
            print(note['session_id'],note['timecode'], note['text'])
    elif a == "rnotes":
        sess_rnotes = get_range_note_by_session(current_session_id)
        for rnote in sess_rnotes:
            print(rnote['session_id'], rnote['start_timecode'], rnote['end_timecode'], rnote['text'])



#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}