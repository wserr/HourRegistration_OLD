import time
import win32evtlog
import wmi
import getpass
import datetime

def GetCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M")

def GetCurrentDay():
    return time.strftime('%d-%m-%Y')

def GetLastLogon():
    user = getpass.getuser()
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=1)

    dtmStartDate = datetime.datetime.strftime(start_date,'%Y%m%d000000.000000-480')
    #dtmStartDate = '20180512000000.000000-480'
    dtmEndDate = datetime.datetime.strftime(end_date,'%Y%m%d000000.000000-480')
    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("Select * from Win32_NTLogEvent Where TimeWritten >= '" + dtmStartDate + "' and TimeWritten < '" + dtmEndDate + "'" + "and EventCode =" + str(4672))
           
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


