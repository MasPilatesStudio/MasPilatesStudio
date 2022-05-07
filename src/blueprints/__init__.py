from flask import Flask
from flask_cors import CORS
from .bp_users import users_bp as user_end_point
from .bp_calendar import calendar_bp as calendar_end_point

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})

    app.config['SECRET_KEY'] = 'secret'

    # Configuracion de los BluePrints
    from .bp_users import users_bp as user_end_point
    app.register_blueprint(user_end_point)
    from .bp_calendar import calendar_bp as calendar_end_point
    app.register_blueprint(calendar_end_point)

    return app
