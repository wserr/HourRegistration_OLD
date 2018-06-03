import sqlite3
from BusinessEntities import DayView

class DADayView:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()

    def GetAll(self):
        self.Cursor.execute("SELECT * FROM vwDays limit 5")
        rows = self.Cursor.fetchall()
        Days = []
        for row in rows:
            day = DayView.DayView(row[0],row[1])
            Days.append(day)
        return Days