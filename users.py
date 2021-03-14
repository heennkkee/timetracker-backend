from flask import jsonify

USERS = {
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

def list_all():
    resp = []

    for userid in USERS:
        resp.append({ "id": USERS[userid]['id'], "name": USERS[userid]['name'] })

    return jsonify({ "data": resp })