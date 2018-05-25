from DataAccess import DADayView
from BusinessEntities import DayView
import sqlite3

class BLDayView:
    def __init__(self,conn):
        self.DAL = DADayView.DADayView(conn)

    def GetAll(self):
        return self.DAL.GetAll()