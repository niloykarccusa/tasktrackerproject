from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from utils.utils import show_error
from logic.auth import add_user
from utils.utils import resource_path

class AddUsersWindow(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window=main_window
        self.setWindowTitle("Register")
        self.setGeometry(500, 150, 350, 400)
        self.setStyleSheet("background-color: #f8f9fa;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        self.title = QLabel(self)
        pixmap=QPixmap(resource_path("assets/logo.png"))
        pixmap=pixmap.scaled(200,100,Qt.AspectRatioMode.KeepAspectRatio)
        self.title.setPixmap(pixmap)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        self.username.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        layout.addWidget(self.password)

        self.add_btn = QPushButton("Add User")
        self.add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        self.add_btn.clicked.connect(self.handle_add_user)
        layout.addWidget(self.add_btn)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def handle_add_user(self):
        username = self.username.text()
        password = self.password.text()
        add_user(username,password)
        self.close()
        from ui.user_list import UserList
        self.main_window.switch_view(UserList())