import events
from client import obs_client
from classes import Note
from PySide6.QtCore import Qt
from qt_signals import obs_bridge
from session_page import SessionPage
from home_page import HomePage
from note_page import  NotePage
from db_to_qt import (
    db_session_to_qt_list,
    update_qt_sessions_list,
    db_notes_to_qt,
    update_qt_notes_lits
)
from PySide6.QtWidgets import (
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

        obs_bridge.status_changed.connect(
            self.set_obs_status
        )
        #___________

        # MAIN STACK
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        #___________

        # HOME PAGE

        self.home_page = HomePage()

        #___________

        #SESSION PAGE

        self.session_page = SessionPage()

        #___________

        #NOTE PAGE

        self.note_page = NotePage()

        #___________

        #RANGE NOTE PAGE

        #___________


        # ADD PAGES TO STACK

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.session_page)
        self.stack.addWidget(self.note_page)

        #___________________

        #SIGNALS

        self.note_page.add_button.clicked.connect(self.add_note)
        self.note_page.input_field.returnPressed.connect(self.add_note)
        self.note_page.notes_list.itemClicked.connect(self.note_clicked)

        self.session_page.session_list.itemClicked.connect(self.update_notes_list)

        self.home_page.sessions_button.clicked.connect(
            self.update_sessions_list
        )

        self.home_page.note_button.clicked.connect(
            self.open_note_page
        )

        self.note_page.back_home_page.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )

        self.session_page.back_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )



    def update_notes_list(self, item):
        session_id = item.data(Qt.ItemDataRole.UserRole)

        notes_list = db_notes_to_qt(session_id)

        update_qt_notes_lits(
            notes_list=notes_list,
            list_widget=self.note_page.notes_list
        )

        self.note_page.current_note.setText("selected: none")

        self.stack.setCurrentWidget(self.note_page)

    def update_sessions_list(self):
        sessions_list = db_session_to_qt_list()

        update_qt_sessions_list(
            sessions_list=sessions_list,
            list_widget=self.session_page.session_list
        )

        self.stack.setCurrentWidget(self.session_page)

    def note_clicked(self, item) -> None:
        self.note_page.current_note.setText(
            f"selected: {item.text()} | "
            f"{item.data(Qt.ItemDataRole.UserRole)}"
        )

    def add_note(self):
        text = self.note_page.input_field.text().strip()

        if not text:
            return

        if events.current_session_id is None:
            self.note_page.current_note.setText("No active session")
            return

        try:
            status = obs_client.get_record_status()

            if not status["outputActive"]:
                self.note_page.current_note.setText("OBS is not recording")
                return

            timecode = status["outputTimecode"]

            note = Note(timecode, text)

            note_id = save_note_to_db(
                note,
                events.current_session_id
            )
        except Exception as err:
            self.note_page.current_note.setText(f"Error: {err}")
            return

        self.note_page.notes_list.addItem(
            f"[{note_id}] {note.timecode} | {note.text}"
        )
        self.note_page.input_field.clear()




    def set_obs_status(self, connected:bool, recording:bool):
        if not connected:
            self.home_page.obs_status.setText("OBS: disconnected")
        elif recording:
            self.home_page.obs_status.setText("OBS: recording")
        else:
            self.home_page.obs_status.setText("OBS: connected")

    def check_obs_connection(self):
        try:
            status = obs_client.get_record_status()

            obs_bridge.status_changed.emit(
                True,
                status["outputActive"]
            )
        except Exception:
            obs_bridge.status_changed.emit(False, False)

    def open_note_page(self):
        self.note_page.notes_list.clear()
        self.note_page.current_note.setText("selected: none")
        self.stack.setCurrentWidget(self.note_page)


obs_client.event_client.callback.register(
    events.on_record_state_changed
)