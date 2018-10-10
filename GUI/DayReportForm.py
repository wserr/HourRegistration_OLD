import sys 
sys.path.append('.')

from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from DataAccess.DataBaseConnection import DataBaseConnection
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView,Project
import sqlite3
from DataAccess.Log import Logger

# import time
# import datetime


master = Tk()

daysCombo = ttk.Combobox(master)
daysCombo.grid(row=0,column=0)

conn = DataBaseConnection()
#Initialize Cache
cache = Cache.Cache(conn)
daysCombo['value'] = cache.DayViews





master.mainloop()







