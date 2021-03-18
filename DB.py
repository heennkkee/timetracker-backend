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

    cur.execute("SELECT id as id, name as name, email as email FROM public.user")
    users = cur.fetchall()

    close(conn, cur)
    return users

def get_user(id):
    conn, cur = open()

    cur.execute('SELECT id as id, name as name, email as email FROM public.user WHERE id = %s', ( id, ))
    user = cur.fetchone()

    close(conn, cur)
    return user

def update_user(user):
    conn, cur = open()

    issue = cur.execute("UPDATE public.user SET name=%s, email=%s WHERE id = %s",
        (user["name"], user["email"], user["id"]) )
    
    if not issue:
        conn.commit()
    
    close(conn, cur)

def add_user(user):
    conn, cur = open()

    issue = cur.execute("INSERT INTO public.user (name, email) VALUES (%s, %s) RETURNING id", ( user["name"], user["email"] ))
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

def add_auth(userid, session, validityInSeconds):
    conn, cur = open()

    issue = cur.execute("INSERT INTO public.authenticate (userid, session, expiry) VALUES (%s, %s, %s)", ( userid, session, validityInSeconds ))
    if not issue:
        conn.commit()

    close(conn, cur)

def check_if_session_valid(session):
    conn, cur = open()
    expiryLimit = int(time.time())
    
    cur.execute("SELECT 'exists' FROM public.authenticate WHERE session = %s AND expiry > %s ORDER BY expiry DESC LIMIT 1", ( session, expiryLimit ))
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

    

AUTHENTICATIONS = [
    {
        "session": secrets.token_urlsafe(16),
        "userid": 1,
        "expiry": int(time.time()) + 3600
    }
]

CLOCKINGS = [
    {
        "id": 1,
        "user_id": 1,
        "datetime": datetime.datetime.now() + datetime.timedelta(hours=-8),
        "direction": "in"
    },
    {
        "id": 2,
        "user_id": 1,
        "datetime": datetime.datetime.now() + datetime.timedelta(hours=-5),
        "direction": "out"
    },
    {
        "id": 3,
        "user_id": 1,
        "datetime": datetime.datetime.now() + datetime.timedelta(hours=-4.5),
        "direction": "in"
    }
]

