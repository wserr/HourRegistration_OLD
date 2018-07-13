from DataAccess.DataBaseConnection import DataBaseConnection
from BusinessEntities import *
from DataAccess.DAProject import DAProject
from DataAccess.DAController import DAController
from GUI.MainScreen import MainScreen
from DataAccess.Log import Logger
from tkinter import Tk,ttk



#Handle Project Initialisations
root = Tk()
databaseConnection = DataBaseConnection()
mainScreen = MainScreen(root,databaseConnection)
try:
    Logger.LogInfo('Application Starting...')
    mainScreen.Show()
except Exception as e:
    Logger.LogError(str(e),True)
finally:
    mainScreen.KillEvent.set()
    mainScreen.ControllerThread.join()
    Logger.LogInfo('Application Stopping...')
    databaseConnection.CloseConnection()



















