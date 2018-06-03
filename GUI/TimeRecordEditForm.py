from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView
import time
import datetime


class TimeRecordEditForm:
    def __init__(self,conn,timeRecord,Cache):
        master = Tk()
        self.TimeRecord = timeRecord
        self.RecordID = timeRecord.ID
        self.StartDate=StringVar(master,value=timeRecord.StartHour)
        self.EndDate=StringVar(master,timeRecord.EndHour)
        self.ProjectValue=StringVar(master,timeRecord.Project)
        self.RecordTypeValue=StringVar(master,timeRecord.RecordType)
        self.DescriptionValue=StringVar(master,value=timeRecord.Description)
        self.OneNoteValue = StringVar(master,value=timeRecord.OneNoteLink)
        if self.OneNoteValue.get()=="None": self.OneNoteValue.set("")
        self.Connection = conn
        self.Master = master
        self.Cache = Cache
        self.Master.title("Time Record")

        self.ProjectsLabel = Label(master,text = 'Project: ')
        self.ProjectsLabel.grid(row=0,column=0)

        self.ProjectsCombo = ttk.Combobox(master,width = 50,textvariable = self.ProjectValue)
        self.ProjectsCombo.grid(row = 0,column = 1,sticky='NSEW')

        self.RecordTypeLabel = Label(master,text = 'Record Type: ')
        self.RecordTypeLabel.grid(row=1,column=0)
        
        self.RecordTypeCombo = ttk.Combobox(master,width = 30,textvariable = self.RecordTypeValue)
        self.RecordTypeCombo.grid(row = 1,column = 1,sticky='NSEW')

        self.StartDateLabel = Label(master,text = 'Start Date: ')
        self.StartDateLabel.grid(row=2,column=0)
        
        self.StartDateTextBox = Entry(master,textvariable = self.StartDate)
        self.StartDateTextBox.grid(row=2,column = 1,sticky='NSEW')

        self.EndDateLabel = Label(master,text = 'End Date: ')
        self.EndDateLabel.grid(row=3,column=0)
        
        self.EndDateTextBox = Entry(master,textvariable = self.EndDate)
        self.EndDateTextBox.grid(row=3,column = 1,sticky='NSEW')

        self.DescriptionLabel = Label(master,text = 'Description: ')
        self.DescriptionLabel.grid(row=4,column=0)
        
        self.DescriptionTextBox = Entry(master,textvariable = self.DescriptionValue)
        self.DescriptionTextBox.grid(row=4,column = 1,sticky='NSEW')

        self.OneNoteLabel = Label(master,text = 'OneNote Link: ')
        self.OneNoteLabel.grid(row=5,column=0)
        
        self.OneNoteTextBox = Entry(master,textvariable = self.OneNoteValue)
        self.OneNoteTextBox.grid(row=5,column = 1,sticky='NSEW')

        self.OKButton = Button(master,text="OK",command = self.Confirm)
        self.OKButton.grid(row = 6,column = 0,sticky='NSEW')

        self.CancelButton = Button(master, text="Cancel",command=self.Quit)
        self.CancelButton.grid(row=6,column=1,sticky='NSEW')

        self.FillCombos()

    def Confirm(self):
        # projectID = self.conn.GetProjectID(self.ProjectValue.get())
        # recordTypeID = self.conn.GetRecordTypeID(self.RecordTypeValue.get())
        # self.conn.UpdateSelectedRecord(self.RecordID,projectID,recordTypeID,self.StartDate.get(),self.EndDate.get(),self.DescriptionValue.get())
        blTr = BLTimeRecord.BLTimeRecord(self.Connection)
        Tr = blTr.GetById(self.RecordID)
        Tr.Description = self.DescriptionValue.get()
        Tr.StartHour = self.GetDate(Tr.StartHour,self.StartDate.get())
        if not self.EndDate.get() =='':           
            Tr.EndHour = self.GetDate(Tr.EndHour,self.EndDate.get())
        Tr.ProjectID = self.Cache.ActiveProjects[self.ProjectsCombo.current()].ID
        Tr.RecordTypeID = self.Cache.RecordTypes[self.RecordTypeCombo.current()].ID


        oneNoteLink = self.OneNoteValue.get()

        try:
            if not oneNoteLink=="" and not oneNoteLink.startswith("onenote"):
                secondPart = oneNoteLink.split("onenote")[1]
                oneNoteLink = "onenote"+secondPart
        except:
            oneNoteLink = ""
            messagebox.showerror('Error',"No valid link found")
            return


        Tr.OneNoteLink = oneNoteLink


        blTr.Update(Tr)
        self.Master.quit()


    def Quit(self):
        self.Master.destroy()

    def FillCombos(self):
        self.FillProjectTypeCombo()
        self.FillRecordTypeCombo()

    def FillProjectTypeCombo(self):
        self.ProjectsCombo['value'] = self.Cache.ActiveProjects

    def FillRecordTypeCombo(self):
        self.RecordTypeCombo['value'] = self.Cache.RecordTypes


    def Show(self):       
        #my_gui = ProjectRecordEditForm(root)
        self.Master.mainloop()

    def GetDate(self,date,inputTime):
        timeArray = inputTime.split(':')
        hours = int(timeArray[0])
        minutes = int(timeArray[1])
        s1Time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        s2Time = s1Time.replace(hour=hours)
        s2Time = s2Time.replace(minute=minutes)
        return datetime.datetime.strftime(s2Time,"%Y-%m-%d %H:%M")
