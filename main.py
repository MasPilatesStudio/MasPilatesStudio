# from flask import Flask
# from flask import Blueprint, jsonify
from flask_cors import CORS
from src.blueprints import create_app
# import src
# from src.blueprints import bp_users as user_endpoint

# app = Flask(src.__name__, instance_relative_config=False)
# app = create_app('default')
app = create_app()

CORS(app, resources={r'/*': {'origins': '*'}})
# app.run()
# @app.route('/', methods=['GET'])
# def main():
#     print('Hello, World!')
#     return jsonify({'message':'Hello'})

# with app.app_context():
#     from src.blueprints import bp_users
#     app.register_blueprint(user_endpoint.users_bp)

# if __name__=="__main__":
