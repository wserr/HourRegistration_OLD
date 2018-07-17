
#Import Modules

from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView,TimeRecordView
from DataAccess import DAController
import time
from GUI.TimeRecordEditForm import *
from GUI.ExportToExcelForm import *
from GUI.ProjectListForm import *
import os
import threading
import queue
from DataAccess.Log import Logger
import configparser
from shutil import copyfile
import datetime

class MainScreen:
    def __init__(self,master,connection):
        #Reset Database if necessary
        Globals.ClearUserTables(connection)
        self.Config = configparser.ConfigParser()
        self.Config.read('config.ini')

        #Main Window
        self.Master = master
        self.Master.title("Hour Registration")

        #Database connection
        self.dbConnection = connection

        #Initialize Cache
        self.Cache = Cache.Cache(connection)

        #Initialize String Vars
        self.RecordTypeValue = StringVar()
        self.ProjectValue = StringVar()
        self.DescriptionValue = StringVar()
        self.LastLogon = StringVar()
        self.LastLogon.set(Globals.GetLastLogon())

        #Designer
        self.DaysCombo = ttk.Combobox(master)
        self.DaysCombo.grid(row=0,column=0,sticky='NSEW',columnspan=3)

        self.RecordButton = Button(master,text = "Start Recording",command = self.StartRecording)
        self.RecordButton.grid(row=  1,column = 0,sticky='NSEW')
        self.RecordIcon = PhotoImage(file=".\\Resources\\add.png")
        self.RecordButton.config(image=self.RecordIcon,width="32",height="32")

        self.DeleteRecordButton = Button(master,text = "Delete Record",command = self.DeleteRecord)
        self.DeleteRecordButton.grid(row=1  ,column = 1,sticky='NSEW')
        self.DeleteRecordIcon = PhotoImage(file=".\\Resources\\delete.png")
        self.DeleteRecordButton.config(image=self.DeleteRecordIcon,width="32",height="32")

        self.StopRecordButton = Button(master,text = "Stop Recording",command = self.StopRecording)
        self.StopRecordButton.grid(row=  1,column = 2,sticky='NSEW')
        self.StopRecordIcon = PhotoImage(file=".\\Resources\\stop.png")
        self.StopRecordButton.config(image=self.StopRecordIcon,width="32",height="32")
            
        self.CopyToCodexButton = Button(master, text = "Copy To Codex", command = self.CopyToCodex)
        self.CopyToCodexButton.grid(row = 2,column=0,sticky='NSEW')
        self.CopyIcon = PhotoImage(file=".\\Resources\\copyCodex.png")
        self.CopyToCodexButton.config(image=self.CopyIcon,width="32",height="32")

        self.ExcelButton = Button(master,text ="Export",command = self.ExportToExcel)
        self.ExcelButton.grid(row = 2,column=1,sticky='NSEW')
        self.ExcelIcon = PhotoImage(file=".\\Resources\\excel.png")
        self.ExcelButton.config(image=self.ExcelIcon,width="32",height="32")

        self.ProjectButton = Button(master,text = "Project",command = self.OpenProjectListForm)
        self.ProjectButton.grid(row=2,column = 2,sticky='NSEW')
        self.ProjectIcon = PhotoImage(file=".\\Resources\\add_project.png")
        self.ProjectButton.config(image=self.ProjectIcon,width="32",height="32")

        self.CopyRecordButton = Button(master,text = "CopyRecord",command = self.CopyRecord)
        self.CopyRecordButton.grid(row=3,column = 0,sticky='NSEW')
        self.CopyRecordIcon = PhotoImage(file=".\\Resources\\copy.png")
        self.CopyRecordButton.config(image=self.CopyRecordIcon,width="32",height="32")

        self.OneNoteButton = Button(master,text = "OneNote",command = self.OpenInOneNote)
        self.OneNoteButton.grid(row=3,column = 1,sticky='NSEW')
        self.OneNoteIcon = PhotoImage(file=".\\Resources\\onenote.png")
        self.OneNoteButton.config(image=self.OneNoteIcon,width="32",height="32")

        self.AddTimeRecordButton = Button(master,text = "AddTimeRecordButton",command = self.ShowNewEditForm)
        self.AddTimeRecordButton.grid(row=3,column=2,sticky="NSEW")
        self.AddTimeRecordIcon = PhotoImage(file=".\\Resources\\application_add.png")
        self.AddTimeRecordButton.config(image=self.AddTimeRecordIcon,width="32",height="32")

        self.BackupButton = Button(master,text = "BackupButton",command = self.DatabaseBackup)
        self.BackupButton.grid(row=4,column=0,sticky="NSEW")
        self.BackupButtonIcon = PhotoImage(file=".\\Resources\\angel.png")
        self.BackupButton.config(image=self.BackupButtonIcon,width="32",height="32")

        self.ProjectsCombo = ttk.Combobox(master,width = 100,textvariable = self.ProjectValue)
        self.ProjectsCombo.grid(row = 0,column = 3,sticky='NSEW')

        self.RecordTypeCombo = ttk.Combobox(master,textvariable = self.RecordTypeValue)
        self.RecordTypeCombo.grid(row = 1,column = 3,sticky='NSEW')

        self.DescriptionTextBox = Entry(master,textvariable = self.DescriptionValue)
        self.DescriptionTextBox.grid(row = 2,column = 3,sticky='NSEW')

        self.RecordsListBox = Listbox(master)
        self.RecordsListBox.grid(row = 3,column =3, rowspan = 7,columnspan = 3,sticky='NSEW')

        self.EventLogExplanationLabel = Label(master,text="Laatst aangemeld op: ")
        self.EventLogExplanationLabel.grid(row=0,column=4)

        self.EventLogLabel = Label(master,textvariable = self.LastLogon)
        self.EventLogLabel.grid(row=1,column = 4)

        self.DaysCombo.bind("<<ComboboxSelected>>",self.DaysCombo_SelectedItemChanged)
        self.RecordsListBox.bind("<<ListboxSelect>>",self.RecordsListBox_SelectedItemChanged)
        self.RecordsListBox.bind('<Double-1>', lambda x: self.ShowEditForm())
        #End Designer

        #Set Form Controls
        self.FillCombos()
        self.SetButtonsEnabled()

        self.Queue = queue.Queue(10)
        self.KillEvent = threading.Event()
        self.ControllerThread = threading.Thread(target=self.ctrl,args=(self.Queue,self.KillEvent))
        self.ControllerThread.start()
        Logger.LogInfo(self.ControllerThread.getName() + ' started.')

        self.CheckForUpdatesFromController()

    def ctrl(self,queue,killEvent):
        dac = DAController.DAController(queue,killEvent)
        dac.Listen()

    def DatabaseBackup(self):
        source = self.Config['DEFAULT']['databasename']
        destination = self.Config['DEFAULT']['databasebackuplocation'] + '{}.db'.format(time.strftime('%Y%m%d%H%M'))
        copyfile(source,destination)
        messagebox.showinfo('Backup','Database backup made')

    def CheckForUpdatesFromController(self):
        if not self.Queue.empty():
            queue = self.Queue.get()
            blPr = BLProject.BLProject(self.dbConnection)
            project = blPr.GetByButton(queue)
            if project is not None:
                print(project.Description)
                recordType = 1
                blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
                for record in self.Cache.TimeRecords:
                    if record.StatusID == TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value:
                        record.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestopt.value
                        record.EndHour = Globals.GetCurrentTime()
                        blTr.Update(record)
                timeRecord = TimeRecord.TimeRecord(None,Globals.GetCurrentTime(),None,project.ID,recordType,'Automatically generated',TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value,0,None,None)
                valid = TimeRecordValidation.TimeRecordValidation()
                validationMessage = valid.ValidateOnCreation(timeRecord)
                if  not len(validationMessage) == 0:
                    errorMessage = ''
                    for i in validationMessage:
                        errorMessage = errorMessage + i + '\n'
                    messagebox.showerror('Error',errorMessage)
                else:
                    index = self.DaysCombo.current()
                    blTr.Create(timeRecord)
                    self.Cache.RefreshAllStaticData()
                    self.FillCombos()
                    if index==-1: index = 0
                    self.DaysCombo.current(index)
                    self.RefreshTimeRecords() 
        self.Master.after(500, self.CheckForUpdatesFromController)

    def OpenInOneNote(self):
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        os.system("start "+timeRecordView.OneNoteLink)

    def CopyRecord(self):
        blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        timeRecord = blTr.GetById(timeRecordView.ID)
        blTr.CopyTimeRecord(timeRecord)
        self.Refresh()

    def Refresh(self):
        index = self.DaysCombo.current()
        self.DaysCombo.current(0)
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        self.DaysCombo.current(index)
        self.RefreshTimeRecords() 
        self.SetButtonsEnabled()
      
    def RecordsListBox_SelectedItemChanged(self,eventObject):
        self.SetButtonsEnabled()

    def DaysCombo_SelectedItemChanged(self,eventObject):
        self.RefreshTimeRecords()
        self.SetButtonsEnabled()

    def RefreshTimeRecords(self):
        index = self.DaysCombo.current()
        if not index == -1:
            date = self.Cache.DayViews[index].Date
            self.Cache.RefreshTimeRecordsForDate(date)
            self.FillTimeRecords(self.Cache.TimeRecordViews)
        else:
            self.RecordsListBox.delete(0,END)

    def Show(self):
        self.Master.mainloop()

    def FillCombos(self):
        self.FillProjectCombo()
        self.FillRecordTypeCombo()
        self.FillDays()

    def FillProjectCombo(self):
        self.ProjectsCombo['value'] = self.Cache.ActiveProjects

    def FillRecordTypeCombo(self):
        self.RecordTypeCombo['value'] = self.Cache.RecordTypes

    def FillDays(self):
        self.DaysCombo['value'] = self.Cache.DayViews

    def FillTimeRecords(self,timeRecordViews):
        self.RecordsListBox.delete(0,END)
        for item in timeRecordViews:     
            self.RecordsListBox.insert(END,item)
        for i in range(0,self.RecordsListBox.size()):
            item = timeRecordViews[i]
            itemStatus = item.Status
            if itemStatus == 'Gestart':
                self.RecordsListBox.itemconfig(i,{'bg':'red'})
            elif itemStatus == 'Gestopt':
                self.RecordsListBox.itemconfig(i,{'bg':'green'})
            elif itemStatus == 'Gekopieerd':
                self.RecordsListBox.itemconfig(i,{'bg':'orange'})              

    def StartRecording(self):
        recordIndex = self.RecordTypeCombo.current()
        projectIndex = self.ProjectsCombo.current()
        if recordIndex == -1: recordType = ''
        else: recordType = self.Cache.RecordTypes[recordIndex].ID
        if projectIndex == -1: project = None 
        else: project = self.Cache.ActiveProjects[projectIndex].ID
        timeRecord = TimeRecord.TimeRecord(None,Globals.GetCurrentTime(),None,project,recordType,self.DescriptionValue.get(),TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value,0,None,None)
        
        valid = TimeRecordValidation.TimeRecordValidation()
        validationMessage = valid.ValidateOnCreation(timeRecord)
        if  not len(validationMessage) == 0:
            errorMessage = ''
            for i in validationMessage:
                errorMessage = errorMessage + i + '\n'
            messagebox.showerror('Error',errorMessage)
        else:
            index = self.DaysCombo.current()
            blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
            blTr.Create(timeRecord)
            self.Cache.RefreshAllStaticData()
            self.FillCombos()
            if index==-1: index = 0
            self.DaysCombo.current(index)
            self.RefreshTimeRecords() 

    def StopRecording(self):
        blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        timeRecord = blTr.GetById(timeRecordView.ID)
        timeRecord.EndHour = Globals.GetCurrentTime()

        timeRecord.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestopt.value
        blTr.Update(timeRecord)
        index = self.DaysCombo.current()
        self.DaysCombo.current(0)
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        self.DaysCombo.current(index)
        self.RefreshTimeRecords()
        self.SetButtonsEnabled()
    
    def CopyToCodex(self):
        self.Master.clipboard_clear()
        index = self.DaysCombo.current()
        date = self.Cache.DayViews[index].Date
        self.Master.clipboard_append(Globals.CopyToCodex(self.dbConnection,date))
        self.RefreshTimeRecords()

    def ShowEditForm(self):
        timeRecordView = self.Cache.TimeRecordViews[self.RecordsListBox.curselection()[0]]    
        edit = TimeRecordEditForm(self.dbConnection,timeRecordView,self.Cache)
        edit.Show()
        index = self.DaysCombo.current()
        self.DaysCombo.current(0)
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        self.DaysCombo.current(index)
        self.RefreshTimeRecords()
        edit.Master.destroy()

    def ShowNewEditForm(self):
        tr = TimeRecordView.TimeRecordView(None,None,None,None,None,None,None,None,None,None)
        index = self.DaysCombo.current()
        tr.Date = self.Cache.DayViews[index].Date
        edit = TimeRecordEditForm(self.dbConnection,tr,self.Cache)
        edit.Show()
        index = self.DaysCombo.current()
        self.DaysCombo.current(0)
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        self.DaysCombo.current(index)
        self.RefreshTimeRecords()
        edit.Master.destroy()

    def OpenProjectListForm(self):
        projectListForm = ProjectListForm(self.Cache,self.dbConnection)
        projectListForm.Show()     
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        projectListForm.Master.destroy() 

    def ExportToExcel(self):
        excel = ExportToExcelForm(self.dbConnection)
        excel.Show()
        excel.Master.destroy()

    def DeleteRecord(self):
        bl = BLTimeRecord.BLTimeRecord(self.dbConnection)
        indexRecordsListBox = self.RecordsListBox.curselection()[0]
        record = self.Cache.TimeRecordViews[indexRecordsListBox]
        bl.DeleteByID(record.ID)
        index = self.DaysCombo.current()
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        #Hier schiet nog 1 record over; het is nog niet verwijderd uit Cache op dit moment
        if len(self.Cache.TimeRecordViews)==1: 
            self.DaysCombo.set('')
        else:
            self.DaysCombo.current(index)
        self.RefreshTimeRecords()
        self.SetButtonsEnabled()

    def SetButtonsEnabled(self):
        enableStop = True
        enableCopyToCodex = True
        enableDelete = True
        enableCopyRecord = True
        enableOpenOneNote = True
        indexDaysCombo = self.DaysCombo.current()
        indexRecordsListBox = self.RecordsListBox.curselection()
        current = Globals.GetCurrentDay()
        if indexDaysCombo==-1:
            enableStop=False
            enableCopyToCodex=False
        else:
            date = self.Cache.DayViews[indexDaysCombo].Date
            if not current==date:
                enableStop=False
            bl = BLTimeRecord.BLTimeRecord(self.dbConnection)
            records = bl.GetAllForDate(date)
            for record in records:
                if record.StatusID==TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value:
                    enableCopyToCodex=False           
        if len(indexRecordsListBox) == 0:
            enableStop=False
            enableDelete = False
            enableCopyRecord = False
            enableOpenOneNote = False
        else:
            trView = self.Cache.TimeRecordViews[indexRecordsListBox[0]]
            if trView.OneNoteLink == 'None' or trView.OneNoteLink == "":
                enableOpenOneNote = False
          
        self.SetButton(enableStop,self.StopRecordButton)
        self.SetButton(enableCopyToCodex,self.CopyToCodexButton)
        self.SetButton(enableDelete,self.DeleteRecordButton)
        self.SetButton(enableCopyRecord,self.CopyRecordButton)
        self.SetButton(enableOpenOneNote,self.OneNoteButton)

        
    def SetButton(self,enabled,button):
        if enabled:
            button.config(state=NORMAL)
        else:
            button.config(state=DISABLED)







    



