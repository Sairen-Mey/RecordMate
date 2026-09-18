from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget
)



class SessionPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        # self.setLayout(layout)

        session_label = QLabel("list of sessions")
        self.back_button = QPushButton("back")
        self.session_list = QListWidget()

        layout.addWidget(session_label)
        layout.addWidget(self.session_list, 1)
        layout.addWidget(self.back_button)
