
from tkinter import *
from tkinter import ttk,messagebox
from BusinessLogic import BLProject,BLRecordType,BLTimeRecordView,BLTimeRecord,TimeRecordValidation,BLDayView, Cache, Globals
from BusinessEntities import TimeRecord,TimeRecordStatusEnum,DayView
import time
from GUI.TimeRecordEditForm import *
from GUI.ExportToExcelForm import *

class MainScreen:
    def __init__(self,master,connection):
        self.dbConnection = connection
        self.Cache = Cache.Cache(connection)

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

        self.StopRecordButton = Button(master,text = "Stop Recording",command = self.StopRecording)
        self.StopRecordButton.grid(row=  1,column = 1,sticky='NSEW')
        self.StopRecordIcon = PhotoImage(file=".\\Resources\\stop.png")
        self.StopRecordButton.config(image=self.StopRecordIcon,width="32",height="32")
            
        self.CopyToCodexButton = Button(master, text = "Copy To Codex", command = self.CopyToCodex)
        self.CopyToCodexButton.grid(row = 1,column=2,sticky='NSEW')
        self.CopyIcon = PhotoImage(file=".\\Resources\\copy.png")
        self.CopyToCodexButton.config(image=self.CopyIcon,width="32",height="32")

        self.ProjectsCombo = ttk.Combobox(master,width = 100,textvariable = self.ProjectValue)
        self.ProjectsCombo.grid(row = 0,column = 3,sticky='NSEW')

        self.RecordTypeCombo = ttk.Combobox(master,textvariable = self.RecordTypeValue)
        self.RecordTypeCombo.grid(row = 1,column = 3,sticky='NSEW')

        self.DescriptionTextBox = Entry(master,textvariable = self.DescriptionValue)
        self.DescriptionTextBox.grid(row = 2,column = 3,sticky='NSEW')

        self.RecordsListBox = Listbox(master)
        self.RecordsListBox.grid(row = 3,column =3, rowspan = 2,columnspan = 3,sticky='NSEW')

        self.ExcelButton = Button(master,text ="Export",command = self.ExportToExcel)
        self.ExcelButton.grid(row = 2,column=0,sticky='NSEW')
        self.ExcelIcon = PhotoImage(file=".\\Resources\\Excel.png")
        self.ExcelButton.config(image=self.ExcelIcon,width="32",height="32")

        self.EventLogExplanationLabel = Label(master,text="Laatst aangemeld op: ")
        self.EventLogExplanationLabel.grid(row=0,column=4)

        self.EventLogLabel = Label(master,textvariable = self.LastLogon)
        self.EventLogLabel.grid(row=1,column = 4)

        self.FillCombos()

        self.DaysCombo.bind("<<ComboboxSelected>>",self.DaysCombo_SelectedItemChanged)
        self.RecordsListBox.bind("<<ListboxSelect>>",self.RecordsListBox_SelectedItemChanged)
        self.RecordsListBox.bind('<Double-1>', lambda x: self.ShowEditForm())

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

    def Show(self):
        self.Master.mainloop()

    def FillCombos(self):
        self.FillProjectCombo()
        self.FillRecordTypeCombo()
        self.FillDays()

    def FillProjectCombo(self):
        self.ProjectsCombo['value'] = self.Cache.Projects

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
        timeRecord = TimeRecord.TimeRecord(None,Globals.GetCurrentTime(),None,project,recordType,self.DescriptionValue.get(),TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value,0)
        
        valid = TimeRecordValidation.TimeRecordValidation()
        validationMessage = valid.ValidateOnCreation(timeRecord)
        if  not len(validationMessage) == 0:
            errorMessage = ''
            for i in validationMessage:
                errorMessage = errorMessage + i + '\n'
            messagebox.showerror('Error',errorMessage)
        else:
            blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
            blTr.Create(timeRecord)
            self.RefreshTimeRecords()
            self.FillCombos()


    def StopRecording(self):
        blTr = BLTimeRecord.BLTimeRecord(self.dbConnection)
        sel = self.RecordsListBox.curselection()[0]
        timeRecordView = self.Cache.TimeRecordViews[sel]
        timeRecord = blTr.GetById(timeRecordView.ID)
        timeRecord.EndHour = Globals.GetCurrentTime()

        timeRecord.StatusID = TimeRecordStatusEnum.TimeRecordStatusEnum.Gestopt.value
        blTr.Update(timeRecord)

        self.RefreshTimeRecords()
        self.Cache.RefreshDayViews()
        self.FillCombos()
    
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
             sequence = (item1,"\t","\t","\t",item2,"\t","\t","\t","\t","\t",item3,"\t",item4,"\t",string1,"\t",string2,"\n")
             self.Master.clipboard_append(s.join(sequence))

    def ShowEditForm(self):
        timeRecordView = self.Cache.TimeRecordViews[self.RecordsListBox.curselection()[0]]    
        edit = TimeRecordEditForm(self.dbConnection,timeRecordView,self.Cache)
        edit.Show()

        self.RefreshTimeRecords()
        self.Cache.RefreshAllStaticData()
        self.FillCombos()
        edit.Master.destroy()

    def ExportToExcel(self):
        excel = ExportToExcelForm(self.dbConnection)
        excel.Show()
        excel.Master.destroy()

    def SetButtonsEnabled(self):
        enableStop = True
        enableCopyToCodex = True
        indexDaysCombo = self.DaysCombo.current()
        indexRecordsListBox = self.RecordsListBox.curselection()
        current = Globals.GetCurrentDay()
        date = self.Cache.DayViews[indexDaysCombo].Date
        if indexDaysCombo==-1:
            enableStop=False
            enableCopyToCodex=False
        else:
            if not current==date:
                enableStop=False
        if len(indexRecordsListBox) == 0:
            enableStop=False

        bl = BLTimeRecord.BLTimeRecord(self.dbConnection)
        records = bl.GetAllForDate(date)
        for record in records:
            if record.StatusID==TimeRecordStatusEnum.TimeRecordStatusEnum.Gestart.value:
                enableCopyToCodex=False
    
        self.SetButton(enableStop,self.StopRecordButton)
        self.SetButton(enableCopyToCodex,self.CopyToCodexButton)

        
    def SetButton(self,enabled,button):
        if enabled:
            button.config(state=NORMAL)
        else:
            button.config(state=DISABLED)







    



