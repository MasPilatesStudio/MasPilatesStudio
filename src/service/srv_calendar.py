from flask import session
from src.controllers import ctrl_calendar

def get_schedule():
  response = ctrl_calendar.get_schedule()
  return response

def book_class(data, email):
  print('email: ' + email)
  response = ctrl_calendar.book_class(data['name'], data['start'],data['end'], email)
  return response
