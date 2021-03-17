import datetime
import time
import secrets

USERS = {
    1: {
            "id": 1,
            "name": "Henrik Aronsson",
            "email": "henrik.aronsson.94@gmail.com"
        },
    2: {
            "id": 2,
            "name": "Person Persson",
            "email": "pers@mail.com"
        }
}

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

AUTHENTICATIONS = [
    {
        "session": secrets.token_urlsafe(16),
        "userid": 1,
        "expiry": int(time.time()) + 3600
    }
]