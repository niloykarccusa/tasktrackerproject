from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame, QSizePolicy,QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent

class ProjectList(QWidget):
    def __init__(self,role,user_id):
        super().__init__()
        self.role=role
        self.user_id=user_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        if self.role == "super":
            from logic.tracker import get_all_projects
            projects=get_all_projects()
        else:
            from logic.tracker import get_user_projects
            projects=get_user_projects(self.user_id)

        if not projects:
            no_projects_msg = QLabel("No Projects added")
            no_projects_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_projects_msg.setStyleSheet("font-size: 24px; font-weight: bold; color: grey; margin-top: 50px;")
            layout.addWidget(no_projects_msg)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for project in projects:
                from logic.auth import get_user
                user=get_user(project.client_id)
                project_frame = self.create_project_card(project.name, user.username)
                scroll_layout.addWidget(project_frame)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)

        self.setLayout(layout)

    def create_project_card(self,project_title, assigned_user):
        card = QFrame()
        card.setStyleSheet("""
            border: 1px solid #ccc; 
            border-radius: 8px; 
            padding: 15px; 
            background-color: #f9f9f9;
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        card_layout = QVBoxLayout()
        title_label = QLabel(f"📌 {project_title}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(title_label)
        user_label = QLabel(f"👤 {assigned_user}")
        user_label.setStyleSheet("font-size: 14px; color: #555;")

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(user_label)

        card_layout.addLayout(bottom_layout)
        card.setLayout(card_layout)
        # card.mousePressEvent = lambda event: on_project_card_click(event, project_title, switch_to_tasks)

        return card

    # def on_project_card_click(event: QMouseEvent, project_title, switch_to_tasks):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         switch_to_tasks(project_title)