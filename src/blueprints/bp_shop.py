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
        response = srv_shop.get_products(filters, current_page, per_page)
        return jsonify({ 'Items': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_count_products', methods=['GET'])
def get_count_products():
    try:
        print('🚀 get_count_products - bp_shop' )
        response = srv_shop.get_count_products()
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

@shop_bp.route('get_count_shopping_cart/<email>', methods=['GET'])
def get_count_shopping_cart(email):
    try:
        print('🚀 get_count_shopping_cart - bp_shop' )
        response = srv_shop.get_count_shopping_cart(email)
        return jsonify({ 'quantity': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

@shop_bp.route('get_order_by_user/<email>', methods=['GET'])
def get_order_by_user(email):
    try:
        print('🚀 get_brands - bp_shop' )
        response = srv_shop.get_order_by_user(email)
        return jsonify({ 'orders': response })
    except BaseException as e:
        return make_error(constants.HTTP_STATUS_500, message=e)

# @shop_bp.route('/config', methods=['GET'])
# def get_publishable_key():
#     stripe.api_key = stripe_keys['secret_key']

#     stripe_keys = {
#         'secret_key': os.environ['STRIPE_SECRET_KEY'],
#         'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY'],
#     }
#     stripe_config = {'publicKey': stripe_keys['publishable_key']}
#     return jsonify(stripe_config)

@shop_bp.route('/add_order', methods=['POST'])
def create_checkout_session():
    try:
        # checkout_session = stripe.checkout.Session.create(
        #     line_items=[
        #         {
        #             # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
        #             'price': 'price_1LOhZ9Jgo7zTVCqcRr6yuKCf',
        #             'quantity': 1,
        #         },
        #     ],
        #     mode='payment',
        #     success_url='success',
        #     cancel_url='cancel',
        # )
        # Create a PaymentIntent with the order amount and currency
        email = request.json.get('email')
        products = request.json.get('products')
        response = srv_shop.add_order(email, products)
        return jsonify({ 'message': response })
    except Exception as e:
        return str(e)

