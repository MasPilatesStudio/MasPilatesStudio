from src.utils import constants
import psycopg2
import psycopg2.extras
import db
from src.model import User

def get_users():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor()
        cur.execute('SELECT * FROM users')
        response = cur.fetchall()
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def add_user(email, name, password):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor()
        query = 'INSERT INTO users (email, name, password, rol, xti_activo) VALUES (%s, %s, %s, %s, %s)'
        data = (email, name, User.generate_password_hash(password), constants.ROL.CLIENT.value, constants.SI,)
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


def update_send_direction(user):
    try:
        update_query = ''
        if user['name']:
            update_query = ', name = \'' + user['name'] + '\''
        conexion = db.get_engine()
        cur = conexion.cursor()
        query = 'UPDATE users SET province = %s, direction = %s, cp = %s, phone = %s ' + update_query + ' WHERE email = %s'
        print(query)
        data = (user['province'], user['direction'], user['cp'], user['phone'], user['email'],)
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


def check_exists(email):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor()
        query = 'SELECT FROM users WHERE email = %s'
        data = (email,)
        cur.execute(query, data)
        result = cur.fetchone()

        if cur.rowcount > 0:
            result = True
        else:
            result = False
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')


def get_user(email):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = 'SELECT * FROM users WHERE email = %s'
        data = (email,)
        cur.execute(query, data)
        result = cur.fetchone()

        if cur.rowcount > 0:
            column_names = [desc[0] for desc in cur.description]
            response = db.serialize(column_names, result)
        else:
            response = 'Usuario no encontrado'
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')