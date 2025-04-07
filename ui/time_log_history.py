from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame, QSizePolicy, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime

class TimeLogHistory(QWidget):
    def __init__(self, role, user_id):
        super().__init__()
        self.role = role
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        if self.role == "super":
            from logic.tracker import get_all_task_ordered_time_logs, get_time_log_distinct_tasks
            time_logs = get_all_task_ordered_time_logs()
            distinct_tasks = get_time_log_distinct_tasks()
        else:
            from logic.tracker import get_user_task_ordered_time_logs, get_time_log_distinct_tasks
            time_logs = get_user_task_ordered_time_logs(self.user_id)
            distinct_tasks = get_time_log_distinct_tasks(self.user_id)

        if not time_logs:
            no_time_logs_msg = QLabel("Time hasn't been tracked for any tasks.")
            no_time_logs_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_time_logs_msg.setStyleSheet("font-size: 24px; font-weight: bold; color: grey; margin-top: 50px;")
            layout.addWidget(no_time_logs_msg)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for task_id in distinct_tasks:
                from logic.tracker import get_task
                task = get_task(task_id)
                task_frame = self.create_task_card(task, time_logs)
                scroll_layout.addWidget(task_frame)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)

        self.setLayout(layout)

    def create_task_card(self, task, time_logs):
        card = QFrame()
        card.setStyleSheet("""
            border: 1px solid #ccc; 
            border-radius: 8px; 
            padding: 15px; 
            background-color: #f9f9f9;
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        card_layout = QVBoxLayout()
        task_label = QLabel(task.description)
        task_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        card_layout.addWidget(task_label)

        task_logs = [log for log in time_logs if log.task_id == task.id]

        for log in task_logs:
            from logic.auth import get_user
            assigned_user = get_user(log.user_id)
            start_time = log.start_time
            end_time = log.end_time
            if end_time is None:
                log_time="In Progress"
            else:
                start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                diff=end-start
                total_seconds = int(diff.total_seconds())
                hh = total_seconds // 3600
                mm = (total_seconds % 3600) // 60
                ss = total_seconds % 60

                log_time = f"{hh:02}:{mm:02}:{ss:02}" if total_seconds > 0 else "00:00:00"
            
            log_label = QLabel(f"{log_time} - {assigned_user.username}")
            log_label.setStyleSheet("font-size: 12px; color: grey;")
            log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(log_label)

        card.setLayout(card_layout)
        return card