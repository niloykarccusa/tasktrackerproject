from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QComboBox
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from utils.utils import show_error
from logic.tracker import add_project
from logic.auth import get_all_sub_users
from utils.utils import resource_path

class AddProjectsWindow(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window=main_window
        users = get_all_sub_users()
        self.setWindowTitle("Add Project")
        self.setGeometry(500, 150, 350, 400)
        self.setStyleSheet("background-color: #f8f9fa;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        self.title = QLabel(self)
        pixmap = QPixmap(resource_path("assets/logo.png"))
        pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio)
        self.title.setPixmap(pixmap)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.project_title = QLineEdit()
        self.project_title.setPlaceholderText("Enter Project Title")
        self.project_title.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        layout.addWidget(self.project_title)

        self.user_dropdown = QComboBox()
        self.user_dropdown.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        self.user_dropdown.addItem("Select User", None)
        for user in users:
            self.user_dropdown.addItem(user.username, user.id)
        layout.addWidget(self.user_dropdown)

        self.add_btn = QPushButton("Add Project")
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
        self.add_btn.clicked.connect(self.handle_add_project)
        layout.addWidget(self.add_btn)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def handle_add_project(self):
        project_title = self.project_title.text().strip()
        assigned_user_id = self.user_dropdown.currentData()

        if not project_title:
            show_error("Project title cannot be empty.")
            return

        if assigned_user_id is None:
            show_error("Please select a user to assign.")
            return
        add_project(project_title, assigned_user_id)
        self.close()
        from ui.project_list import ProjectList
        self.main_window.switch_view(ProjectList(self.main_window.user_role,self.main_window.logged_in_user_id))