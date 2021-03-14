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

def get(id):
    if id in USERS:
        return jsonify({ "data": USERS[id] })

    return { "data": None }, 404, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

def update(id, user):
    if id in USERS:
        if "email" in user:
            USERS[id]["email"] = user["email"]

        if "name" in user:
            USERS[id]["name"] = user["name"]

        return jsonify(USERS[id])
    
    return { "data": None }, 404, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }

def add(user):
    newId = int(max(USERS, key=int)) + 1

    try:
        USERS[str(newId)] = {
            "id": newId,
            "name": user["name"],
            "email": user["email"]
        }
    except KeyError as keyErr:
        return "Missing attribute " + str(keyErr), 400

    return jsonify(USERS[str(newId)])