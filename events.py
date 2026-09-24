from QT.qt_signals import obs_bridge
from data.bd import create_session,close_session

current_session_id: int|None = None

def on_record_state_changed(event):
    global current_session_id

    if event.output_state == "OBS_WEBSOCKET_OUTPUT_STARTED":
        current_session_id = create_session("f")
        obs_bridge.status_changed.emit(True, True)

    elif event.output_state == "OBS_WEBSOCKET_OUTPUT_STOPPED":
        if current_session_id is not None:
            close_session(current_session_id, "a")
            current_session_id = None
        obs_bridge.status_changed.emit(True, False)
