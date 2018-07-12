from BusinessLogic import BLTimeRecordView,BLDayView,BLProject,BLRecordType,BLTimeRecord
from BusinessEntities import TimeRecordView,DayView,Project,RecordType
from DataAccess.Log import Logger

class Cache:
    def __init__(self,conn):
        Logger.LogInfo('Cache: Initializing Cache')
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
        Logger.LogInfo('Cache: Cache initialized')

    def RefreshTimeRecordsForDate(self,date):
        Logger.LogInfo('Refreshing TimeRecords for date: ' + date)
        self.TimeRecordViews = self.blTrv.GetAllForDate(date)
        self.TimeRecords = self.blTr.GetAllForDate(date)
        Logger.LogInfo('Done refreshing TimeRecords')

        
    def RefreshDayViews(self):
        Logger.LogInfo('Refreshing DayViews')
        self.DayViews = self.blVwD.GetAll()
        Logger.LogInfo('Done refreshing DayViews')

    def RefreshProjects(self):
        Logger.LogInfo('Refreshing Projects')
        self.ActiveProjects = self.blPr.GetAll(False)
        self.AllProjects = self.blPr.GetAll()
        Logger.LogInfo('Done refreshing projects')

    def RefreshRecordTypes(self):
        Logger.LogInfo('Refresh RecordTypes')
        self.RecordTypes = self.blRt.GetAll()
        Logger.LogInfo('Done refreshing recordtypes')

    def RefreshAllStaticData(self):
        Logger.LogInfo('Refreshing all static data')
        self.DayViews = self.blVwD.GetAll()
        self.ActiveProjects = self.blPr.GetAll(False)
        self.AllProjects = self.blPr.GetAll()
        self.RecordTypes = self.blRt.GetAll()   
        Logger.LogInfo('Done refreshing all static data')     


    