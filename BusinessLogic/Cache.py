from BusinessLogic import BLTimeRecordView,BLDayView,BLProject,BLRecordType,BLTimeRecord
from BusinessEntities import TimeRecordView,DayView,Project,RecordType


class Cache:
    def __init__(self,conn): 
        self.blTrv = BLTimeRecordView.BLTimeRecordView(conn)
        self.blVwD = BLDayView.BLDayView(conn)
        self.blPr = BLProject.BLProject(conn)
        self.blRt = BLRecordType.BLRecordType(conn)
        self.blTr = BLTimeRecord.BLTimeRecord(conn)
        self.DayViews = self.blVwD.GetAll()
        self.ActiveProjects = self.blPr.GetAll(False)
        self.AllProjects = self.blPr.GetAll()
        self.RecordTypes = self.blRt.GetAll()
        self.TimeRecordViews = []
        self.TimeRecords = []

    def RefreshTimeRecordsForDate(self,date):
        self.TimeRecordViews = self.blTrv.GetAllForDate(date)
        self.TimeRecords = self.blTr.GetAllForDate(date)
        
    def RefreshDayViews(self):
        self.DayViews = self.blVwD.GetAll()

    def RefreshProjects(self):
        self.ActiveProjects = self.blPr.GetAll(False)
        self.AllProjects = self.blPr.GetAll()

    def RefreshRecordTypes(self):
        self.RecordTypes = self.blRt.GetAll()

    def RefreshAllStaticData(self):
        self.DayViews = self.blVwD.GetAll()
        self.ActiveProjects = self.blPr.GetAll(False)
        self.AllProjects = self.blPr.GetAll()
        self.RecordTypes = self.blRt.GetAll()        


    