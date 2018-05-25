import sqlite3
from BusinessEntities import TimeRecord

class DATimeRecord:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()
        self.Connection = conn.Connection

    def GetAll(self):
        self.Cursor.execute("SELECT * FROM tblTimeRecord")
        rows = self.Cursor.fetchall()
        TimeRecords = []
        for row in rows:
            timeRecord = TimeRecord.TimeRecord(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            TimeRecords.append(timeRecord)
        return TimeRecords

    def GetByIDList(self,Ids):
        idList = []
        for Id in Ids:
            idList.append(self.GetByID(Id))
        return idList

    def GetByID(self,Id):
        self.Cursor.execute("SELECT * FROM tblTimeRecord where TRE_ID = ?",(str(Id),))
        rows = self.Cursor.fetchall()
        TimeRecords = []
        for row in rows:
            timeRecord = TimeRecord.TimeRecord(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            TimeRecords.append(timeRecord)
        return TimeRecords[0]

    def Create(self,timeRecord):
        self.Cursor.execute("INSERT INTO tblTimeRecord (TRE_StartHour,TRE_EndHour,TRE_ProjectID,TRE_RecordTypeID,TRE_Description,TRE_StatusID,TRE_Minutes) values(?,?,?,?,?,?,?)",
        (timeRecord.StartHour,timeRecord.EndHour,timeRecord.ProjectID,timeRecord.RecordTypeID,timeRecord.Description,timeRecord.StatusID,timeRecord.Minutes))
        self.Connection.commit()

    def Update(self, timeRecord):
        self.Cursor.execute("Update tblTimeRecord set TRE_StartHour = ?,TRE_EndHour = ?,TRE_ProjectID=?,TRE_RecordTypeID=?,TRE_Description=?,TRE_StatusID=?,TRE_Minutes=? where TRE_ID = ?",
        (timeRecord.StartHour,timeRecord.EndHour,timeRecord.ProjectID,timeRecord.RecordTypeID,timeRecord.Description,timeRecord.StatusID,timeRecord.Minutes,timeRecord.ID))
        self.Connection.commit()

    def GetAllForDate(self,date):
        self.Cursor.execute("SELECT * from tblTimeRecord where strftime('%d-%m-%Y',TRE_StartHour) = ?",(date,))
        rows = self.Cursor.fetchall()
        TimeRecords = []
        for row in rows:
            timeRecord = TimeRecord.TimeRecord(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            TimeRecords.append(timeRecord)
        return TimeRecords  

