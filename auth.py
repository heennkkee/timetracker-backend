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
        return API.Unauthorized("Authorization failed")

    session = secrets.token_urlsafe(16)
    
    DB.add_auth(userid, session, int(time.time()) + 3600)

    return API.OK({ "session": session }, { 'Set-Cookie': 'session={0}; Path=/; Max-Age=3600; SameSite=None; Secure'.format(session) })

def isValidSession(apikey, required_scopes=None):
    if DB.check_if_session_valid(apikey):
        return {'sub': 'whatever'}

    return None

def logout(userid, body):
    # Workaround...?
    session = body["session"]

    DB.remove_auth(session)

    return API.OK(None, { 'Set-Cookie': 'session=; Path=/; Max-Age=-1; SameSite=None; Secure'})
