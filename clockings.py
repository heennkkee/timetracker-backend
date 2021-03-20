import datetime, copy
import API
import DB

def list_users_all_clockings(userid, limit=None):
    resp = []
    if not DB.get_user(userid):
        return API.NotFound("No such user")

    for clocking in DB.CLOCKINGS:
        if clocking['user_id'] == userid:
            resp.append(copy.deepcopy(clocking))
    
    resp.reverse()

    for x in resp:
        x["datetime"] = x["datetime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

    if limit == None:
        return API.OK(resp)
    
    return API.OK(resp[:limit])

def add(userid, body):
    newId = max(clocking["id"] for clocking in DB.CLOCKINGS) + 1

    try:
        DB.CLOCKINGS.append({
            "id": newId,
            "user_id": userid,
            "direction": body["direction"],
            "datetime": body.get("datetime", datetime.datetime.now())
        })
    except KeyError as keyErr:
        return API.InputError("Missing attribute: " + str(keyErr))

    return API.Created(DB.CLOCKINGS[-1])