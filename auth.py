import requests
import time
import API
import DB
import uuid
import secrets

LAME_SECRET = "suchsecret"

def login(userid, body):
    password = body["password"]
    
    # Validate password...
    if password != password:
        return API.Unauthenticated("Failed to authenticate")

    session = secrets.token_urlsafe(16)

    DB.AUTHENTICATIONS.append({
        "userid": userid,
        "session": session,
        "expiry": int(time.time()) + 3600 # 1 hour
    })

    return API.OK({ "session": session }, { 'Set-Cookie': 'session={0}; Path=/; Max-Age=3600; SameSite=None'.format(session) })

def isValidSession(apikey, required_scopes=None):

    epoch = int(time.time())
    auths = (x for x in DB.AUTHENTICATIONS if x["session"] == apikey and x["expiry"] > epoch)

    try:
        next(auths)
        return {'sub': 'whatever'}
    except StopIteration:
        return False

def logout(userid, body):
    # Workaround...?
    session = body["session"]
    DB.AUTHENTICATIONS = [x for x in DB.AUTHENTICATIONS if not (x["session"] == session and x["userid"] == userid)]

    return API.OK(None, { 'Set-Cookie': 'session=; Path=/; Max-Age=-1; SameSite=None'})