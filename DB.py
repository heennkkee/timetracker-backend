import datetime
import time
import secrets

try:
    import my_secrets
except Exception:
    ignore = True

import os
import psycopg2
from psycopg2.extras import RealDictCursor


DATABASE_URL = None
try:
    DATABASE_URL = my_secrets.DB_URL
except NameError:
    DATABASE_URL = os.environ['DATABASE_URL']

def open():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def close(conn, cur):
    cur.close()
    conn.close()

def get_users():
    conn, cur = open()

    cur.execute("SELECT id as id, name as name, email as email FROM public.user ORDER BY id ASC")
    users = cur.fetchall()

    close(conn, cur)
    return users

def get_user_by_email(email, includeHash = False):
    conn, cur = open()

    sql = ''

    if includeHash:
        sql = 'SELECT id as id, name as name, email as email, salt as salt, pwdhash as pwdhash, mfasecret as mfasecret FROM public.user WHERE email = %s'
    else:
        sql = 'SELECT id as id, name as name, email as email FROM public.user WHERE email = %s'

    cur.execute(sql, ( email, ))
    user = cur.fetchone()

    close(conn, cur)
    return user

def get_user(id, includeHash = False):
    conn, cur = open()
    sql = ''

    if includeHash:
        sql = 'SELECT id as id, name as name, email as email, salt as salt, pwdhash as pwdhash, mfasecret as mfasecret FROM public.user WHERE id = %s'
    else:
        sql = 'SELECT id as id, name as name, email as email FROM public.user WHERE id = %s'

    cur.execute(sql, ( id, ))
    user = cur.fetchone()

    close(conn, cur)
    return user

def update_user_password(userId, pwdHash, newSalt):
    conn, cur = open()

    succes = True
    try:
        cur.execute("UPDATE public.user SET pwdhash=%s, salt=%s WHERE id = %s",
            (pwdHash, newSalt, userId) )
        conn.commit()
    except Exception:
        succes = False
    finally:
        close(conn, cur)

    close(conn, cur)

    return succes


def update_user(user):
    conn, cur = open()

    succes = True
    try:
        cur.execute("UPDATE public.user SET name=%s, email=%s WHERE id = %s",
            (user["name"], user["email"], user["id"]) )
        conn.commit()
    except Exception:
        succes = False
    finally:
        close(conn, cur)

    
    close(conn, cur)

    return succes

def add_user(user):
    conn, cur = open()

    issue = cur.execute("INSERT INTO public.user (name, email, salt, pwdhash) VALUES (%s, %s, %s, %s) RETURNING id", ( user["name"], user["email"], user["salt"], user["pwdhash"] ))
    if not issue:
        conn.commit()

    newId = cur.fetchone()
    if not newId:
        raise Exception("Failed to insert post")
    
    user["id"] = newId["id"]

    close(conn, cur)

    return user

def remove_user(userid):
    conn, cur = open()

    succes = True
    try:
        cur.execute("DELETE FROM public.user WHERE ID = %s", ( userid, ))
        conn.commit()
    except Exception:
        succes = False
    finally:
        close(conn, cur)

    return succes

def add_auth(userid, session, validHours):
    conn, cur = open()

    issue = cur.execute("INSERT INTO public.authenticate (userid, session, expiry) VALUES (%s, %s, (NOW() + interval '%s hour'))", ( userid, session, validHours ))
    if not issue:
        conn.commit()

    close(conn, cur)

def check_if_session_valid(session):
    conn, cur = open()
    
    cur.execute("SELECT 'exists' FROM public.authenticate WHERE session = %s AND expiry > NOW() ORDER BY expiry DESC LIMIT 1", ( session,  ))
    auths = cur.fetchone()

    close(conn, cur)

    if auths:
        return True
    
    return False

def remove_auth(session):
    conn, cur = open()

    issue = cur.execute("DELETE FROM public.authenticate WHERE session = %s", ( session, ))
    if not issue:
        conn.commit()

    close(conn, cur)

def get_clockings(userid, limit=None, since=None, to=None):
    conn, cur = open()
    sqlLimit = ''
    sqlSince = ''
    sqlTo = ''

    if limit:
        sqlLimit = ' LIMIT %s '

    if since:
        sqlSince = ' AND datetime >= %s '

    if to:
        sqlTo = ' AND datetime < %s '

    sql = 'SELECT id as id, userid as userid, datetime as datetime, direction as direction FROM public.clocking WHERE userid = %s ' + sqlSince + sqlTo + ' ORDER BY datetime desc' + sqlLimit

    if limit and since and to:
        cur.execute(sql, ( userid, since, limit, to ))
    elif since and to:
        cur.execute(sql, ( userid, since, to ))
    elif since and limit:
        cur.execute(sql, ( userid, since, limit ))
    elif to and limit:
        cur.execute(sql, ( userid, to, limit ))
    elif since: 
        cur.execute(sql, ( userid, since ))
    elif limit:
        cur.execute(sql, ( userid, limit ))
    elif to:
        cur.execute(sql, ( userid, to ))
    else:
        cur.execute(sql, ( userid, ))
    
    clockings = cur.fetchall()

    close(conn, cur)
    
    return clockings

def add_clocking(clocking):
    conn, cur = open()

    try:
        cur.execute("INSERT INTO public.clocking (userid, direction, datetime) VALUES (%s, %s, %s) RETURNING id", ( clocking["userid"], clocking["direction"], clocking["datetime"] ))
        conn.commit()
        newId = cur.fetchone()
        if not newId:
            raise Exception("Failed to insert post")
        
        clocking["id"] = newId["id"]
    except Exception:
        test = False
    finally:
        close(conn, cur)
    
  
    return clocking

def remove_clocking(userid, clockingid):
    conn, cur = open()

    succes = True
    try:
        cur.execute("DELETE FROM public.clocking WHERE id = %s and userid = %s", ( clockingid, userid))
        conn.commit()
    except Exception:
        succes = False
    finally:
        close(conn, cur)

    return succes

def get_clocking(userid, clockingid):
    conn, cur = open()
    sql = 'SELECT id as id, userid as userid, direction as direction, datetime as datetime FROM public.clocking WHERE id = %s and userid = %s'

    cur.execute(sql, ( clockingid, userid ))
    clocking = cur.fetchone()

    close(conn, cur)
    return clocking

