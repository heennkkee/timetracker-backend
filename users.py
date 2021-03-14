import API

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
        resp.append({ "id": USERS[userid]['id'], "name": USERS[userid]['name'], "email": USERS[userid]['email'] })

    return API.OK(resp)

def get(id):
    if id in USERS:
        return API.OK(USERS[id])

    return API._404("No such user")

def update(id, body):
    if id in USERS:
        if "email" in body:
            USERS[id]["email"] = body["email"]

        if "name" in body:
            USERS[id]["name"] = body["name"]

        return API.OK(USERS[id])
    
    return API.NotFound("User not found")

def add(body):
    newId = int(max(USERS, key=int)) + 1

    try:
        USERS[str(newId)] = {
            "id": newId,
            "name": body["name"],
            "email": body["email"]
        }
    except KeyError as keyErr:
        return API.Error("Missing attribute: " + str(keyErr))

    return API.Created(USERS[str(newId)])

def remove(id):
    if id not in USERS:
        return API.NotFound("User not found")
    
    del USERS[id]
    return API.OK(None)