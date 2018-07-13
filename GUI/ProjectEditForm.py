from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView,Project
import sqlite3
from DataAccess.Log import Logger
# import time
# import datetime


class ProjectEditForm:
    def __init__(self,conn,project=None):
        master = Tk()
        self.Connection = conn
        self.ProjectOmschrijvingVar = StringVar(master)
        self.ProjectIDVar = StringVar(master)
        self.Button = StringVar(master)

        self.Master = master
        self.Master.title("Project Edit Form")

        if project==None:
            self.BusinessEntity = None
        else:
            self.BusinessEntity = project
            self.ProjectOmschrijvingVar.set(project.Description)
            self.ProjectIDVar.set(project.ExterneId)
            if str(self.BusinessEntity.Button) == "None": 
                self.Button.set("") 
            else: self.Button.set(self.BusinessEntity.Button)

        self.ProjectOmschrijvingLabel = Label(master,text = 'Project Omschrijving: ')
        self.ProjectOmschrijvingLabel.grid(row=0,column=0)

        self.ProjectIDLabel = Label(master,text = 'Project Externe ID: ')
        self.ProjectIDLabel.grid(row=1,column=0)
              
        self.ProjectOmschrijving = Entry(master,textvariable = self.ProjectOmschrijvingVar)
        self.ProjectOmschrijving.grid(row=0,column = 1)

        self.ProjectID = Entry(master,textvariable = self.ProjectIDVar)
        self.ProjectID.grid(row=1,column=1)

        self.ProjectButtonLabel = Label(master,text = 'Project Button: ')
        self.ProjectButtonLabel.grid(row=5,column=0,sticky = 'NSEW')

        self.ProjectButton = Entry(master,textvariable = self.Button)
        self.ProjectButton.grid(row=5,column=1,sticky = 'NSEW')

        self.OKButton = Button(master,text="OK",command = self.Confirm)
        self.OKButton.grid(row = 6,column = 0,sticky='NSEW')

        self.CancelButton = Button(master, text="Cancel",command = self.Quit)
        self.CancelButton.grid(row=6,column=1,sticky='NSEW')



    def Show(self):
        self.Master.mainloop()

    def Quit(self):
        self.Master.destroy()

    def Confirm(self):
        try:
            if self.BusinessEntity==None:
                project = Project.Project(None,self.ProjectOmschrijvingVar.get(),self.ProjectIDVar.get(),self.Button.get(),True)
                if project.Button == '': project.Button = None
                bl = BLProject.BLProject(self.Connection)
                bl.Create(project)
            else:
                project = self.BusinessEntity
                project.Description = self.ProjectOmschrijvingVar.get()
                project.ExterneId = self.ProjectIDVar.get()
                project.Button = self.Button.get()
                if project.Button == '': project.Button = None
                bl = BLProject.BLProject(self.Connection)
                bl.Update(project)
            self.Master.quit()          
        except sqlite3.IntegrityError as e:
            messagebox.showerror('Error','Button must be unique')
            Logger.LogError(str(e))
            return
        except Exception as e:
            Logger.LogError(str(e))
            return


        



               



