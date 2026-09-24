from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QLabel,
    QSizePolicy
)



class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.obs_status = QLabel("OBS: disconnected")

        # self.input_field = QLineEdit()
        # self.input_field.setPlaceholderText("write a note")

        # self.input_field.setSizePolicy(
        #     QSizePolicy.Policy.Expanding,
        #     QSizePolicy.Policy.Fixed
        # )

        # self.add_button = QPushButton("add note")

        # self.add_button.setSizePolicy(
        #     QSizePolicy.Policy.Fixed,
        #     QSizePolicy.Policy.Fixed
        # )

        # self.notes_list = QListWidget()
        # self.current_note = QLabel("selected: none")
        self.sessions_button = QPushButton("sessions")

        self.note_button = QPushButton("note")

        self.range_note_button = QPushButton("range note")

        # input_layout = QHBoxLayout()

        # input_layout.addWidget(self.input_field, 1)
        # input_layout.addWidget(self.add_button)

        layout.addWidget(self.obs_status)
        # layout.addLayout(input_layout)
        # layout.addWidget(self.notes_list, 1)
        # layout.addWidget(self.current_note)
        layout.addWidget(self.sessions_button)
        layout.addWidget(self.note_button)
        layout.addWidget(self.range_note_button)