from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView,TimeRecordStatusEnum
import time
import datetime


class TimeRecordEditForm:
    def __init__(self,conn,timeRecordView,Cache):
        master = Tk()
        self.TimeRecord = timeRecordView
        self.RecordID = timeRecordView.ID
        if self.TimeRecord.Project == None:
            self.IsNew = True
        else:
            self.IsNew = False
        self.StartDate=StringVar(master,value=timeRecordView.StartHour)
        self.EndDate=StringVar(master,timeRecordView.EndHour)
        self.ProjectValue=StringVar(master,timeRecordView.Project)
        self.RecordTypeValue=StringVar(master,timeRecordView.RecordType)
        self.DescriptionValue=StringVar(master,value=timeRecordView.Description)
        self.OneNoteValue = StringVar(master,value=timeRecordView.OneNoteLink)
        self.KmValue = StringVar(master,value=timeRecordView.Km)
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

        self.KmLabel = Label(master,text = 'Aantal km: ')
        self.KmLabel.grid(row=6,column=0)
        
        self.KmTextBox = Entry(master,textvariable = self.KmValue)
        self.KmTextBox.grid(row=6,column = 1,sticky='NSEW')

        self.OKButton = Button(master,text="OK",command = self.Confirm)
        self.OKButton.grid(row = 7,column = 0,sticky='NSEW')

        self.CancelButton = Button(master, text="Cancel",command=self.Quit)
        self.CancelButton.grid(row=7,column=1,sticky='NSEW')

        self.FillCombos()

    def Confirm(self):
        # projectID = self.conn.GetProjectID(self.ProjectValue.get())
        # recordTypeID = self.conn.GetRecordTypeID(self.RecordTypeValue.get())
        # self.conn.UpdateSelectedRecord(self.RecordID,projectID,recordTypeID,self.StartDate.get(),self.EndDate.get(),self.DescriptionValue.get())
        blTr = BLTimeRecord.BLTimeRecord(self.Connection)
        Tr = blTr.GetById(self.RecordID)
        Tr.Description = self.DescriptionValue.get()
        timeString = Globals.ConvertToAmericanDate(self.TimeRecord.Date) + ' 00:00'
        Tr.StartHour = self.GetDate(timeString,self.StartDate.get())
        if not self.EndDate.get() =='':           
            Tr.EndHour = self.GetDate(Tr.StartHour,self.EndDate.get())
        Tr.ProjectID = self.Cache.ActiveProjects[self.ProjectsCombo.current()].ID
        Tr.RecordTypeID = self.Cache.RecordTypes[self.RecordTypeCombo.current()].ID
        Tr.Km = self.KmValue.get()

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

        if not self.IsNew:
            blTr.Update(Tr)
        else:
            Tr.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestopt.value
            blTr.Create(Tr)
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
