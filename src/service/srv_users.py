from src.model.User import User
from werkzeug.security import check_password_hash
from src.controllers import ctrl_users
from flask import session, g

def get_users():
    response = ctrl_users.get_users()
    return response


def get_user(email):
    response = ctrl_users.get_user(email)
    user = User(response['email'], response['name'], response['password'])
    return user

def get_user_data(email):
    response = ctrl_users.get_user(email)
    del response['password']
    return response


def register_user(user):
    # Ver si el usuario ya existe
    exist = ctrl_users.check_exists(user['email'])
    if exist == True:
        return "El usuario ya existe"
    if exist == False:
        return ctrl_users.add_user(user['email'], user['name'], user['password'])

def update_send_direction(user):
    return ctrl_users.update_send_direction(user)


def login(user):
    response = ctrl_users.get_user(user['email'])
    if response != 'Usuario no encontrado' and response != None:
        if check_password_hash(response['password'], user['password']):
            session['email'] = user['email']
            session['rol'] = response['rol']
            token = User.generate_auth_token(response['email'])
            user = {
                'email': user['email'],
                'rol': response['rol'],
                'token': token
            }
            return user
        else:
            return 'Incorrect password'
    else:
        return 'Invalid credentials'