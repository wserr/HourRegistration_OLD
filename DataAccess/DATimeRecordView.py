import sqlite3
from BusinessEntities import TimeRecordView

class DATimeRecordView:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()
    
    def GetByID(self,Id):
        self.Cursor.execute("SELECT * FROM vwTimeRecord where TRE_ID = ?",(str(Id),))
        rows = self.Cursor.fetchall()
        TimeRecords = []
        for row in rows:
            timeRecord = TimeRecordView.TimeRecordView(row[0],row[1],row[2],row[3],row[4],row[5],row[6],str(row[7]).replace("\n",""))
            TimeRecords.append(timeRecord)
        return TimeRecords[0]

    def GetByIdList(self, Ids):
        idList = []
        for Id in Ids:
            idList.append(self.GetByID(Id))
        return idList        

    def GetAll(self):
        self.Cursor.execute("SELECT * FROM vwTimeRecord order by StartTime DESC")
        rows = self.Cursor.fetchall()
        TimeRecordViews = []
        for row in rows:
            timeRecordview = TimeRecordView.TimeRecordView(row[0],row[1],row[2],row[3],row[4],row[5],row[6],str(row[7]).replace("\n",""))
            TimeRecordViews.append(timeRecordview)
        return TimeRecordViews

    def GetAllBetweenDates(self,fromDate,toDate):
        self.Cursor.execute("SELECT * FROM vwTimeRecord where Date between ? and ? order by StartTime DESC",(fromDate,toDate))
        rows = self.Cursor.fetchall()
        TimeRecordViews = []
        for row in rows:
            timeRecordview = TimeRecordView.TimeRecordView(row[0],row[1],row[2],row[3],row[4],row[5],row[6],str(row[7]).replace("\n",""))
            TimeRecordViews.append(timeRecordview)
        return TimeRecordViews