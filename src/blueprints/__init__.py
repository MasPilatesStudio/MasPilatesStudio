from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    # Configuracion de los BluePrints
    from .bp_users import users_bp as user_end_point
    app.register_blueprint(user_end_point)

    return app
