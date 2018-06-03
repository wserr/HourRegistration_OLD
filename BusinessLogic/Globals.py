import time
import win32evtlog
import wmi
import getpass
import datetime

def GetCurrentTime():
    return roundTime().strftime("%Y-%m-%d %H:%M")

def GetCurrentDay():
    return time.strftime('%d-%m-%Y')

def GetLastLogon():
    user = getpass.getuser()
    start_date = datetime.datetime.now() +  datetime.timedelta(days=-1)
    end_date = start_date + datetime.timedelta(days=2)

    dtmStartDate = datetime.datetime.strftime(start_date,'%Y%m%d000000.000000-480')
    #dtmStartDate = '20180512000000.000000-480'
    dtmEndDate = datetime.datetime.strftime(end_date,'%Y%m%d000000.000000-480')
    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("Select * from Win32_NTLogEvent Where TimeWritten > '" + dtmStartDate + "' and TimeWritten < '" + dtmEndDate + "'" + "and EventCode =" + str(4672))
           
    # Query WMI object.
    wql_r = wmi_o.query(wql)
    t = None
    for i in wql_r:
        if i.InsertionStrings[1] == user:
            t = i.TimeGenerated
            break

    # year = t[:4]
    # month = t[4:6]
    # day = t[6:8]
    hour = ""
    minutes = ""

    if not t is None:
        hour = str(int(t[8:10])+2)
        minutes = t[10:12]
    return hour + ":" + minutes # + " " + day + "-" + month + "-" + year

def roundTime(dt=None, dateDelta=datetime.timedelta(minutes=5)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
