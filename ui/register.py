from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from utils.utils import show_error
from logic.auth import register
from utils.utils import resource_path

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
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

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        layout.addWidget(self.confirm_password)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet(
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
        self.register_btn.clicked.connect(self.handle_register)
        layout.addWidget(self.register_btn)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.login_label = QLabel('<a href="#">Already have an account? Login</a>')
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setStyleSheet("color: #007bff; font-size: 12px;")
        self.login_label.setOpenExternalLinks(False)
        self.login_label.linkActivated.connect(self.open_login)
        layout.addWidget(self.login_label)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if password == confirm_password:
            if register(username, password):
                self.open_login()
            else:
                show_error("Registration Failed")
        else:
            show_error("Passwords don't match")

    def open_login(self):
        from ui.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()