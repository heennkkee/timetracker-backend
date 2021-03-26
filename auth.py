import requests, time, secrets, uuid, hashlib, binascii, os, pyotp
import API, DB

# pyotp.random_base32()
# pyotp.TOTP(secret).now()

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
        
        if not pyotp.TOTP(user["mfasecret"]).verify(mfacode):
            return API.Unauthorized("Authorization failed")

    session = secrets.token_urlsafe(16)

    DB.add_auth(user["id"], session, int(time.time()) + 3600 * 24) # 24 hours validity

    return API.OK({ "session": session, "userid": user["id"] }, { 'Set-Cookie': 'session={0}; Path=/; Max-Age=3600; SameSite=None; Secure'.format(session) })

def isValidSession(apikey, required_scopes=None):
    if DB.check_if_session_valid(apikey):
        return {'sub': 'whatever'}

    return None

def check():
    return API.OK(None)

def logout(body):
    # Workaround...?
    session = body["session"]

    DB.remove_auth(session)

    return API.OK(None, { 'Set-Cookie': 'session=; Path=/; Max-Age=-1; SameSite=None; Secure'})
