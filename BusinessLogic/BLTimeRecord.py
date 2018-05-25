from DataAccess import DATimeRecord
from BusinessEntities import TimeRecord
import sqlite3
import time

class BLTimeRecord:
    def __init__(self,conn):
        self.DAL = DATimeRecord.DATimeRecord(conn)

    def GetAll(self):
        return self.DAL.GetAll()

    def Create(self,timeRecord):
        self.DAL.Create(timeRecord)

    def GetById(self,Id):
        return self.DAL.GetByID(Id)
    
    def Update(self,timeRecord):
        s1Time = time.strptime(timeRecord.StartHour, "%Y-%m-%d %H:%M")

        if not timeRecord.EndHour is None:
            s2Time = time.strptime(timeRecord.EndHour,"%Y-%m-%d %H:%M")

            s1TimeSeconds = time.mktime(s1Time)
            s2TimeSeconds = time.mktime(s2Time)

            difference = int((s2TimeSeconds-s1TimeSeconds)/60)
            timeRecord.Minutes = difference

        self.DAL.Update(timeRecord)

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

    