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



class RangeNotePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("write a range note")

        self.input_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )


        self.close_note_button = QPushButton("close range note")

        self.close_note_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self.add_button = QPushButton("add range note")

        self.add_button.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        self.notes_list = QListWidget()
        self.current_note = QLabel("selected: none")

        self.back_home_page = QPushButton("back")

        input_layout = QHBoxLayout()

        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.close_note_button)

        layout.addLayout(input_layout)

        layout.addWidget(self.notes_list, 1)
        layout.addWidget(self.current_note)
        layout.addWidget(self.back_home_page)









