from flask import Flask, jsonify
from flask_cors import CORS
import connexion

#app = Flask(__name__)
app = connexion.App(__name__, specification_dir='./')
#app.add_api('swagger.yml')

CORS(app.app)

@app.route('/', methods=['GET'])
def hello_world():
    resp = {
        "data": [
            "hej",
            "wops"
        ]
    }
    return jsonify(resp)

@app.route('/users', methods=['GET'])
def load_users():
    resp = {
        "data": [
            {
                "id": 1,
                "name": "Henrik Aronsson"
            },
            {
                "id": 2,
                "name": "Person Persson"
            }
        ]
    }
    return jsonify(resp)


@app.route('/users/<id>')
def load_user(id):
    users = {
        "1": {
                "id": 1,
                "name": "Henrik Aronsson",
                "email": "henrik@mail.com"
            },
        "2": {
                "id": 2,
                "name": "Person Persson",
                "email": "pers@mail.com"
            }
    }

    if id in users:
        return jsonify(users[id])

    return { "data": None }, 404, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)