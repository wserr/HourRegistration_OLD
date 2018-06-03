from tkinter import *
from tkinter import ttk,messagebox,filedialog
from BusinessLogic import BLExcel,BLTimeRecordView,Globals



class ExportToExcelForm:
    def __init__(self,conn):
        master = Toplevel()
        self.Master = master
        self.Connection = conn
        self.DateFrom = StringVar()
        self.DateTo = StringVar()

        self.Master.title("Export To Excel")

        self.ExplanationLabel = Label(master,text='Export to excel between dates')
        self.ExplanationLabel.grid(row = 0,column = 0, columnspan = 2)

        self.DateFromLabel = Label(master,text = 'Select FROM date (yyyy-mm-dd):')
        self.DateFromLabel.grid(row=1,column=0)

        self.DateFromTextBox = Entry(master,textvariable = self.DateFrom)
        self.DateFromTextBox.grid(row=1,column = 1,sticky='NSEW')

        self.DateFromLabel = Label(master,text = 'Select TO date (yyyy-mm-dd):')
        self.DateFromLabel.grid(row=2,column=0)

        self.DateToTextBox = Entry(master,textvariable = self.DateTo)
        self.DateToTextBox.grid(row=2,column = 1,sticky='NSEW')

        self.OKButton = Button(master,text="OK",command = self.Confirm)
        self.OKButton.grid(row = 3,column = 0,sticky='NSEW')

    
    def Confirm(self):
        blE = BLExcel.BLExcel(self.Connection)
        fromDate = self.DateFrom.get()
        toDate = self.DateTo.get()
        blTrV = BLTimeRecordView.BLTimeRecordView(self.Connection)
        timeRecords = blTrV.GetAllBetweenDates(fromDate,toDate)
        result = messagebox.askquestion("Validatie", "{0} records geselecteerd. Doorgaan?".format(len(timeRecords)), icon='warning')
        if result == 'yes':
            file_path = filedialog.askdirectory()
            file_path = file_path + "/" + Globals.GetCurrentDay()
            blE.ExportToExcel(timeRecords,file_path)
            self.Master.quit()

    def Show(self):
        self.Master.mainloop()
