from src.controllers import ctrl_shop
import stripe

stripe.api_key = 'sk_test_51L8UuqJgo7zTVCqcDcPNe68hbsuHs3d8gSsF2EbaeX0nms5O32lZA9pV73MJV2OOCueBL5tHKSoTtkiMnS3TAnFZ00n4X1M7Jx'

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
    amount = 0
    for product in products:
        amount += float(product['price'])
    intent = None
    if response == 'OK':
        try:
            intent = stripe.checkout.Session.create(
                success_url='https://maspilatesstudio-front.herokuapp.com/#//#/shop',
                cancel_url='https://maspilatesstudio-front.herokuapp.com/#/shoppingCart',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                {
                    'name': 'Compra',
                    'quantity': 1,
                    'currency': 'eur',
                    'amount': round(float(amount) * 100)
                }]
            )
            print(intent)
            return intent['url']
        except Exception as e:
            return str(e)

def add_product(product):
    response = stripe.Product.create(
        name=product['name'],
        description=product['description'],
        default_price_data={"unit_amount": product['price'] * 100, "currency": "eur"},
    )
    print(response)
    response = ctrl_shop.add_product(product, response['default_price'])
    return response

def _calculate_order_amount(products):
    total = 0
    for product in products:
        total += product['price'] * product['quantity']
    return total
