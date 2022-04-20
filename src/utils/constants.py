from enum import Enum, unique

HTTP_STATUS_500 = 500
HTTP_STATUS_400 = 400

SI = 'S'
@unique
class ROL(Enum):
  EMPLOYEE = 'Employee'
  CLIENT = 'Client'
  ADMINISTRATOR = 'Administrator'