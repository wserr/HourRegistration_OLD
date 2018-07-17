import sqlite3
from BusinessEntities import DayView
import configparser

class DADayView:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()

    def GetAll(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        days = config['APP']['daysincombo']
        self.Cursor.execute("SELECT * FROM vwDays limit {}".format(days))
        rows = self.Cursor.fetchall()
        Days = []
        for row in rows:
            day = DayView.DayView(row[0],row[1])
            Days.append(day)
        return Days