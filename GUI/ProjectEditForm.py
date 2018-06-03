from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView,Project
# import time
# import datetime


class ProjectEditForm:
    def __init__(self,conn,project=None):
        master = Tk()
        self.Connection = conn
        self.ProjectOmschrijvingVar = StringVar(master)
        self.ProjectIDVar = StringVar(master)

        self.Master = master
        self.Master.title("Project Edit Form")

        if project==None:
            self.BusinessEntity = None
        else:
            self.BusinessEntity = project
            self.ProjectOmschrijvingVar.set(project.Description)
            self.ProjectIDVar.set(project.ExterneId)

        self.ProjectOmschrijvingLabel = Label(master,text = 'Project Omschrijving: ')
        self.ProjectOmschrijvingLabel.grid(row=0,column=0)

        self.ProjectIDLabel = Label(master,text = 'Project Externe ID: ')
        self.ProjectIDLabel.grid(row=1,column=0)
              
        self.ProjectOmschrijving = Entry(master,textvariable = self.ProjectOmschrijvingVar)
        self.ProjectOmschrijving.grid(row=0,column = 1)

        self.ProjectID = Entry(master,textvariable = self.ProjectIDVar)
        self.ProjectID.grid(row=1,column=1)


        self.OKButton = Button(master,text="OK",command = self.Confirm)
        self.OKButton.grid(row = 5,column = 0,sticky='NSEW')

        self.CancelButton = Button(master, text="Cancel",command = self.Quit)
        self.CancelButton.grid(row=5,column=1,sticky='NSEW')


    def Show(self):
        self.Master.mainloop()

    def Quit(self):
        self.Master.destroy()

    def Confirm(self):
        if self.BusinessEntity==None:
            project = Project.Project(None,self.ProjectOmschrijvingVar.get(),self.ProjectIDVar.get())
            bl = BLProject.BLProject(self.Connection)
            bl.Create(project)
        else:
            project = self.BusinessEntity
            project.Description = self.ProjectOmschrijvingVar.get()
            project.ExterneId = self.ProjectIDVar.get()
            bl = BLProject.BLProject(self.Connection)
            bl.Update(project)  
        self.Master.quit()          



