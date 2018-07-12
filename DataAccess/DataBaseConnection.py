import sqlite3
import configparser
from DataAccess.Log import Logger

class DataBaseConnection():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self.Connection = sqlite3.connect(config['DEFAULT']['DataBaseName'])
            Logger.LogInfo('DataBase Connection Established')
        except Exception as e:
            Logger.LogError(str(e))

    def CloseConnection(self):
        Logger.LogInfo('DataBase Connection Closed')
        self.Connection.close() 

