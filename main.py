from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def main():
    print('Hello, World!')
    return jsonify({'message':'Hello'})

# if __name__=="__main__":
#     app.run()