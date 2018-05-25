import sqlite3
from BusinessEntities import Project

class DAProject:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()

    def GetAll(self):
        self.Cursor.execute("SELECT * FROM tblProject")
        rows = self.Cursor.fetchall()
        Projects = []
        for row in rows:
            project = Project.Project(row[0],row[1],row[2].replace("\n",""))
            Projects.append(project)
        return Projects

    def GetProjectIDFromDescription(self,projectName):
        sql = "select PRO_ID from tblProject where PRO_Description = ?"
        self.Cursor.execute(sql,(projectName,))
        result = []
        for row in self.Cursor.fetchall():
            result.append(row[0])
        if len(result)==0:
            return None
        else:
            return int(result[0])

    def GetProjectExterneID(self,projectID):
        sql = "select PRO_ExterneID from tblProject where PRO_ID = ?"
        self.Cursor.execute(sql,(projectID,))
        result = []
        for row in self.Cursor.fetchall():
            result.append(row[0])
        if len(result)==0:
            return None
        else:
            return result[0] 

        