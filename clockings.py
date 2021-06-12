import datetime, copy
import API
import DB
from pytz import timezone
from dateutil import easter
from datetime import timedelta

# To-Do: move this to user setting/schedule instead.
myTz = timezone('Europe/Stockholm')

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

    # iterate to... make timezone adjustments
    for cl in clockings:
        cl['datetime'] = cl['datetime'].astimezone(myTz)

    dateSummaries = {}
    maxLength = len(clockings)

    for i in range(maxLength):
        previousClocking = clockings[i - 1] if i > 0 else None
        clocking = clockings[i]

        # midnight
        midnight = myTz.localize(datetime.datetime.combine(clocking['datetime'].date(), datetime.time(0)))

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
                        
            # If we clocked out, we worked in the night...
            if clocking['direction'] == 'out':
                ob = checkOb(midnight, clocking['datetime'])
                dateSummaries[strKey]['worktime'] = (clocking['datetime'] - midnight).seconds
                dateSummaries[strKey]['ob1'] = ob['ob1']
                dateSummaries[strKey]['ob2'] = ob['ob2']
                dateSummaries[strKey]['ob3'] = ob['ob3']
            
            # Do we have a previous clocking (i.e. this is a new day, but not the first)
            # Check if it was a "clock in", then add some time to yesterday as well.
            if previousClocking:
                if previousClocking['direction'] == 'in':
                    ob = checkOb(previousClocking['datetime'], midnight)
                    key = str(previousClocking['datetime'].date())
                    dateSummaries[key]['worktime'] += (midnight - previousClocking['datetime']).seconds
                    dateSummaries[key]['ob1'] += ob['ob1']
                    dateSummaries[key]['ob2'] += ob['ob2']
                    dateSummaries[key]['ob3'] += ob['ob3']

        else:
            # We've already got this post in our summaries
            if clocking['direction'] == 'out':
                ob = checkOb(previousClocking['datetime'], clocking['datetime'])
                dateSummaries[strKey]['worktime'] += (clocking['datetime'] - previousClocking['datetime']).seconds
                dateSummaries[strKey]['ob1'] += ob['ob1']
                dateSummaries[strKey]['ob2'] += ob['ob2']
                dateSummaries[strKey]['ob3'] += ob['ob3']

    summary = {
        'worktime': 0,
        'ob1': 0,
        'ob2': 0,
        'ob3': 0
    }

    for dateKey in dateSummaries:
        summary['worktime'] += dateSummaries[dateKey]['worktime']
        summary['ob1'] += dateSummaries[dateKey]['ob1']
        summary['ob2'] += dateSummaries[dateKey]['ob2']
        summary['ob3'] += dateSummaries[dateKey]['ob3']

    return API.OK({ 'summary': summary, 'details': dateSummaries })
        

def checkOb(fr, to):
    # 00-24 (weekday == 6):         OB3
    # 07-21 (weekday == 5):         OB3
    # 00-07 (weekday range(0, 6)):  OB2
    # 21-24 (weekday range(0, 6)):  OB1

    if (fr.tzinfo != to.tzinfo):
        raise("From and to must be the same timezone")

    returnValue = {
        'ob1': 0,
        'ob2': 0,
        'ob3': 0
    }

    isHoliday = checkHolidays(fr.date())
    weekDay = fr.weekday()

    seven = datetime.datetime.combine(fr.date(), datetime.time(hour=7, tzinfo=fr.tzinfo))
    eveningNine = datetime.datetime.combine(fr.date(), datetime.time(hour=21, tzinfo=fr.tzinfo))
    if isHoliday or weekDay == 6:
        returnValue['ob3'] = (to - fr).seconds
    else:
        if (to <= seven):
            # Same for weekdays [0, 5]
            # OB2 (full range)
            returnValue['ob2'] = (to - fr).seconds
        elif (fr >= eveningNine):
            # Same for weekdays [0, 5]
            # OB 1 (full range)
            returnValue['ob1'] = (to - fr).seconds
        elif (fr >= seven and to <= eveningNine):
            if (weekDay == 5):
                returnValue['ob3'] = (to - fr).seconds
#            else:
#               no Ob
        elif (fr < seven and to > eveningNine):
            # Overlap whole day (OB2, (no OB | OB3), OB1)
            returnValue['ob2'] = (seven - fr).seconds
            returnValue['ob1'] = (to - eveningNine).seconds
            if weekDay == 5:
                returnValue['ob3'] = (eveningNine - to).seconds
        elif (fr < seven):
            # overlap morning -> midday (OB2, (no OB | OB3))
            returnValue['ob2'] = (seven - fr).seconds
            if weekDay == 5:
                returnValue['ob3'] = (to - seven).seconds
        else:
            # overlap midday -> evening ((no ob | OB3) -> OB1)
            if weekDay == 5:
                returnValue['ob3'] = (to - seven).seconds

            returnValue['ob1'] = (to - eveningNine).seconds
            
    return returnValue


def checkHolidays(dt):
    month = dt.month
    day = dt.day
    if month == 1:
        if day in [1, 6]:
            return True
    if month == 5:
        if day in [1]:
            return True
    if month == 6:
        if day in [6]:
            return True
        
        # Midsummer
        if day in range(20, 27) and dt.weekday == 5: # saturday
            return True

    if month == 12:
        if day in [25, 26]:
            return True

    # Easter
    easterDt = easter.easter(dt.year)
    # Påskdagen
    if dt == easterDt:
        return True
    
    # Annandag påsk
    if dt == (easterDt + timedelta(days=1)):
        return True

    # Långfredagen
    if dt == (easterDt - timedelta(days=2)):
        return True
    
    # Kristi flygare
    if dt == (easterDt + timedelta(days=39)):
        return True

    return False

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