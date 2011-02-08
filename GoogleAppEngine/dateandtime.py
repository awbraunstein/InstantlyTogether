import datetime

def within(t1, t2):
    hr = datetime.timedelta(minutes=20)
    if t1 == None or t2 == None:
        return false
    if t1>t2:
        delta = t1-t2
        print t1
        print t2
    else:
        delta = t2-t1
        print t2
        print t1
    return delta <= hr