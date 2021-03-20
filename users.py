import API
import DB

def list_all():
    return API.OK(DB.get_users())

def get(userid):
    user = DB.get_user(userid)
    if not user:
        return API.NotFound("No such user")

    return API.OK(user)


def update(userid, body):
    user = DB.get_user(userid)

    if not user:
        return API.NotFound("No such user")

    if "id" in body:
        if userid != body["id"]:
            return API.InputError("IDs are not matching")

    if "email" in body:
        user["email"] = body["email"]

    if "name" in body:
        user["name"] = body["name"]
    
    if DB.update_user(user):
        return API.OK(user)
    
    return API.ServerError("Failed to update user")

def add(body):

    try:
        newUser = {
            "name": body["name"],
            "email": body["email"]
        }
    except KeyError as keyErr:
        return API.InputError("Missing attribute: " + str(keyErr))

    newUser = DB.add_user(newUser)

    return API.Created(newUser)

def remove(userid):
    user = DB.get_user(userid)
    if not user:
        return API.NotFound("No such user")
    
    if not DB.remove_user(userid):
        return API.ServerError("Failed to remove user")

    return API.OK(None)