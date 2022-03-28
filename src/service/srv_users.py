from src.controllers import ctrl_users

def get_users():
    response = ctrl_users.get_users()
    return response