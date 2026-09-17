import events
from client import obs_client
from classes import Note, RangeNote
from PySide6.QtCore import Qt
from qt_signals import obs_bridge
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QSizePolicy,
    QStackedWidget,
    QLabel,
    QListWidgetItem
)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Record Mate v1.0")

        self.obs_status = QLabel("OBS: disconnected")

        obs_bridge.status_changed.connect(
            self.set_obs_status
        )

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        home_page = QWidget()

        layout = QVBoxLayout()

        home_page.setLayout(layout)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.current_note = QLabel("selected: none")

        self.stack.addWidget(home_page)

        layout.addWidget(self.obs_status)

        self.input_field = QLineEdit()

        self.input_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.input_field.setPlaceholderText("write a note")

        self.add_button = QPushButton("add note")

        self.add_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self.notes_list = QListWidget()

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.add_button, 0)

        layout.addLayout(input_layout)
        layout.addWidget(self.notes_list, 1)
        layout.addWidget(self.current_note)


        self.add_button.clicked.connect(self.add_note)
        self.input_field.returnPressed.connect(self.add_note)
        self.notes_list.itemClicked.connect(self.note_clicked)


    def note_clicked(self, item) -> None:
        self.current_note.setText(f"selected: {item.text()} | {item.data(Qt.ItemDataRole.UserRole)}")

    def add_note(self):
        text = self.input_field.text().strip()

        if not text:
            return

        if events.current_session_id is None:
            self.current_note.setText("No active session")
            return

        try:
            status = obs_client.get_record_status()

            if not status["outputActive"]:
                self.current_note.setText("OBS is not recording")
                return

            timecode = status["outputTimecode"]

            note = Note(timecode, text)

            note_id = save_note_to_db(
                note,
                events.current_session_id
            )
        except Exception as err:
            self.current_note.setText(f"Error: {err}")
            return

        self.notes_list.addItem(f"[{note_id}] {note.timecode} | {note.text}")
        self.input_field.clear()



    def set_obs_status(self, connected:bool, recording:bool):
        if not connected:
            self.obs_status.setText("OBS: disconnected")
        elif recording:
            self.obs_status.setText("OBS: recording")
        else:
            self.obs_status.setText("OBS: connected")

    def check_obs_connection(self):
        try:
            status = obs_client.get_record_status()

            obs_bridge.status_changed.emit(
                True,
                status["outputActive"]
            )
        except Exception:
            obs_bridge.status_changed.emit(False, False)

obs_client.event_client.callback.register(
    events.on_record_state_changed
)

app = QApplication()

window = MainWindow()

window.show()

app.exec()



#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}