import time

def dateTimeToMillis(dateTime):
# eg:10-01 18:50:28.346
    millis = dateTime[-3:]
    dateTime = ("2016-" + dateTime)[:-4]
    print "millis:%r, dateTime:%r" % (millis, dateTime)
    timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    print "dateTime -> %r" % timeStamp
    timeStamp += int(millis)
    print "dateTime -> %r" % timeStamp
    return timeStamp
