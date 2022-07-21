import psycopg2
import psycopg2.extras
import db

def get_products(filters, current_page, per_page):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT * FROM articles WHERE xti_activo = 'S' '''
        if filters['category'] != '':
            query += ' AND category = \'' + filters['category'] + '\''
        if filters['search'] != '':
            query += ''' AND lower(name) LIKE '%''' + filters['search'].lower() + '''%' '''
        if len(filters['brands']) > 0:
            string_brands = "', '".join([str(elem) for elem in filters['brands']])
            query += " AND (brand is null or brand in ('" + string_brands + "'))"
        if filters['order'] == 'asc':
            query += ' ORDER BY price::DECIMAL asc'
        if filters['order'] == 'desc':
            query += ' ORDER BY price::DECIMAL desc'
        elif filters['order'] == None:
            query += ' ORDER BY id desc'
        query += ' LIMIT ' + str(per_page) + ' OFFSET ' + str(((current_page -1) * per_page) )
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

def get_count_products():
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT COUNT(*) FROM articles WHERE xti_activo = 'S' '''
        cur.execute(query)
        response = cur.fetchall()

        aux = []
        if cur.rowcount > 0:
            response = response[0][0]
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
            aux = 'No hay registros'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return aux
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def add_to_shopping_cart (email, productId):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' INSERT INTO "shoppingCart" ("email", "id_article", "quantity")
                    VALUES (%s, '%s', '1')
                    ON CONFLICT (email, id_article)
                    DO UPDATE SET quantity = (select quantity FROM "shoppingCart"
                    WHERE email = %s AND id_article = '%s') + 1 '''
        data = (email, productId, email, productId,)
        cur.execute(query, data)
        conexion.commit()
        if cur.rowcount > 0:
            response = 'OK'
        else:
            response = 'ERROR'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')


def get_shopping_cart(email):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """ SELECT c.quantity, a.* FROM "shoppingCart" c
                    INNER JOIN articles a ON c.id_article = a.id
                    WHERE email = %s
                    ORDER BY c.id_article ASC """
        data = (email,)
        cur.execute(query, data)
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
