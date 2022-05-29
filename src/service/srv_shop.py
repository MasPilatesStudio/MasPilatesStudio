from src.controllers import ctrl_shop

def get_products(filters):
  response = ctrl_shop.get_products(filters)
  return response

def get_categories():
  response = ctrl_shop.get_categories()
  return response

def get_brands():
  response = ctrl_shop.get_brands()
  return response
