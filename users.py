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
        resp.append({ "id": USERS[userid]['id'], "name": USERS[userid]['name'] })

    return API.OK(resp)

def get(id):
    if id in USERS:
        return API.OK(USERS[id])

    return API._404("No such user")

def update(id, user):
    if id in USERS:
        if "email" in user:
            USERS[id]["email"] = user["email"]

        if "name" in user:
            USERS[id]["name"] = user["name"]

        return API.OK(USERS[id])
    
    return API.NotFound("User not found")

def add(user):
    newId = int(max(USERS, key=int)) + 1

    try:
        USERS[str(newId)] = {
            "id": newId,
            "name": user["name"],
            "email": user["email"]
        }
    except KeyError as keyErr:
        return API.Error("Missing attribute: " + str(keyErr))

    return API.Created(USERS[str(newId)])

def remove(id):
    if id not in USERS:
        return API.NotFound("User not found")
    
    del USERS[id]
    return API.OK(None)