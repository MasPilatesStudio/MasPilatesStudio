from flask import session
from src.controllers import ctrl_calendar

def get_schedule():
  response = ctrl_calendar.get_schedule()
  return response

def book_class(book, email):
  response = ctrl_calendar.book_class(book['name'], book['start'],book['end'], email)
  return response

def get_bookings(email):
  response = ctrl_calendar.get_bookings(email)
  return response