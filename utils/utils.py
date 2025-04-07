from PyQt6.QtWidgets import QMessageBox
import os
import sys

def show_error(errorMessage):
    msg=QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(errorMessage)
    msg.setWindowTitle("Error")
    msg.exec()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.expanduser("~")
        db_folder = os.path.join(base_path, "TaskTrackerData")
    else:
        db_folder = os.path.abspath("database")

    os.makedirs(db_folder, exist_ok=True)
    return os.path.join(db_folder, "task_tracker.db")