from database.models import perform_db_action
from datetime import datetime

def get_all_projects():
    return perform_db_action("projects", "get_projects")

def get_user_projects(user_id):
    return perform_db_action("projects", "get_projects",client_id=user_id)

def add_project(name, client_id):
    return perform_db_action("projects", "create_project", name=name, client_id=client_id)

def add_task(description, assigned_user_id,project_id):
    return perform_db_action("tasks", "create_task", description=description, assigned_user_id=assigned_user_id,project_id=project_id)

def get_all_tasks():
    return perform_db_action("tasks", "get_tasks")

def get_user_tasks(user_id):
    return perform_db_action("tasks", "get_tasks",assigned_user_id=user_id)

def get_project(project_id):
    return perform_db_action("projects", "get_project",id=project_id)

def get_task(task_id):
    return perform_db_action("tasks", "get_task",id=task_id)

def add_time_log(user_id,task_id):
    start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return perform_db_action("time_logs", "create_time_logs",user_id=user_id,task_id=task_id,start_time=start_time)

def update_time_log(user_id,task_id):
    end_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return perform_db_action("time_logs", "update_time_logs",user_id=user_id,task_id=task_id,end_time=end_time)

def get_user_task_time_logs(user_id,task_id):
    return perform_db_action("time_logs", "get_time_logs",user_id=user_id,task_id=task_id)

def get_user_task_ordered_time_logs(user_id):
    return perform_db_action("time_logs", "get_ordered_time_logs",user_id=user_id)

def get_all_task_ordered_time_logs():
    return perform_db_action("time_logs", "get_ordered_time_logs")

def get_time_log_distinct_tasks():
    return perform_db_action("time_logs", "get_distinct_tasks")

def check_timer_active(user_id,task_id):
    return perform_db_action("time_logs","is_timer_active",user_id=user_id,task_id=task_id)

def check_any_timer_active(user_id):
    return perform_db_action("time_logs","is_any_timer_active",user_id=user_id)