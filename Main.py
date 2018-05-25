from DataAccess.DataBaseConnection import DataBaseConnection
from BusinessEntities import *
from DataAccess.DAProject import DAProject
from GUI.MainScreen import MainScreen
from DataAccess.Log import Logger
from tkinter import Tk,ttk

#Handle Project Init(ialisations
root = Tk()
databaseConnection = DataBaseConnection()

try:
    mainScreen = MainScreen(root,databaseConnection)
    mainScreen.Show()
    # proj = DAProject(databaseConnection.Connection)
    # projs = proj.GetAll()
    # for proj in projs:
    #     print(proj.Description)
# except Exception as e:
#     Logger.LogError(traceback.print_exception(exc_type, exc_value, exc_traceback,
#                               limit=2))
finally:
    databaseConnection.CloseConnection()
















