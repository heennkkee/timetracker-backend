import requests, time, secrets, uuid, hashlib, binascii, os, pyotp
import API, DB

def getNewSalt():
    return hashlib.sha256(os.urandom(60)).hexdigest()

def checkPwdHash(pwd, salt, targetHash):
    return binascii.hexlify(targetHash) == binascii.hexlify(calcPwdHash(pwd, salt))

def calcPwdHash(pwd, salt):
    return hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), 100000, dklen=128)

def login(body):
    email = body["e-mail"]
    password = body["password"]
    mfacode = body.get("mfacode", None)
    
    user = DB.get_user_by_email(email, True)

    if not user:
        return API.Unauthorized("Authorization failed")

    if not checkPwdHash(password, user["salt"], user["pwdhash"]):
        return API.Unauthorized("Authorization failed")

    if user["mfasecret"]:
        if not mfacode:
            return API.Forbidden("2fa")
        
        valid_window = 5
        # ugly workaround for some local clock-issues..
        if __debug__:
            valid_window = 300

        if not pyotp.TOTP(user["mfasecret"]).verify(mfacode, valid_window=valid_window):
            return API.Unauthorized("Authorization failed")

    session = secrets.token_urlsafe(16)

    idValidity = 24 #hours
    DB.add_auth(user["id"], session, idValidity)

    return API.OK({ "session": session, "userid": user["id"] }, { 'Set-Cookie': 'session={0}; Path=/; Max-Age={1}; SameSite=None; Secure'.format(session, idValidity * 3600) })

def isValidSession(apikey, required_scopes=None):
    if DB.check_if_session_valid(apikey):
        return {'sub': 'whatever'}

    return None

def check():
    return API.OK(None)

def logout(body):
    # Workaround...?
    try:
        session = body["session"]
        DB.remove_auth(session)
    except Exception:
        whatever = False
    finally:
        return API.OK(None, { 'Set-Cookie': 'session=; Path=/; Max-Age=-1; SameSite=None; Secure'})
