from DataAccess import DAExcel
from BusinessEntities import Project
from BusinessLogic import BLTimeRecordView
import sqlite3

class BLExcel:
    def __init__(self,conn):
        self.DAL = DAExcel.DAExcel(conn)
        
    def ExportToExcel(self,timeRecordViews,path):
        self.DAL.ExportToExcel(timeRecordViews,path)

