from flask import Blueprint, jsonify, request, session
from src.utils.response_utils import make_error
from src.utils import constants
from src.service import srv_users

users_bp = Blueprint('users', __name__, url_prefix='/users')
# users_bp.before_request(Before)

@users_bp.route('register', methods=['POST'])
def register_user():
    try:
        print('🚀 register_user - bp_users' )
        user = request.json.get('user')
        response = srv_users.register_user(user)
        return jsonify({ 'message': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@users_bp.route('add_employee', methods=['POST'])
def add_employee():
    try:
        print('🚀 add_employee - bp_users' )
        employee = request.json.get('employee')
        response = srv_users.add_employee(employee)
        return jsonify({ 'message': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)


@users_bp.route('update_send_direction', methods=['POST'])
def update_send_direction():
    try:
        print('🚀 register_user - bp_users' )
        user = request.json.get('user')
        response = srv_users.update_send_direction(user)
        return jsonify({ 'response': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)


@users_bp.route('get_user/<email>', methods=['GET'])
def get_user(email):
    try:
        print('🚀 register_user - bp_users' )
        response = srv_users.get_user_data(email)
        return jsonify({ 'response': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)


@users_bp.route('login', methods=['POST'])
def login():
    try:
        user = request.json.get('user')
        response = srv_users.login(user)
        return jsonify( {'response': response} )
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)


@users_bp.route('logout', methods=['GET'])
def logout():
    try:
        session.pop('email', None)
        session.pop('rol', None)
        return jsonify( {'response': 'OK'} )
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)


def get_user_email():
    print('get_user_email' + session['email'])
    email = session['email']
    return str(email)

def get_user_rol():
    rol = session['rol']
    return str(rol)
