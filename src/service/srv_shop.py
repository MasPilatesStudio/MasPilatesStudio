from src.controllers import ctrl_shop
import stripe

def get_products(filters, current_page, per_page):
    response = ctrl_shop.get_products(filters, current_page, per_page)
    return response

def get_count_products():
    response = ctrl_shop.get_count_products()
    return response

def get_categories():
    response = ctrl_shop.get_categories()
    return response

def get_brands():
    response = ctrl_shop.get_brands()
    return response

def get_shopping_cart(email):
    response = ctrl_shop.get_shopping_cart(email)
    return response

def get_count_shopping_cart(email):
    response = ctrl_shop.get_count_shopping_cart(email)
    return response

def add_to_shopping_cart(email, productId):
    response = ctrl_shop.add_to_shopping_cart(email, productId)
    return response

def get_order_by_user(email):
    response = ctrl_shop.get_order_by_user(email)
    return response

def add_order(email, products):
    response = ctrl_shop.add_order(email, products)
    intent = None
    if response == 'OK':
        intent = stripe.PaymentIntent.create(
            amount=_calculate_order_amount(products),
            currency='eur',
            automatic_payment_methods={
                'enabled': True,
            },
            success_url='success',
            cancel_url='cancel',
        )
        print(intent.url)
    return intent.url

def _calculate_order_amount(products):
    total = 0
    for product in products:
        total += product['price'] * product['quantity']
    return total
