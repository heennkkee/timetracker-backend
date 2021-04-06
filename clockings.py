import datetime, copy
import API
import DB
from pytz import timezone

def list_user_clockings(userid, limit=None, since=None, to=None):
    return API.OK(DB.get_clockings(userid, limit, since, to))

def remove_clocking(userid, clockingid):
    clocking = DB.get_clocking(userid, clockingid)
    if not clocking:
        API.NotFound("No such clocking")

    if not DB.remove_clocking(userid, clockingid):
        return API.ServerError("Failed to remove clocking")
    
    return API.OK(None)

def summarizeTimePerDay(userid, since, to):
    clockings = DB.get_clockings(userid, None, since, to, 'asc')

    dateSummaries = {}
    previousClocking = None
    for clocking in clockings:
        strKey = str(clocking['datetime'].date())

        # Existing or new post?
        if not strKey in dateSummaries.keys():
            # Create a post to keep our counts in
            dateSummaries[strKey] = {
                'worktime': 0,
                'ob1': 0,
                'ob2': 0,
                'ob3': 0
            }

            # midnight
            myTz = timezone('Europe/Stockholm')
            midnight = myTz.localize(datetime.datetime.combine(clocking['datetime'].date(), datetime.time(0)))
            
            
            # If we clocked out, we worked in the night...
            if clocking['direction'] == 'out':
                # Add OB here...
                dateSummaries[strKey]['worktime'] = (clocking['datetime'] - midnight).seconds
            
            # Do we have a previous clocking (i.e. this is a new day, but not the first)
            # Check if it was a "clock in", then add some time to yesterday as well.
            if previousClocking:
                if previousClocking['direction'] == 'in':
                    # Add OB here...
                        dateSummaries[str(previousClocking['datetime'].date())]['worktime'] += (midnight - previousClocking['datetime']).seconds
        
        else:
            # We've already got this post in our summaries
            if clocking['direction'] == 'out':
                # Add OB here...
                dateSummaries[strKey]['worktime'] += (clocking['datetime'] - previousClocking['datetime']).seconds

        previousClocking = clocking
        
    return API.OK(dateSummaries)
        

# Weekday range(0, 6) (0 t.o.m 5)
# 21-24: OB1
# 00-07: OB2

# Weekday 5
# 07-21: OB3

# Weekday 6 (holidays)
# 00-24: OB3

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