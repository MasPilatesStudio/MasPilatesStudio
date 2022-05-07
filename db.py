from traceback import print_tb
import psycopg2
from config import config

def get_engine():
    conexion = None
    try:
        # Lectura de los parámetros de conexion
        params = config()

        # Conexion al servidor de PostgreSQL
        print('Conectando a la base de datos PostgreSQL...')
        conexion = psycopg2.connect(**params)
        return conexion
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def serialize(column_names, res):
    d = {}
    for index in range(0,len(column_names)):
        d[column_names[index]] = res[index]
    return d

def serialize_array(column_names, response):
    aux = []
    for result in response:
        response = serialize(column_names, result)
        aux.append(response)
    return aux
