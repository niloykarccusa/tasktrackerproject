from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame, QSizePolicy,QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from logic.auth import get_all_sub_users

class UserList(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        users=get_all_sub_users()

        if not users:
            no_users_msg = QLabel("No Users added")
            no_users_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_users_msg.setStyleSheet("font-size: 24px; font-weight: bold; color: grey; margin-top: 50px;")
            layout.addWidget(no_users_msg)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for user in users:
                user_frame = self.create_user_card(user)
                scroll_layout.addWidget(user_frame)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)

        self.setLayout(layout)

    def create_user_card(self,user_obj):
        card = QFrame()
        card.setStyleSheet("""
            border: 1px solid #ccc; 
            border-radius: 8px; 
            padding: 15px; 
            background-color: #f9f9f9;
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        card_layout = QVBoxLayout()
        title_label = QLabel(f"📌 {user_obj.username}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(title_label)
        card.setLayout(card_layout)
        # card.mousePressEvent = lambda event: on_user_card_click(event, user_title, switch_to_tasks)

        return card

    # def on_user_card_click(event: QMouseEvent, user_title, switch_to_tasks):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         switch_to_tasks(user_title)