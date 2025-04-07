from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QComboBox,QTextEdit
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from utils.utils import show_error
from logic.tracker import add_task
from logic.auth import get_all_sub_users
from logic.tracker import get_all_projects
from utils.utils import resource_path

class AddTasksWindow(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window=main_window
        users = get_all_sub_users()
        projects=get_all_projects()
        self.setWindowTitle("Add Task")
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

        self.task_desc = QTextEdit()
        self.task_desc.setPlaceholderText("Enter Task Description")
        self.task_desc.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        layout.addWidget(self.task_desc)

        self.user_dropdown = QComboBox()
        self.user_dropdown.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        self.user_dropdown.addItem("Select User", None)
        for user in users:
            self.user_dropdown.addItem(user.username, user.id)
        layout.addWidget(self.user_dropdown)

        self.project_dropdown = QComboBox()
        self.project_dropdown.setStyleSheet(
            "padding: 8px; border-radius: 5px; border: 1px solid #ccc; background-color: white;"
        )
        self.project_dropdown.addItem("Select Project", None)
        for project in projects:
            self.project_dropdown.addItem(project.name, project.id)
        layout.addWidget(self.project_dropdown)

        self.add_btn = QPushButton("Add Task")
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
        self.add_btn.clicked.connect(self.handle_add_task)
        layout.addWidget(self.add_btn)

        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    def handle_add_task(self):
        task_desc = self.task_desc.toPlainText()
        assigned_user_id = self.user_dropdown.currentData()
        assigned_project_id = self.project_dropdown.currentData()

        if not task_desc:
            show_error("Task description cannot be empty.")
            return

        if assigned_user_id is None:
            show_error("Please select a user to assign.")
            return

        if assigned_project_id is None:
            show_error("Please select a project to assign.")
            return
        add_task(task_desc, assigned_user_id,assigned_project_id)
        self.close()
        from ui.task_list import TaskList
        self.main_window.switch_view(TaskList(self.main_window,self.main_window.user_role,self.main_window.logged_in_user_id))