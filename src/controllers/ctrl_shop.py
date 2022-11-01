import psycopg2
import psycopg2.extras
import db

def get_products(filters, current_page, per_page, user_rol):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT * FROM articles WHERE (xti_activo = 'S' '''
        if user_rol is not None and user_rol != 'Client':
            query += ''' OR xti_activo = 'N' )'''
        else:
            query += ')'
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

def get_count_products(filters, user_rol):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''SELECT COUNT(*) FROM articles WHERE (xti_activo = 'S' '''
        if user_rol is not None and user_rol['rol'] != 'Client':
             query += ''' OR xti_activo = 'N') '''
        else:
            query += ')'
        if filters['category'] != '':
            query += ' AND category = \'' + filters['category'] + '\''
        if filters['search'] != '':
            query += ''' AND lower(name) LIKE '%''' + filters['search'].lower() + '''%' '''
        if len(filters['brands']) > 0:
            string_brands = "', '".join([str(elem) for elem in filters['brands']])
            query += " AND (brand is null or brand in ('" + string_brands + "'))"
        print(query)
        cur.execute(query)
        response = cur.fetchall()

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


def delete_product (email, product):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if product['quantity'] > 0:
            query = ''' UPDATE "shoppingCart" SET quantity = %s
                        WHERE id_article = %s AND email = %s '''
            data = (product['quantity'], product['id'], email,)
            cur.execute(query, data)
        else:
            query = ''' DELETE FROM "shoppingCart"
                        WHERE id_article = %s AND email = %s '''
            data = (product['id'], email,)
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


def get_count_shopping_cart(email):
    try:
        print(email)
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """ SELECT SUM(c.quantity ) AS cantidad_total
                    FROM "shoppingCart" c
                    INNER JOIN users u ON c.email = u.email
                    WHERE c.email = %s
                    GROUP BY c.email """
        data = (email,)
        cur.execute(query, data)
        response = cur.fetchall()
        print(response)
        if cur.rowcount > 0:
            response = response[0][0]
        else:
            response = '0'
        # Cierre de la comunicación con PostgreSQL
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')


def add_order (email, products):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' INSERT INTO "order" ("id_user", "date", "state")
                    VALUES (%s, current_timestamp, 'ESPERA') RETURNING id'''
        data = (email,)
        cur.execute(query, data)
        id_order = cur.fetchone()[0]
        print(id_order)
        print('Insert orderLine')

        query = ''' INSERT INTO "orderLine" (id_order, id_article, amount, quantity, line)
                    VALUES (%s, %s, %s, %s, %s)'''
        for i in range(len(products)):
            data = (id_order, products[i]['id'], products[i]['price'], products[i]['quantity'], i,)
            cur.execute(query, data)
            print('Inserted orderLine')

        query = ''' DELETE FROM "shoppingCart" WHERE email = %s '''
        data = (email,)
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


def get_orders(user):
    try:
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' SELECT p.id,
                        string_agg(concat(lp.quantity::VARCHAR(4), ' ', a.name), ', ') AS articles,
                        SUM(lp.amount::float * lp.quantity) AS total_price,
                        p.id_user,
                        u.direction,
                        to_char(p.date, 'DD/MM/YYYY') AS date,
                        p.state
                    FROM "order" p
                    INNER JOIN "orderLine" lp ON p.id = lp.id_order
                    INNER JOIN articles a ON lp.id_article = a.id
                    INNER JOIN users u ON p.id_user = u.email
                '''
        if user['rol'] != 'Administrator' and user['rol'] != 'Employee':
            query += ' WHERE u.email = %s'
        query += 'GROUP BY p.id, u.email ORDER BY p.date desc'
        data = (user['email'],)
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

def add_product(product):
    try:
        print('ctrl_shop - add_product - start')
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' INSERT INTO "articles" ("name", "description", "price", "xti_activo", "category", "brand")
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id '''
        data = (product['name'], product['description'], product['price'], 'S', product['category'], product['brand'],)
        cur.execute(query, data)
        id_product = cur.fetchone()[0]

        query = ''' UPDATE "articles" SET image = %s WHERE id = %s'''
        data = (str(id_product) + '.png', id_product,)
        cur.execute(query, data)
        conexion.commit()
        return id_product
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def disabled_product(xti_activo, product_id):
    try:
        print('ctrl_shop - change_order_state - start')
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' UPDATE "articles" SET xti_activo = %s WHERE id = %s RETURNING id '''
        data = (xti_activo, product_id,)
        cur.execute(query, data)
        id_product = cur.fetchone()[0]
        conexion.commit()
        return id_product
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def change_order_state(order_id, state):
    try:
        print('ctrl_shop - change_order_state - start')
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' UPDATE "order" SET state = %s WHERE id = %s RETURNING id '''
        data = (state, order_id,)
        cur.execute(query, data)
        id_order = cur.fetchone()[0]
        conexion.commit()
        return id_order
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')


def pay_monthly_fee(email):
    try:
        print('ctrl_shop - pay_monthly_fee - start')
        conexion = db.get_engine()
        cur = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ''' UPDATE users SET pay_date = current_date WHERE email = %s '''
        data = (email,)
        cur.execute(query, data)
        conexion.commit()
        return 'OK'
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')