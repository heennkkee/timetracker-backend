import API
import DB

def list_all():
    resp = []

    for userid in DB.USERS:
        resp.append({ "id": DB.USERS[userid]['id'], "name": DB.USERS[userid]['name'], "email": DB.USERS[userid]['email'] })

    return API.OK(resp)

def get(userid):
    if userid in DB.USERS:
        return API.OK(DB.USERS[userid])

    return API.NotFound("No such user")

def update(userid, body):
    if userid in DB.USERS:
        if "email" in body:
            DB.USERS[userid]["email"] = body["email"]

        if "name" in body:
            DB.USERS[userid]["name"] = body["name"]

        return API.OK(DB.USERS[userid])
    
    return API.NotFound("User not found")

def add(body):
    newId = int(max(DB.USERS, key=int)) + 1

    try:
        DB.USERS[str(newId)] = {
            "id": newId,
            "name": body["name"],
            "email": body["email"]
        }
    except KeyError as keyErr:
        return API.Error("Missing attribute: " + str(keyErr))

    return API.Created(DB.USERS[str(newId)])

def remove(userid):
    if userid not in DB.USERS:
        return API.NotFound("User not found")
    
    del DB.USERS[userid]
    return API.OK(None)