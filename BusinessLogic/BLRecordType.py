from DataAccess import DARecordType
from BusinessEntities import RecordType
import sqlite3

class BLRecordType:
    def __init__(self,conn):
        self.DAL = DARecordType.DARecordType(conn)

    def GetAll(self):
        return self.DAL.GetAll()

    def GetRecordTypeIDFromDescription(self,recordTypeName):
        return self.DAL.GetRecordTypeIDFromDescription(recordTypeName)

    def GetRecordTypeExterneID(self,recordTypeID):
        return self.DAL.GetRecordTypeExterneID(recordTypeID)
        