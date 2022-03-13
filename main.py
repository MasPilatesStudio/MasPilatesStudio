from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    print('Hello, World!')
    return jsonify({'message':'Hello'})

if __name__=="__main__":
    app.run(debug==True)