from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget,QMessageBox
from PyQt6.QtGui import QIcon, QAction
from logic.auth import logout, logged_in_user, get_user
from utils.utils import resource_path
from logic.tracker import check_any_timer_active
from utils.activity_tracker import ActivityTracker

class TaskTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logged_in_user_id = logged_in_user().user_id
        self.user_role = get_user(self.logged_in_user_id).role

        self.setWindowTitle("Task Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(resource_path("assets/logo.png")))

        self.menu_bar = self.menuBar()
        self.setup_menu()

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.current_view = None
        self.show_projects()

        if check_any_timer_active(self.logged_in_user_id):
            self.instantiate_activity_tracker()
        

    def instantiate_activity_tracker(self):
        self.activity_tracker=ActivityTracker(timeout=300,callback=self.handle_inactivity)
        self.activity_tracker.start_tracking()

    def stop_current_thracker(self):
        self.activity_tracker.stop_tracking()

    def handle_inactivity(self):
        from ui.task_list import TaskList
        if self.current_view and isinstance(self.current_view,TaskList):
            self.current_view.handle_inactivity()
        else:
            TaskList(self,self.user_role,self.logged_in_user_id).handle_inactivity()
        QTimer.singleShot(0,self.show_inactivity_message)

    def show_inactivity_message(self):
        self.setWindowState(Qt.WindowState.WindowActive)
        self.activateWindow()
        self.raise_()
        msg_box=QMessageBox()
        msg_box.setWindowTitle("Inactivity Alert")
        msg_box.setText("Task timer paused due to 5 minutes of inactivity")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def setup_menu(self):
        projects_menu = self.menu_bar.addMenu("Projects")
        projects_menu.addAction(self.create_action("View Projects", self.show_projects))
        if self.user_role == "super":
            projects_menu.addAction(self.create_action("Add Project", self.open_add_project))

        tasks_menu = self.menu_bar.addMenu("Tasks")
        tasks_menu.addAction(self.create_action("View Tasks", self.show_tasks))
        if self.user_role == "super":
            tasks_menu.addAction(self.create_action("Add Task", self.open_add_task))

        time_logs_menu = self.menu_bar.addMenu("Time Logs")
        time_logs_menu.addAction(self.create_action("View Time Logs", self.show_time_logs))

        if self.user_role == "super":
            users_menu = self.menu_bar.addMenu("Users")
            users_menu.addAction(self.create_action("Manage Users", self.open_user_management))
            users_menu.addAction(self.create_action("Add Users", self.open_add_user))

        settings_menu = self.menu_bar.addMenu("Settings")
        settings_menu.addAction(self.create_action("Log Out", self.log_out))
        settings_menu.addAction(self.create_action("Quit and Log Out", self.log_out_quit))

    def create_action(self, name, function):
        action = QAction(name, self)
        action.triggered.connect(function)
        return action

    def switch_view(self, new_view):
        if self.current_view:
            self.layout.removeWidget(self.current_view)
            self.current_view.deleteLater()

        self.current_view = new_view
        self.layout.addWidget(self.current_view)

    def show_projects(self):
        from ui.project_list import ProjectList
        self.switch_view(ProjectList(self.user_role,self.logged_in_user_id))

    def show_tasks(self):
        from ui.task_list import TaskList
        self.switch_view(TaskList(self,self.user_role,self.logged_in_user_id))

    def show_time_logs(self):
        from ui.time_log_history import TimeLogHistory
        self.switch_view(TimeLogHistory(self.user_role,self.logged_in_user_id))

    def open_user_management(self):
        from ui.user_list import UserList
        self.switch_view(UserList())

    def open_add_project(self):
        from ui.add_projects import AddProjectsWindow
        self.add_project_window = AddProjectsWindow(self)
        self.add_project_window.show()

    def open_add_task(self):
        from ui.add_tasks import AddTasksWindow
        self.add_task_window = AddTasksWindow(self)
        self.add_task_window.show()

    def open_add_user(self):
        from ui.add_users import AddUsersWindow
        self.add_user_window = AddUsersWindow(self)
        self.add_user_window.show()

    def log_out(self):
        logout(self.logged_in_user_id)
        from ui.login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def log_out_quit(self):
        logout(self.logged_in_user_id)
        self.close()