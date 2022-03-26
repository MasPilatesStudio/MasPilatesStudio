from flask import Flask
from config import config

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config[config_name])

    # Configuracion de los BluePrints
    from .bp_users import users_bp as user_end_point
    app.register_blueprint(user_end_point)

    return app
