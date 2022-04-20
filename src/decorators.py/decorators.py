from functools import wraps
from flask import g, make_response, jsonify
from src.blueprints import bp_users

def check_user(valids_rols):
    def decorator(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            email = bp_users.get_user_email()
            rol = bp_users.get_user_rol()
            if rol in valids_rols:
                g.email = email
                g.rol = rol
                return funcion(*args, **kwargs)
            else:
                return make_response(jsonify({'data': 'Access denied'}))
        return wrapper
    return decorator