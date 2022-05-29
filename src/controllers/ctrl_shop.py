import psycopg2
import psycopg2.extras
import db

def get_products(filters):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT * FROM articles WHERE xti_activo = 'S' '''
        if filters['category'] != '':
            query += ' AND category = \'' + filters['category'] + '\''
        if filters['search'] != '':
            query += ''' AND lower(name) LIKE '%''' + filters['search'].lower() + '''%' '''
        if filters['order'] == 'asc':
            query += ' ORDER BY price asc'
        if filters['order'] == 'desc':
            query += ' ORDER BY price desc'
        elif filters['order'] == None:
            query+= ' ORDER BY id desc'
        print(query)
        cur.execute(query)
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

def get_categories():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT category FROM categories WHERE xti_activo = 'S' '''
        cur.execute(query)
        response = cur.fetchall()

        aux = []
        if cur.rowcount > 0:
            column_names = [desc[0] for desc in cur.description]
            response = db.serialize_array(column_names, response)
            for res in response:
                aux.append(res['category'])
        else:
            response = 'No hay registros'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return aux
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def get_brands():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = 'SELECT distinct brand FROM articles'
        cur.execute(query)
        response = cur.fetchall()

        aux = []
        if cur.rowcount > 0:
            column_names = [desc[0] for desc in cur.description]
            response = db.serialize_array(column_names, response)
            for res in response:
                aux.append(res['brand'])
        else:
            response = 'No hay registros'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return aux
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')
