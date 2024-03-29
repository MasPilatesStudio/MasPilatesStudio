from flask import Blueprint, jsonify, request
from src.utils.response_utils import make_error
from src.utils import constants
from src.service import srv_shop
import os

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

@shop_bp.route('get_products', methods=['POST'])
def get_products():
    try:
        print('🚀 get_products - bp_shop' )
        filters = request.json.get('filters')
        current_page = request.json.get('currentPage')
        per_page = request.json.get('perPage')
        user_rol = request.json.get('userLogued')
        response = srv_shop.get_products(filters, current_page, per_page, user_rol)
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_count_products', methods=['POST'])
def get_count_products():
    try:
        print('🚀 get_count_products - bp_shop' )
        filters = request.json.get('filters')
        user_rol = request.json.get('userLogued')
        response = srv_shop.get_count_products(filters, user_rol)
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

@shop_bp.route('get_shopping_cart/<email>', methods=['GET'])
def get_shopping_cart(email):
    try:
        print('🚀 get_brands - bp_shop' )
        response = srv_shop.get_shopping_cart(email)
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('add_to_shopping_cart', methods=['POST'])
def add_to_shopping_cart():
    try:
        print('🚀 get_brands - bp_shop' )
        productId = request.json.get('productId')
        email = request.json.get('email')
        response = srv_shop.add_to_shopping_cart(email, productId)
        return jsonify({ 'message': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('delete_product', methods=['PUT'])
def delete_product():
    try:
        print('🚀 delete_product - bp_shop' )
        productId = request.json.get('product')
        email = request.json.get('email')
        response = srv_shop.delete_product(email, productId)
        return jsonify({ 'message': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_count_shopping_cart/<email>', methods=['GET'])
def get_count_shopping_cart(email):
    try:
        print('🚀 get_count_shopping_cart - bp_shop' )
        response = srv_shop.get_count_shopping_cart(email)
        return jsonify({ 'quantity': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_orders', methods=['POST'])
def get_orders():
    try:
        print('🚀 get_brands - bp_shop' )
        user = request.json.get('user')
        response = srv_shop.get_orders(user)
        return jsonify({ 'orders': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('/add_order', methods=['POST'])
def create_checkout_session():
    try:
        # Create a PaymentIntent with the order amount and currency
        email = request.json.get('email')
        products = request.json.get('products')
        response = srv_shop.add_order(email, products)
        return jsonify({ 'sessionId': response })
    except Exception as e:
        return str(e)

@shop_bp.route('/add_product', methods=['POST'])
def add_product():
    try:
        product = request.json.get('product')
        response = srv_shop.add_product(product)
        return jsonify({ 'message': response })
    except Exception as e:
        return str(e)

@shop_bp.route('/disabled_product', methods=['POST'])
def disabled_product():
    try:
        product_id = request.json.get('product_id')
        xti_activo = request.json.get('xti_activo')
        response = srv_shop.disabled_product(xti_activo, product_id)
        return jsonify({ 'product': response })
    except Exception as e:
        return str(e)

@shop_bp.route('/change_order_state', methods=['POST'])
def change_order_state():
    try:
        order_id = request.json.get('order_id')
        state = request.json.get('state')
        response = srv_shop.change_order_state(order_id, state)
        return jsonify({ 'message': response })
    except Exception as e:
        return str(e)

@shop_bp.route('/pay_monthly_fee', methods=['POST'])
def pay_monthly_fee():
    try:
        # Create a PaymentIntent with the order amount and currency
        email = request.json.get('email')
        response = srv_shop.pay_monthly_fee(email)
        return jsonify({ 'response': response })
    except Exception as e:
        return str(e)