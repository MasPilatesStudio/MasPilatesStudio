from src.utils import constants
import psycopg2
import psycopg2.extras
import db

def get_schedule():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM classes')
        response = cur.fetchall()

        if cur.rowcount > 0:
            column_names = [desc[0] for desc in cur.description]
            response = db.serialize_array(column_names, response)
        else:
            response = 'No hay registros'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def book_class(name, start_date, end_date, user_email):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor()
        query = 'INSERT INTO books (name_class, start_date, end_date, user_email) VALUES (%s, %s, %s, %s, %s)'
        data = (name, start_date, end_date, user_email)
        cur.execute(query, data)
        conexion.commit()

        if cur.rowcount > 0:
            result = 'OK'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

