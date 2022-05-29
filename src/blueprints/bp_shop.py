from flask import Blueprint, jsonify, request
from src.utils.response_utils import make_error
from src.utils import constants
from src.service import srv_shop

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

@shop_bp.route('get_products', methods=['POST'])
def get_products():
    try:
        print('🚀 get_products - bp_shop' )
        filters = request.json.get('filters')
        response = srv_shop.get_products(filters)
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_categories', methods=['GET'])
def get_categories():
    try:
        print('🚀 get_categories - bp_shop' )
        response = srv_shop.get_categories()
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_brands', methods=['GET'])
def get_brands():
    try:
        print('🚀 get_brands - bp_shop' )
        response = srv_shop.get_brands()
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)
