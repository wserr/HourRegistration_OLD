from DataAccess import DATimeRecordView
from BusinessEntities import TimeRecordView
import sqlite3
from BusinessLogic import BLTimeRecord

class BLTimeRecordView:
    def __init__(self,conn):
        self.DAL = DATimeRecordView.DATimeRecordView(conn)
        self.Connection = conn

    def GetAll(self):
        return self.DAL.GetAll()

    def GetById(self, Id):
        return self.DAL.GetByID(Id)
    
    def GetByIdList(self, Ids):
        return self.DAL.GetByIdList(Ids)

    def GetAllForDate(self,date):
        blTr = BLTimeRecord.BLTimeRecord(self.Connection)
        Ids = blTr.GetAllIDsForDate(date)
        timeRecordViews = self.GetByIdList(Ids)
        return timeRecordViews

    def GetAllBetweenDates(self,fromDate,toDate):
        return self.DAL.GetAllBetweenDates(fromDate,toDate)
