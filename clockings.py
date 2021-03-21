import datetime, copy
import API
import DB

def list_users_all_clockings(userid, limit=None):

    return API.OK(DB.get_clockings(userid, limit))

def add(userid, body):
    clocking = None
    
    try:
        clocking = {
            "userid": userid,
            "direction": body["direction"],
            "datetime": body.get("datetime", datetime.datetime.utcnow())
        }
    except KeyError as keyErr:
        return API.InputError("Missing attribute: " + str(keyErr))
    
    clocking = DB.add_clocking(clocking)

    return API.Created(clocking)