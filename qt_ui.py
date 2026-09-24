import events
from client import obs_client
from classes import Note, RangeNote
from PySide6.QtCore import Qt
from qt_signals import obs_bridge
from range_note_page import RangeNotePage
from session_page import SessionPage
from home_page import HomePage
from note_page import  NotePage
from db_to_qt import (
    db_session_to_qt_list,
    update_qt_sessions_list,
    db_notes_to_qt,
    update_qt_notes_list, db_range_notes_to_qt, update_qt_range_notes_list
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
from sql_to_class import sql_to_range_note


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

        self.range_note_page = RangeNotePage()

        #___________

        self.selected_range_note_item = Note

        # ADD PAGES TO STACK

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.session_page)
        self.stack.addWidget(self.note_page)
        self.stack.addWidget(self.range_note_page)

        #___________________

        #SIGNALS

        self.note_page.add_button.clicked.connect(self.add_note)
        self.note_page.input_field.returnPressed.connect(self.add_note)
        self.note_page.notes_list.itemClicked.connect(self.note_clicked)
        self.range_note_page.notes_list.itemClicked.connect(self.range_note_clicked)
        self.session_page.session_list.itemClicked.connect(self.update_notes_list)

        self.home_page.sessions_button.clicked.connect(
            self.update_sessions_list
        )

        self.home_page.note_button.clicked.connect(
            self.open_note_page
        )

        self.home_page.range_note_button.clicked.connect(
            self.open_range_note_page
        )

        self.range_note_page.add_button.clicked.connect(
            self.add_range_note
        )

        self.range_note_page.notes_list.itemClicked.connect(
            self.selected_range_note
        )

        self.range_note_page.close_note_button.clicked.connect(
            self.close_selected_range_note
        )

        self.note_page.back_home_page.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )

        self.range_note_page.back_home_page.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )

        self.session_page.back_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )




    def selected_range_note(self, item):
        self.selected_range_note_item = item

        self.range_note_page.current_note.setText(
            f"selected: {item.text()}"
        )

    def close_selected_range_note(self):
        if self.selected_range_note_item is None:
            return

        item = self.selected_range_note_item

        range_note_id = item.data(Qt.ItemDataRole.UserRole)

        range_note = sql_to_range_note(get_range_note_by_id(range_note_id=range_note_id))

        if range_note.obs_timecode_end is not None:
            return

        status = obs_client.get_record_status()

        if not status["outputActive"]:
            self.range_note_page.current_note.setText(
                "OBS is not recording"
            )
            return

        timecode = status["outputTimecode"]

        range_note.set_obs_time_end(obs_timecode_end=timecode)

        update_range_note_by_id(range_note_id=range_note_id, range_note=range_note)

        item.setText(
            f"[{range_note.obs_timecode_start}|{range_note.obs_timecode_end}]"
            f"{range_note.text}"
        )

        self.range_note_page.current_note.setText(
            f"[{range_note.obs_timecode_start}|{range_note.obs_timecode_end}]"
            f"{range_note.text}"
        )

    def open_range_note_page(self):
        self.range_note_page.notes_list.clear()
        self.range_note_page.current_note.setText("selected: none")
        self.stack.setCurrentWidget(self.range_note_page)

    def open_note_page(self):
        self.note_page.notes_list.clear()
        self.note_page.current_note.setText("selected: none")
        self.stack.setCurrentWidget(self.note_page)

    def update_range_note_list(self, item):
        session_id = item.data(Qt.ItemDataRole.UserRole)

        range_notes_list = db_range_notes_to_qt(session_id=session_id)

        update_qt_range_notes_list(range_notes_list=range_notes_list, list_widget=self.range_note_page.notes_list)

        self.range_note_page.current_note.setText("selected: none")

        self.stack.setCurrentWidget(self.range_note_page)

    def update_notes_list(self, item):
        session_id = item.data(Qt.ItemDataRole.UserRole)

        notes_list = db_notes_to_qt(session_id)

        update_qt_notes_list(notes_list=notes_list, list_widget=self.note_page.notes_list)

        self.note_page.current_note.setText("selected: none")

        self.stack.setCurrentWidget(self.note_page)

    def update_sessions_list(self):
        sessions_list = db_session_to_qt_list()

        update_qt_sessions_list(
            sessions_list=sessions_list,
            list_widget=self.session_page.session_list
        )

        self.stack.setCurrentWidget(self.session_page)

    def range_note_clicked(self, item):
        self.range_note_page.current_note.setText(
            f"selecteed: {item.text()}"
                f"{item.data(Qt.ItemDataRole.UserRole)}"

        )

    def note_clicked(self, item) -> None:
        self.note_page.current_note.setText(
            f"selected: {item.text()} | "
            f"{item.data(Qt.ItemDataRole.UserRole)}"
        )

    def add_range_note(self):
        if events.current_session_id is None:
            self.range_note_page.current_note.setText("No active session")
            return

        try:
            status = obs_client.get_record_status()

            if not status["outputActive"]:
                self.note_page.current_note.setText("OBS is not recording")
                return

            timecode = status["outputTimecode"]

            range_note = RangeNote()

            range_note.set_obs_time_start(obs_timecode_start=timecode)
        except Exception as err:
            self.range_note_page.current_note.setText(f"Error: {err}")
            return

        range_note_id = save_range_note_to_db(range_note=range_note, session_id=events.current_session_id)

        range_note.set_range_note_id(range_note_id=range_note_id)

        item = QListWidgetItem(
            f"[{range_note.obs_timecode_start}|{range_note.obs_timecode_end}] "
            f"{range_note.text}"
        )

        item.setData(
            Qt.ItemDataRole.UserRole,
            range_note_id
        )

        self.range_note_page.notes_list.addItem(item)

        self.range_note_page.input_field.clear()

    def close_range_note(self, item:QListWidgetItem):
        range_note_id:int = item.data(Qt.ItemDataRole.UserRole)
        print("ID FROM ITEM:", range_note_id)

        range_note = sql_to_range_note(get_range_note_by_id(range_note_id=range_note_id))
        print("FROM DB:", range_note)
        if range_note.obs_timecode_end is None:
            status = obs_client.get_record_status()

            if not status["outputActive"]:
                self.note_page.current_note.setText("OBS is not recording")
                return

            timecode = status["outputTimecode"]

            range_note.set_obs_time_end(obs_timecode_end=timecode)

            update_range_note_by_id(range_note_id=range_note_id, range_note=range_note)

            item.setText(
                f"[{range_note.obs_timecode_start}|{range_note.obs_timecode_end}] "
                f"{range_note.text}"
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




obs_client.event_client.callback.register(
    events.on_record_state_changed
)