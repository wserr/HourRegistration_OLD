
from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView
import time
from GUI.TimeRecordEditForm import *
from GUI.ExportToExcelForm import *
from GUI.ProjectListForm import *
import os
import configparser

class MainScreen:
    def __init__(self,master,connection):
        self.dbConnection = connection

        self.Master = master
        self.Master.title("Overview")

        self.RecordTypeValue = StringVar()
        self.ProjectValue = StringVar()
        self.DescriptionValue = StringVar()
        self.LastLogon = StringVar()
        self.LastLogon.set(Globals.GetLastLogon())
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

        self.ResetTimeTables()

        self.Cache = Cache.Cache(connection)
        self.FillCombos()

        self.DaysCombo.bind("<<ComboboxSelected>>",self.DaysCombo_SelectedItemChanged)
        self.RecordsListBox.bind("<<ListboxSelect>>",self.RecordsListBox_SelectedItemChanged)
        self.RecordsListBox.bind('<Double-1>', lambda x: self.ShowEditForm())

        self.SetButtonsEnabled()



    def ResetTimeTables(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        reset = int(config['RESET']['Reset'])
        if reset == 1:
            blPr = BLProject.BLProject(self.dbConnection)
            blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
            blPr.DeleteAll()
            blTr.DeleteAll()
            config['RESET']['Reset'] = '0'   # create

            with open('config.ini', 'w') as configfile:    # save
                config.write(configfile)
            

    def OpenInOneNote(self):
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        os.system("start "+timeRecordView.OneNoteLink)

    def OpenProjectListForm(self):
        projectListForm = ProjectListForm(self.Cache,self.dbConnection)
        projectListForm.Show()     
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        projectListForm.Master.destroy() 


    def CopyRecord(self):
        blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        timeRecord = blTr.GetById(timeRecordView.ID)
        timeRecord.ID = None
        timeRecord.StartHour = Globals.GetCurrentTime()
        timeRecord.EndHour = None
        timeRecord.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value
        timeRecord.Minutes = 0
        blTr.Create(timeRecord)
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
        blRT = BLRecordType.BLRecordType(self.dbConnection)
        blPR = BLProject.BLProject(self.dbConnection)
        recordType = blRT.GetRecordTypeIDFromDescription(self.RecordTypeValue.get())
        project = blPR.GetProjectIDFromDescription(self.ProjectValue.get())
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
        blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
        index = self.DaysCombo.current()
        date = self.Cache.DayViews[index].Date
        timeRecords = blTr.GetAllForDate(date)

        blPr = BLProject.BLProject(self.dbConnection)
        blRt = BLRecordType.BLRecordType(self.dbConnection)
        for item in timeRecords:       
             item1 = blPr.GetProjectExterneID(item.ProjectID)
             item2 = blRt.GetRecordTypeExterneID(item.RecordTypeID)
             s1Time = time.strptime(item.StartHour, "%Y-%m-%d %H:%M")
             s2Time = time.strptime(item.EndHour,"%Y-%m-%d %H:%M")
             item3 = time.strftime("%H:%M",s1Time)
             item4 = time.strftime("%H:%M",s2Time)
             item5 = item.Description
             s="" 

             string1 = ""
             string2 = ""
             item.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gekopieerd.value
             blTr.Update(item)
             self.RefreshTimeRecords()
             if len(item5) > 30:
                 items = item5.split(" ")
                 countChar = 0

                 indexToSplit = 0
                 for i in range(0,len(items)):
                    countChar =countChar + len(items[i])
                    if i>30:
                        indexToSplit = i-1
                        break
                 filler = " "
                 if indexToSplit == 0:
                     indexToSplit = 30
                     filler = ""
                 list1 = item5[0:indexToSplit]
                 list2 = item5[indexToSplit:]
                 string1 = filler.join(list1)
                 string2 = filler.join(list2)
             else:
                 string1 = item5
             km = "\t"
             if not item.Km is None:
                 km = str(item.Km) + "\t"

             sequence = (item1,"\t","\t","\t",item2,"\t","\t","\t",km,"\t",item3,"\t",item4,"\t",string1,"\t",string2,"\n")
             self.Master.clipboard_append(s.join(sequence))

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







    



