from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame, QSizePolicy, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from datetime import datetime,timedelta
from logic.tracker import check_any_timer_active

class TaskList(QWidget):
    def __init__(self,main_window, role, user_id):
        super().__init__()
        self.main_window=main_window
        self.role = role
        self.user_id = user_id
        self.running_tasks = {}
        self.task_buttons={}
        self.timer_labels={}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        if self.role == "super":
            from logic.tracker import get_all_tasks
            tasks = get_all_tasks()
        else:
            from logic.tracker import get_user_tasks
            tasks = get_user_tasks(self.user_id)

        if not tasks:
            no_tasks_msg = QLabel("No Tasks added")
            no_tasks_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_tasks_msg.setStyleSheet("font-size: 24px; font-weight: bold; color: grey; margin-top: 50px;")
            layout.addWidget(no_tasks_msg)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for task in tasks:
                from logic.auth import get_user
                assigned_user = get_user(task.assigned_user_id)
                from logic.tracker import get_project
                project = get_project(task.project_id)
                from logic.tracker import get_user_task_time_logs
                time_logs=get_user_task_time_logs(self.user_id,task.id)
                task_frame = self.create_task_card(task, project.name, assigned_user.username,time_logs)
                scroll_layout.addWidget(task_frame)

                from logic.tracker import check_timer_active
                if(check_timer_active(self.user_id,task.id)):
                    self.start_task_timer(task.id,time_logs)

            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)

        self.setLayout(layout)

    def create_task_card(self, task, project_name, assigned_user,time_logs):
        card = QFrame()
        card.setStyleSheet("""
            border: 1px solid #ccc; 
            border-radius: 8px; 
            padding: 15px; 
            background-color: #f9f9f9;
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        card_layout = QVBoxLayout()

        desc_label = QLabel(task.description)
        desc_label.setFont(QFont("Arial", 14, QFont.Weight.Medium))
        card_layout.addWidget(desc_label)

        project_label = QLabel(f"📂 {project_name}")
        project_label.setStyleSheet("font-size: 12px; color: grey; text-decoration: underline; margin-top: 5px;")
        card_layout.addWidget(project_label)

        bottom_layout = QHBoxLayout()
        user_label = QLabel(f"👤 {assigned_user}")
        user_label.setStyleSheet("font-size: 12px; color: #555;")

        play_pause_button = QPushButton()
        play_pause_button.setFixedSize(30, 30)
        play_pause_button.setText("▶")
        play_pause_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 15px; font-size: 16px;")
        play_pause_button.clicked.connect(lambda: self.toggle_timer(task.id))

        tracked_time=self.calculate_total_tracked_time(time_logs)
        timer_label = QLabel(tracked_time)
        timer_label.setStyleSheet("font-size: 14px; color: #333; padding-left: 10px;")
        

        bottom_layout.addWidget(user_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(play_pause_button)
        bottom_layout.addWidget(timer_label)

        self.task_buttons[task.id]=play_pause_button
        self.timer_labels[task.id]=timer_label

        card_layout.addLayout(bottom_layout)
        card.setLayout(card_layout)

        return card

    def toggle_timer(self, task_id):
        from logic.tracker import get_user_task_time_logs,update_time_log,add_time_log

        if self.running_tasks:
            active_task = list(self.running_tasks.keys())[0]  
            self.running_tasks[active_task]["timer"].stop()
            update_time_log(self.user_id,active_task)
            self.main_window.stop_current_thracker()
            self.running_tasks.pop(active_task,None)
            self.task_buttons[active_task].setText("▶️") 
            self.task_buttons[active_task].setStyleSheet("background-color: #28a745;")
            if task_id == active_task:
                return
        
        time_logs=get_user_task_time_logs(self.user_id,task_id)
        self.start_task_timer(task_id,time_logs)
        add_time_log(self.user_id,task_id)
        if check_any_timer_active(self.user_id):
            self.main_window.instantiate_activity_tracker()

    def start_task_timer(self,task_id,time_logs):
        total_seconds=self.calculate_tracked_seconds(time_logs)
        timer=QTimer(self)
        timer.timeout.connect(lambda: self.update_timer(task_id))
        self.running_tasks[task_id]={"timer":timer,"seconds":total_seconds}
        timer.start(1000)
        self.task_buttons[task_id].setText("⏸️")
        self.task_buttons[task_id].setStyleSheet("background-color: #dc3545; color: white; border-radius: 15px; font-size: 16px;")

    def update_timer(self, task_id):
        if task_id not in self.running_tasks:
            return

        self.running_tasks[task_id]["seconds"] += 1
        seconds = self.running_tasks[task_id]["seconds"]
        hh = seconds // 3600
        mm = (seconds % 3600) // 60
        ss = seconds % 60

        self.timer_labels[task_id].setText(f"{hh:02}:{mm:02}:{ss:02}")
    
    def calculate_total_tracked_time(self, time_logs):
        total_seconds = self.calculate_tracked_seconds(time_logs)
        hh, mm, ss = total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60
        return f"{hh:02}:{mm:02}:{ss:02}" if total_seconds > 0 else "00:00:00"

    def calculate_tracked_seconds(self, time_logs):
        total_time = timedelta()
        for log in time_logs:
            if log.start_time and log.end_time:
                try:
                    start = datetime.strptime(log.start_time, "%Y-%m-%d %H:%M:%S")
                    end = datetime.strptime(log.end_time, "%Y-%m-%d %H:%M:%S")
                    total_time += (end - start)
                except ValueError as e:
                    print(f"❌ Error parsing timestamps: {e}")
            elif log.start_time:
                end_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                start = datetime.strptime(log.start_time, "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                total_time += (end - start)
        return int(total_time.total_seconds())

    def handle_inactivity(self):
        if self.running_tasks:
            active_task = list(self.running_tasks.keys())[0]
            self.toggle_timer(active_task)