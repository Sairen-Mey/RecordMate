import events
from client import obs_client
from classes import Note, RangeNote, Session
from PySide6.QtCore import Qt
from qt_signals import obs_bridge
from db_to_qt import (
    db_session_to_qt_list,
    update_qt_sessions_list,
    db_notes_to_qt,
    update_qt_notes_lits
)
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


        # OBS STATUS
        self.obs_status = QLabel("OBS: disconnected")

        obs_bridge.status_changed.connect(
            self.set_obs_status
        )
        #___________

        # MAIN STACK
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        #___________

        # HOME PAGE
        self.home_page = QWidget()
        layout = QVBoxLayout()
        self.home_page.setLayout(layout)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("write a note")

        self.input_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.add_button = QPushButton("add note")

        self.add_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self.notes_list = QListWidget()
        self.current_note = QLabel("selected: none")

        sessions_list_button = QPushButton("sessions")

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.add_button, 0)

        layout.addWidget(self.obs_status)
        layout.addLayout(input_layout)
        layout.addWidget(self.notes_list, 1)
        layout.addWidget(self.current_note)
        layout.addWidget(sessions_list_button)

        #___________

        #SESSION PAGE

        self.session_page = QWidget()
        session_layout = QVBoxLayout()
        self.session_page.setLayout(session_layout)

        session_label = QLabel("list of sessions")
        session_page_back_button = QPushButton("back")

        self.session_list = QListWidget()

        session_layout.addWidget(session_label)
        session_layout.addWidget(self.session_list, 1)
        session_layout.addWidget(session_page_back_button)


        # ADD PAGES TO STACK

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.session_page)
        #___________________

        #SIGNALS

        self.add_button.clicked.connect(self.add_note)
        self.input_field.returnPressed.connect(self.add_note)
        self.notes_list.itemClicked.connect(self.note_clicked)
        self.session_list.itemClicked.connect(self.update_notes_list)

        sessions_list_button.clicked.connect(
            self.update_sessions_list
        )

        session_page_back_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )


    def update_notes_list(self, item):
        session_id = item.data(Qt.ItemDataRole.UserRole)

        notes_list = db_notes_to_qt(session_id)

        update_qt_notes_lits(
            notes_list=notes_list,
            list_widget=self.notes_list
        )
        self.current_note.setText("selected: none")
        self.stack.setCurrentWidget(self.home_page)

    def update_sessions_list(self):
        sessions_list = db_session_to_qt_list()

        update_qt_sessions_list(
            sessions_list=sessions_list,
            list_widget=self.session_list
        )

        self.stack.setCurrentWidget(self.session_page)

    def note_clicked(self, item) -> None:
        self.current_note.setText(
            f"selected: {item.text()} | "
            f"{item.data(Qt.ItemDataRole.UserRole)}"
        )

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

        self.notes_list.addItem(
            f"[{note_id}] {note.timecode} | {note.text}"
        )
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