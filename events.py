from QT.qt_signals import obs_bridge
from data.bd import create_session,close_session
from timemodul import get_date_and_time
current_session_id: int|None = None


def start_recording_session():
    global current_session_id
    print("START SESSION CALLED:", current_session_id)
    if current_session_id is not None:
        return

    current_session_id = create_session(get_date_and_time())
    print("SESSION CREATED:", current_session_id)
    obs_bridge.status_changed.emit(True, True)


def on_record_state_changed(event):
    global current_session_id
    print("EVENT RECEIVED:", event.output_state)
    if event.output_state == "OBS_WEBSOCKET_OUTPUT_STARTED":
        print("START EVENT")
        # current_session_id = create_session("f")
        # obs_bridge.status_changed.emit(True, True)
        start_recording_session()

    elif event.output_state == "OBS_WEBSOCKET_OUTPUT_STOPPED":
        if current_session_id is not None:
            close_session(current_session_id, get_date_and_time())
            current_session_id = None
        obs_bridge.status_changed.emit(True, False)
