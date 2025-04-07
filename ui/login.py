from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from logic.auth import login
from utils.utils import show_error
from utils.utils import resource_path

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
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

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet(
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
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.register_label = QLabel('<a href="#">Register if you don\'t have an account</a>')
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_label.setStyleSheet("color: #007bff; font-size: 12px;")
        self.register_label.setOpenExternalLinks(False)
        self.register_label.linkActivated.connect(self.open_register)
        layout.addWidget(self.register_label)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
        if login(username, password):
            self.open_main_window()
        else:
            show_error("Login Failed!!Please check your credentials again.")

    def open_main_window(self):
        from ui.task_tracker import TaskTrackerWindow
        self.main_window = TaskTrackerWindow()
        self.main_window.show()
        self.close()

    def open_register(self):
        from ui.register import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()