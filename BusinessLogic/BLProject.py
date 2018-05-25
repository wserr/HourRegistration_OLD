from DataAccess import DAProject
from BusinessEntities import Project
import sqlite3

class BLProject:
    def __init__(self,conn):
        self.DAL = DAProject.DAProject(conn)

    def GetAll(self):
        return self.DAL.GetAll()

    def GetProjectIDFromDescription(self,projectName):
        return self.DAL.GetProjectIDFromDescription(projectName)

    def GetProjectExterneID(self,projectID):
        return self.DAL.GetProjectExterneID(projectID)