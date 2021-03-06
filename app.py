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

if __name__ == '__main__':
    app.run()