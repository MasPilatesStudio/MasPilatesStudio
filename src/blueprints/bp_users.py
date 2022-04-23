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


@users_bp.route('login', methods=['GET'])
def login():
    try:
        user = request.json.get('user')
        token = srv_users.login(user)
        return jsonify( {'response': token} )
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
    email = session['email']
    return str(email)

def get_user_rol():
    rol = session['rol']
    return str(rol)

# @users_bp.route("/")
# @auth.login_required
# def index():
#     return jsonify({ 'user': g.user.username })

# @users_bp.route('users', methods=['GET'])
# def get_users():
#     try:
#         print('Hello, World!')
#         response = srv_users.get_users()

#         return jsonify({ 'message': response })
#     except BaseException as e:
#         return make_error(constants.HTTP_STATUS_500, message=e)


# @users_bp.route('/api/login')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify(token)

# @auth.verify_password
# def verify_password(username_or_token, password):
#     if request.path == "/api/login":
#         response = srv_users.get_user(username_or_token)
#         if not response or not response.verify_password(password):
#             return False
#     else:
#         user = User.User.verify_auth_token(username_or_token)
#         if not user:
#             return False
#     g.user = user
#     return True
