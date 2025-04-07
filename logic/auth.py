from database.models import perform_db_action
import bcrypt

def login(username, password):
    user = perform_db_action("users", "get_user", username=username)
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        user_id=user.id
        session_data={
            "user_id":user.id,
            "username":user.username
        }
        perform_db_action("sessions", "set_session", user_id=user_id,session_data=session_data)
        return True
    return False

def register(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return perform_db_action("users", "create_user", username=username, password=hashed_password)

def is_logged_in():
    return perform_db_action("sessions", "check_session")

def logout(user_id):
    return perform_db_action("sessions", "clear_session",user_id=user_id)

def logged_in_user():
    return perform_db_action("sessions", "get_logged_in_user")

def get_user(user_id):
    return perform_db_action("users", "get_user",id=user_id)

def get_all_sub_users():
    return perform_db_action("users", "get_sub_users")

def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return perform_db_action("users", "create_user", username=username, password=hashed_password,role='sub')