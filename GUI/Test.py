import wmi
import time
import datetime
import onepy
import os

def GetLatestLogon():

    start_date = datetime.datetime.now() +  datetime.timedelta(days=-1)
    end_date = start_date + datetime.timedelta(days=2)

    dtmStartDate = datetime.datetime.strftime(start_date,'%Y%m%d000000.000000-480')
    #dtmStartDate = '20180512000000.000000-480'
    dtmEndDate = datetime.datetime.strftime(end_date,'%Y%m%d000000.000000-480')
    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("Select TimeGenerated from Win32_NTLogEvent Where TimeWritten > '" + dtmStartDate + "' and TimeWritten < '" + dtmEndDate + "'" + "and EventCode =" + str(4672))


    # Query WMI object.
    wql_r = wmi_o.query(wql)
    t = wql_r[0].TimeGenerated

    year = t[:4]
    month = t[4:6]
    day = t[6:8]
    hour = str(int(t[8:10])+2)
    minutes = t[10:12]

    return hour + ":" + minutes + " " + day + "-" + month + "-" + year

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

#os.system("start "+"onenote:https://d.docs.live.net/3fa0ca2f0d0fdaf8/Documenten/Projecten/Ureningave/Test_1.one#Nieuwe%20features&section-id={B92C728E-23D3-4FF1-87B5-6EFD01014A69}&page-id={A34C7AFF-7ED1-4F45-87B1-AC20B3306B3A}&end")

link = "https://onedrive.live.com/view.aspx?resid=3FA0CA2F0D0FDAF8%212150&id=documents&wd=target%28Ureningave%2FTest_1.one%7CB92C728E-23D3-4FF1-87B5-6EFD01014A69%2FBugs%7C746E9F8D-C568-482F-B330-84CC4F4E0F84%2F%29onenote:https://d.docs.live.net/3fa0ca2f0d0fdaf8/Documenten/Projecten/Ureningave/Test_1.one#Bugs&section-id={B92C728E-23D3-4FF1-87B5-6EFD01014A69}&page-id={746E9F8D-C568-482F-B330-84CC4F4E0F84}&end"
#link = "test"
try:
    if not link=="":
        secondPart = link.split("onenote")[1]
        fullLink = "onenote"+secondPart
        os.system("start "+fullLink)
except:
    link = ""
    print("No valid link found")

