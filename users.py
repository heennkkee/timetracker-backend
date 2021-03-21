import API, DB, auth

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

def update_password(userid, body):
    user = DB.get_user(userid, True)
    newPassword = body["newPassword"]
    password = body["password"]
    
    if not user:
        return API.NotFound("No such user")

    if not auth.checkPwdHash(password, user["salt"], user["pwdhash"]):
        return API.Unauthorized("Authorization failed")

    salt = auth.getNewSalt()

    if DB.update_user_password(userid, auth.calcPwdHash(newPassword, salt), salt):
        return API.OK(None)
    
    return API.ServerError("Failed to update password")


def add(body):

    try:
        salt = auth.getNewSalt()
        pwdhash = auth.calcPwdHash(body["password"], salt)
        newUser = {
            "name": body["name"],
            "email": body["email"],
            "salt": salt,
            "pwdhash": pwdhash
        }
    except KeyError as keyErr:
        return API.InputError("Missing attribute: " + str(keyErr))

    newUser = DB.add_user(newUser)
    user = DB.get_user(newUser["id"])
    return API.Created(user)

def remove(userid):
    user = DB.get_user(userid)
    if not user:
        return API.NotFound("No such user")
    
    if not DB.remove_user(userid):
        return API.ServerError("Failed to remove user")

    return API.OK(None)