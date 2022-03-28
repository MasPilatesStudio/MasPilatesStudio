from flask import Blueprint, jsonify
from flask import current_app as app
from src.utils.response_utils import make_error
from src.utils import constants
from src.service import srv_users

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('users', methods=['GET'])
def get_users():
    try:
        print('Hello, World!')
        response = srv_users.get_users()
        return jsonify({ 'message': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)
