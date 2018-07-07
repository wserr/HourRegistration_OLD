from DataAccess import DAProject
from BusinessEntities import Project
import sqlite3

class BLProject:
    def __init__(self,conn):
        self.DAL = DAProject.DAProject(conn)

    def GetAll(self,includeNotActive=True):
        return self.DAL.GetAll(includeNotActive)

    def GetProjectIDFromDescription(self,projectName):
        return self.DAL.GetProjectIDFromDescription(projectName)

    def GetProjectExterneID(self,projectID):
        return self.DAL.GetProjectExterneID(projectID)

    def Create(self,project):
        self.DAL.Create(project)

    def Update(self,project):
        self.DAL.Update(project)

    def DeleteByID(self,projectID):
        self.DAL.DeleteByID(projectID)

    def DeleteAll(self):
        self.DAL.DeleteAll()


    def GetByButton(self, buttonID,includeNotActive=False):
        return self.DAL.GetByButton(buttonID,includeNotActive)