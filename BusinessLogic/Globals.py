import time
import win32evtlog
import wmi
import getpass
import datetime
import configparser
from BusinessLogic import BLProject,BLTimeRecord,BLRecordType
from BusinessEntities import TimeRecordStatusEnum
from DataAccess.Log import Logger

def GetCurrentTime():
    return roundTime().strftime("%Y-%m-%d %H:%M")

def GetCurrentDay():
    return time.strftime('%d-%m-%Y')

def GetLastLogon():
    try:
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
    except Exception as e:
        Logger.LogError(e)


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

def ClearUserTables(dbConn):
    config = configparser.ConfigParser()
    config.read('config.ini')
    reset = int(config['RESET']['Reset'])
    if reset == 1:
        blPr = BLProject.BLProject(dbConn)
        blTr = BLTimeRecord.BLTimeRecord(dbConn)
        blPr.DeleteAll()
        blTr.DeleteAll()
        config['RESET']['Reset'] = '0'   # create

        with open('config.ini', 'w') as configfile:    # save
            config.write(configfile)

def CopyToCodex(dbConn,date):
    try:
        blTr = BLTimeRecord.BLTimeRecord(dbConn)
        timeRecords = blTr.GetAllForDate(date)
        blPr = BLProject.BLProject(dbConn)
        blRt = BLRecordType.BLRecordType(dbConn)
        sequence = ''
        for item in timeRecords:       
            item1 = blPr.GetProjectExterneID(item.ProjectID)
            item2 = blRt.GetRecordTypeExterneID(item.RecordTypeID)
            s1Time = time.strptime(item.StartHour, "%Y-%m-%d %H:%M")
            s2Time = time.strptime(item.EndHour,"%Y-%m-%d %H:%M")
            item3 = time.strftime("%H:%M",s1Time)
            item4 = time.strftime("%H:%M",s2Time)
            item5 = item.Description
            s="" 
            string1 = ""
            string2 = ""
            item.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gekopieerd.value
            blTr.Update(item)
            if len(item5) > 30:
                items = item5.split(" ")
                countChar = 0

                indexToSplit = 0
                for i in range(0,len(items)):
                    countChar =countChar + len(items[i])
                    if i>30:
                        indexToSplit = i-1
                        break
                filler = " "
                if indexToSplit == 0:
                    indexToSplit = 30
                    filler = ""
                list1 = item5[0:indexToSplit]
                list2 = item5[indexToSplit:]
                string1 = filler.join(list1)
                string2 = filler.join(list2)
            else:
                string1 = item5
            km = "\t"
            if not item.Km is None:
                km = str(item.Km) + "\t"
            line = (item1,"\t","\t","\t",item2,"\t","\t","\t",km,"\t",item3,"\t",item4,"\t",string1,"\t",string2,"\n")
            sequence = sequence + s.join(line)
        return sequence
    except Exception as e:
        Logger.LogError(str(e))


def ConvertToAmericanDate(dateString):
    try:
        timeArray = dateString.split('-')
        year = timeArray[2]
        month = timeArray[1]
        day = timeArray[0]
        return year + '-' + month + '-' + day
    except Exception as e:
        Logger.LogError(e)


def ConvertToEuropeanTime(dateString):
    try:
        timeArray = dateString.split('-')
        year = timeArray[0]
        month = timeArray[1]
        day = timeArray[2]
        return year + '-' + month + '-' + day
    except Exception as e:
        Logger.LogError(e)




