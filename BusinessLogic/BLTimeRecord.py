from DataAccess import DATimeRecord
from BusinessEntities import TimeRecord, TimeRecordStatusEnum
from BusinessLogic import Globals
import sqlite3
import time


class BLTimeRecord:
    def __init__(self,conn):
        self.DAL = DATimeRecord.DATimeRecord(conn)

    def GetAll(self):
        return self.DAL.GetAll()

    def Create(self,timeRecord):
        updatedTimeRecord = self.UpdateTimeDifference(timeRecord)
        self.DAL.Create(updatedTimeRecord)

    def GetById(self,Id):
        return self.DAL.GetByID(Id)
    
    def Update(self,timeRecord):
        updatedTimeRecord = self.UpdateTimeDifference(timeRecord)
        self.DAL.Update(updatedTimeRecord)

    def GetByIDList(self,Ids):
        return self.DAL.GetByIDList(Ids)

    def GetAllForDate(self,date):
        return self.DAL.GetAllForDate(date)

    def GetAllIDsForDate(self,date):
        idList = []
        timeRecords =  self.DAL.GetAllForDate(date) 
        for item in timeRecords:
            idList.append(item.ID)
        return idList

    def DeleteByID(self, id):
        self.DAL.DeleteByID(id)

    def DeleteAll(self):
        self.DAL.DeleteAll()

    def UpdateTimeDifference(self,timeRecord):
        s1Time = time.strptime(timeRecord.StartHour, "%Y-%m-%d %H:%M")

        if not timeRecord.EndHour is None:
            s2Time = time.strptime(timeRecord.EndHour,"%Y-%m-%d %H:%M")

            s1TimeSeconds = time.mktime(s1Time)
            s2TimeSeconds = time.mktime(s2Time)

            difference = int((s2TimeSeconds-s1TimeSeconds)/60)
            timeRecord.Minutes = difference
        return timeRecord

    def CopyTimeRecord(self, timeRecord):
        timeRecord.ID = None
        timeRecord.StartHour = Globals.GetCurrentTime()
        timeRecord.EndHour = None
        timeRecord.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value
        timeRecord.Minutes = 0
        self.Create(timeRecord)

    