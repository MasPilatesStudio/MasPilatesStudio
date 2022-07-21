from src.controllers import ctrl_shop

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

def add_to_shopping_cart(email, productId):
  response = ctrl_shop.add_to_shopping_cart(email, productId)
  return response
