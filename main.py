import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from logic.auth import is_logged_in
from config_setup import run_config
from utils.utils import resource_path

user_home=os.path.expanduser("~")
log_dir=os.path.join(user_home,"TaskTrackerData")
log_file_path=os.path.join(log_dir,"error_log.txt")
os.makedirs(log_dir,exist_ok=True)

try:
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/logo.png")))
    run_config()

    if is_logged_in():
        from ui.task_tracker import TaskTrackerWindow
        window = TaskTrackerWindow()
    else:
        from ui.login import LoginWindow
        window = LoginWindow()

    window.setWindowIcon(QIcon(resource_path("assets/logo.png")))
    window.show()
    
    sys.exit(app.exec())

except Exception as e:
    with open(log_file_path, "w") as f:
        traceback.print_exc(file=f)