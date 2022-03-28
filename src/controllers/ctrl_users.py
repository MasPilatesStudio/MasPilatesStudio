import psycopg2
import db

def get_users():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor()
        cur.execute('SELECT name FROM users')
        response = cur.fetchall()
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return response[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')