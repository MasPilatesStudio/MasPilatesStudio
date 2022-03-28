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