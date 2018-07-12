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

try:
    Logger.LogInfo('Application Starting...')
    mainScreen = MainScreen(root,databaseConnection)
    mainScreen.Show()
except Exception as e:
    Logger.LogError(str(e),True)
finally:
    Logger.LogInfo('Application Stopping...')
    databaseConnection.CloseConnection()



















