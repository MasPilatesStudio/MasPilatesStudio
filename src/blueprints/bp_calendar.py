from flask import Blueprint, jsonify, request, g
from src.utils.response_utils import make_error
from src.utils import constants
from src.service import srv_calendar
from src.decorators import decorators

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('schedule', methods=['GET'])
def get_schedule():
    try:
        print('🚀 get_schedule - bp_calendar' )
        response = srv_calendar.get_schedule()
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@calendar_bp.route('book_class', methods=['POST'])
def book_class():
    try:
        print('🚀 book_class - bp_calendar' )
        book = request.json.get('book')
        print(book)
        email = request.json.get('email')
        response = srv_calendar.book_class(book, email)
        print(response)
        return jsonify({ 'response': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@calendar_bp.route('get_bookings/<email>', methods=['GET'])
def get_bookings(email):
    try:
        print('🚀 get_bookings - bp_calendar' )
        print(email)
        response = srv_calendar.get_bookings(email)
        print(response)
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)