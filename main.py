from flask_cors import CORS
from src.blueprints import create_app

app = create_app()

CORS(app, resources={r'/*': {'origins': '*'}})
# app.run()
