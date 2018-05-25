from BusinessLogic import BLTimeRecordView,BLDayView,BLProject,BLRecordType
from BusinessEntities import TimeRecordView,DayView,Project,RecordType


class Cache:
    def __init__(self,conn): 
        self.blTrv = BLTimeRecordView.BLTimeRecordView(conn)
        self.blVwD = BLDayView.BLDayView(conn)
        self.blPr = BLProject.BLProject(conn)
        self.blRt = BLRecordType.BLRecordType(conn)
        self.DayViews = self.blVwD.GetAll()
        self.Projects = self.blPr.GetAll()
        self.RecordTypes = self.blRt.GetAll()
        self.TimeRecordViews = []

    def RefreshTimeRecordsForDate(self,date):
        self.TimeRecordViews = self.blTrv.GetAllForDate(date)
        
    def RefreshDayViews(self):
        self.DayViews = self.blVwD.GetAll()

    def RefreshProjects(self):
        self.Projects = self.blPr.GetAll()

    def RefreshRecordTypes(self):
        self.RecordTypes = self.blRt.GetAll()

    def RefreshAllStaticData(self):
        self.DayViews = self.blVwD.GetAll()
        self.Projects = self.blPr.GetAll()
        self.RecordTypes = self.blRt.GetAll()        


    