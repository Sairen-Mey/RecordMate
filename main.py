from PySide6.QtWidgets import (
    QApplication
)

from QT.qt_signals import obs_bridge
from QT.qt_ui import MainWindow
import events
from client import obs_manager





app = QApplication()

window = MainWindow()

connection = obs_manager.connect()
print("CONNECTED:", connection)
if connection:
    obs_manager.event_client.callback.register(
        events.on_record_state_changed
    )
    print("OBS callback registered")
    if obs_manager.get_is_obs_active():
        events.start_recording_session()
    else:
        obs_bridge.status_changed.emit(True, False)
else:
    obs_bridge.status_changed.emit(False, False)

window.show()

app.exec()



#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}