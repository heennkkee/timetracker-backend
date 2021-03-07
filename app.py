from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    resp = {
        "data": [
            "hej",
            "wops"
        ]
    }
    return resp, 200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

@app.route('/users')
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
    return resp, 200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }


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
        return { "data": users[id] }, 200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

    return { "data": None }, 404, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

if __name__ == '__main__':
    app.run()