import os
from configparser import ConfigParser

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

class Development(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave'
class Testing(Config):
    TESTING = True

class Production(Config):
    pass

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,

    'default': Development
}

def config(archivo='base_de_datos.ini', seccion='postgresql'):
    # Parsear el archivo
    parser = ConfigParser()
    parser.read(archivo)
 
    # Ir a la sección de postgresql y extraer los parámetros
    db = {}
    if parser.has_section(seccion):
        params = parser.items(seccion)
        for param in params:
            db[param[0]] = param[1]
        return db
    else:
        raise Exception('Secccion {0} no encontrada en el archivo {1}'.format(seccion, archivo))