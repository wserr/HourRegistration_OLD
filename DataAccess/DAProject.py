import sqlite3
from BusinessEntities import Project

class DAProject:
    def __init__(self,conn):
        self.Cursor = conn.Connection.cursor()
        self.Connection = conn.Connection

    def GetAll(self,includeNotActive):
        if includeNotActive==False:
            self.Cursor.execute("SELECT * FROM tblProject where PRO_Actief = 1")
        else:
            self.Cursor.execute("SELECT * FROM tblProject")
        rows = self.Cursor.fetchall()
        Projects = []
        for row in rows:
            project = Project.Project(row[0],row[1],row[2],row[3])
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

    def Create(self,project):
        self.Cursor.execute("INSERT INTO tblProject (PRO_Description,PRO_ExterneID) values(?,?)",
        (project.Description,project.ExterneId))
        self.Connection.commit()

    def Update(self, project):
        self.Cursor.execute("Update tblProject set PRO_Description=?,PRO_ExterneID=?,PRO_Actief=? where PRO_ID=?",(project.Description,project.ExterneId,project.Active,project.ID))
        self.Connection.commit()

    def DeleteByID(self,projectID):
        self.Cursor.execute("delete from tblProject where PRO_ID = ?",(str(projectID),))
        self.Connection.commit()

    def DeleteAll(self):
        self.Cursor.execute("delete from tblProject")
        self.Connection.commit()       